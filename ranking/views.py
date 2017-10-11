from django.views.generic import DetailView, UpdateView, ListView
from django.db.models import Q
from django import forms
from .models import RankedList
from overview.models import Candidate


class RankedListExplore(ListView):
    template_name = "ranking/explore_lists.html"
    model = RankedList

    def get_queryset(self):
        filters = Q(public=True)
        if self.request.user.is_authenticated:
            filters = filters | Q(owner=self.request.user)
        return super().get_queryset().filter(filters)


class RankedListDetail(DetailView):
    template_name = "ranking/detail.html"
    model = RankedList


class CandidateListField(forms.Field):
    def clean(self, value):
        ids = value.split(',')
        candidates = Candidate.objects.filter(id__in=ids)
        if len(ids) != len(candidates):
            raise forms.ValidationError("unable to find candidate")
        return candidates

    def bound_dsata(self, data, initial):
        if self.disabled:
            return ','.join(i.id for i in initial)
        return data


class EditForm(forms.ModelForm):
    candidates = CandidateListField()

    class Meta:
        model = RankedList
        fields = ['name', 'slug', 'public']


class MyList(UpdateView):
    form_class = EditForm
    model = RankedList
    template_name = "ranking/detail.html"

    def get_object(self):
        return RankedList.objects.for_user(self.request.user)
