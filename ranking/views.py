import logging
from typing import List
from django.http.response import HttpResponseBadRequest
from django.views.generic import DetailView, UpdateView, ListView

# from django.utils.decorators import method_decorator
from django.utils import timezone

# from django.views.decorators.http import last_modified
# from django.views.decorators.vary import vary_on_headers
from django.db.models import Q, Max
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect


from .forms import NoteForm, OrderedForm, VisibilityForm, NameForm
from .models import RankedList, RankedElement
from overview.models import Candidate


class _MyBallotMixin:
    def get_object(self):
        return RankedList.objects.for_request(self.request, force=True)


class RankedListExplore(ListView):
    template_name = "ranking/explore_lists.html"
    model = RankedList

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            filters = Q(public=True)
            if self.request.user.is_authenticated:
                filters = filters | Q(owner=self.request.user)
            return super().get_queryset().filter(filters)


class RankedListDetail(DetailView):
    template_name = "ranking/detail.html"
    model = RankedList

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            filters = Q(public=True)
            if self.request.user.is_authenticated:
                filters = filters | Q(owner=self.request.user)
            return super().get_queryset().filter(filters)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["annotations"] = self.object.annotated_candidates.select_related("candidate")
        return context


class DownloadRankedList(RankedListDetail):
    content_type = "text/plain"
    template_name = "ranking/detail.txt"

    def render_to_response(self, *args, **kwargs):
        resp = super().render_to_response(*args, **kwargs)
        resp["Content-Disposition"] = "attachment; filename={name}-ranking.txt".format(
            name=slugify(self.object.name)
        )
        return resp


class CandidateListField(forms.Field):
    def clean(self, value):
        if not value:
            raise forms.ValidationError("Something went wrong. Please reload and try again.")

        slugs = value.split(",")  # order is important!

        # make sure the candidates go into the dadtabase with the same order as
        # they came into the API
        candidates = Candidate.objects.filter(slug__in=slugs)
        candidates = sorted(candidates, key=lambda c: slugs.index(c.slug))

        if len(set(slugs)) != len(candidates):
            raise forms.ValidationError("unable to find candidate")
        return candidates


class EditForm(forms.ModelForm):
    """Only used for reordering candidates!"""

    candidates = CandidateListField()

    def save(self):
        self.instance.annotated_candidates.overwrite_list(self.cleaned_data["candidates"])
        self.instance.timestamp_modified = timezone.now()
        self.instance.save()
        return self.instance

    class Meta:
        model = RankedList
        fields: List[str] = []


def my_last_edit(request):
    view = MyList()
    view.request = request
    return view.get_object().last_modified


# @require_POST
def append_to_ballot(request, slug):
    try:
        candidate = Candidate.objects.get(is_running=True, hide=False, slug=slug)
    except Candidate.DoesNotExist:
        return HttpResponseBadRequest()

    ballot = RankedList.objects.for_request(request, force=True)
    max_order = ballot.annotated_candidates.aggregate(Max("order"))["order__max"]
    if max_order is None:
        max_order = -1

    ballot.annotated_candidates.create(candidate=candidate, order=max_order + 1)
    return redirect(candidate)


class RenameBallot(_MyBallotMixin, UpdateView):
    form_class = NameForm
    model = RankedList
    success_url = reverse_lazy("my_ranking")


# @method_decorator(vary_on_headers('HTTP_X_REQUESTED_WITH'), "get")
# @method_decorator(last_modified(my_last_edit), "get")
class MyList(_MyBallotMixin, UpdateView):
    form_class = EditForm
    model = RankedList
    template_name = "ranking/detail.html"
    success_url = reverse_lazy("my_ranking")

    def get_json(self, obj):
        return {
            "candidates": list(obj.annotated_candidates.values_list("candidate__slug", flat=True))
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["mine"] = True

        context["name_form"] = self.get_name_form()
        context["visibility_form"] = self.get_visibility_form()
        context["ordering_form"] = self.get_ordering_form()

        context["annotations"] = self.object.annotated_candidates.select_related("candidate")
        for annotation in context["annotations"]:
            annotation.comment_form = self.get_note_form(annotation)

        return context

    def get_name_form(self):
        return NameForm(instance=self.object)

    def get_visibility_form(self):
        return VisibilityForm(instance=self.object, initial={"public": not self.object.public})

    def get_ordering_form(self):
        return OrderedForm(instance=self.object, initial={"ordered": not self.object.ordered})

    def get_note_form(self, ranked_element):
        return NoteForm(instance=ranked_element)

    def get(self, request):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            self.object = self.get_object()
            return JsonResponse(self.get_json(self.object))
        else:
            return super().get(request)

    def form_invalid(self, form):
        ret = super().form_invalid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            logging.warning("uh oh", extra={"errors": form.errors})
            return JsonResponse(form.errors.as_json())
        else:
            return ret

    def form_valid(self, form):
        ret = super().form_valid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(self.get_json(form.instance))
        else:
            return ret


class MakePublic(_MyBallotMixin, UpdateView):
    model = RankedList
    form_class = VisibilityForm
    success_url = reverse_lazy("my_ranking")

    def get_initial(self):
        initial = super().get_initial()
        initial["public"] = not self.object.public
        return initial


class MakeOrdered(_MyBallotMixin, UpdateView):
    form_class = OrderedForm
    success_url = reverse_lazy("my_ranking")

    def get_initial(self):
        initial = super().get_initial()
        initial["ordered"] = not self.object.ordered
        return initial


class UpdateNote(UpdateView):
    form_class = NoteForm
    model = RankedElement

    def get_queryset(self):
        return RankedList.objects.for_request(self.request, force=True).annotated_candidates

    def get_object(self):
        try:
            return self.get_queryset().get(candidate__slug=self.kwargs["slug"])
        except RankedElement.DoesNotExist:
            # not sure if we'll ever need this
            candidate = Candidate.objects.get(slug=self.kwargs["slug"])
            return self.get_queryset().create(candidate=candidate)

    def form_valid(self, form):
        ret = super().form_valid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse("OK", status=200)
        else:
            return ret

    def get_success_url(self):
        return reverse("candidate_detail", args=[self.object.candidate.slug])


@require_POST
def delete_note(request, slug):
    """Deletes note and position in ranking"""

    candidate = get_object_or_404(Candidate.objects.all(), slug=slug)
    ranked_list = RankedList.objects.for_request(request, force=True)
    ranked_list.annotated_candidates.filter(candidate=candidate).delete()
    return HttpResponse("DELETED", status=201)
