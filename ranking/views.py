import logging
from django.views.generic import DetailView, UpdateView, ListView
# from django.utils.decorators import method_decorator
from django.utils import timezone
# from django.views.decorators.http import last_modified
# from django.views.decorators.vary import vary_on_headers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django import forms
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import RankedList, RankedElement
from overview.models import Candidate


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


class CandidateListField(forms.Field):
    def clean(self, value):
        slugs = value.split(',')  # order is important!

        # make sure the candidates go into the dadtabase with the same order as
        # they came into the API
        candidates = Candidate.objects.filter(slug__in=slugs)
        candidates = sorted(candidates, key=lambda c: slugs.index(c.slug))

        if len(set(slugs)) != len(candidates):
            raise forms.ValidationError("unable to find candidate")
        return candidates


class EditForm(forms.ModelForm):
    """ Only used for reordering candidates! """

    candidates = CandidateListField()

    def save(self):
        self.instance.annotated_candidates.overwrite_list(self.cleaned_data['candidates'])
        self.instance.timestamp_modified = timezone.now()
        self.instance.save()
        return self.instance

    class Meta:
        model = RankedList
        fields = []


def my_last_edit(request):
    view = MyList()
    view.request = request
    return view.get_object().last_modified


# @method_decorator(vary_on_headers('HTTP_X_REQUESTED_WITH'), "get")
# @method_decorator(last_modified(my_last_edit), "get")
class MyList(LoginRequiredMixin, UpdateView):
    form_class = EditForm
    model = RankedList
    template_name = "ranking/detail.html"
    success_url = reverse_lazy("my_ranking")

    def get_object(self):
        return RankedList.objects.for_user(self.request.user)

    def get_json(self, obj):
        return {"candidates": list(
            obj.annotated_candidates
            .values_list("candidate__slug", flat=True))
        }

    def get(self, request):
        if self.request.is_ajax():
            self.object = self.get_object()
            return JsonResponse(self.get_json(self.object))
        else:
            return super().get(request)

    def form_invalid(self, form):
        ret = super().form_invalid(form)
        if self.request.is_ajax():
            logging.warning("uh oh", extra={"errors": form.errors})
        else:
            ret

    def form_valid(self, form):
        ret = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(self.get_json(form.instance))
        else:
            return ret


class UpdateNote(UpdateView):
    fields = ['comment']
    model = RankedElement

    def get_queryset(self):
        return self.request.user.rankedlist.annotated_candidates.all()

    def get_object(self):
        try:
            return self.get_queryset().get(candidate__slug=self.kwargs['slug'])
        except RankedElement.DoesNotExist:
            # not sure if we'll ever need this
            candidate = Candidate.objects.get(slug=self.kwargs['slug'])
            return self.get_queryset().create(candidate=candidate)

    def form_valid(self, form):
        ret = super().form_valid(form)
        if self.request.is_ajax():
            return HttpResponse("OK", 200)
        else:
            return ret

    def get_success_url(self):
        return reverse("candidate_detail", args=[self.object.candidate.slug])
