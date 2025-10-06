import random
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from typing import Optional


class RankedListManager(models.Manager):
    def for_request(self, request, election, *, force) -> Optional["RankedList"]:
        user = request.user

        if user.is_authenticated:
            try:
                return RankedList.objects.get(
                    owner=user,
                    election=election
                )
            except RankedList.DoesNotExist:
                if force:
                    return RankedList.objects.create(
                        name=RankedList.make_name(
                            user,
                            election,
                        ),
                        slug=user.username,
                        owner=user,
                        election=election
                    )
                else:
                    return None

        else:
            try:
                return RankedList.objects.get(
                    pk=request.session["ranked_list_id"],
                    election=election,

                )
            except (RankedList.DoesNotExist, KeyError):
                if not force:
                    return None

                # try hard to find an id
                for _ in range(5):
                    name = "Anon {}".format(random.randint(1000000, 2000000))

                    # can't reliably catch IntegrityErrors so get_or_creating here instead
                    ranked_list, created = RankedList.objects.get_or_create(
                        {"name": "{}'s Slate".format(name)}, 
                        slug=slugify(name),
                        election=election,
                    )

                    if created:
                        request.session["ranked_list_id"] = ranked_list.id
                        return ranked_list
                raise Exception("couldnt allocate a list id")


class RankedList(models.Model):
    objects = RankedListManager()

    election = models.ForeignKey("overview.Election", on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    ordered = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ("election", "slug")
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list_explore", args=[self.slug])

    @staticmethod
    def make_name(user, election):
        return "{username}'s {position} Slate".format(
            username=user.get_full_name() or user.username,
            position=election.position,
        )


class RankedElementManager(models.Manager):
    def overwrite_list(self, candidates):
        updated = set()

        # hack to make sure that when we assign something like order=1, there
        # are no elements on the list have order=1 before they get reassigned
        self.all().update(order=models.F("order") + 1000)

        for ranking in self.all():
            try:
                ranking.order = candidates.index(ranking.candidate) + 1
            except ValueError:
                ranking.delete()  # TODO keep these around but hide them
            else:
                updated.add(ranking.candidate)
                ranking.save()

        for new_candidate in set(candidates) - updated:
            self.create(candidate=new_candidate, order=candidates.index(new_candidate) + 1)


class RankedElement(models.Model):
    objects = RankedElementManager()

    ranked_list = models.ForeignKey(
        RankedList, related_name="annotated_candidates", on_delete=models.CASCADE
    )

    # probably need to reorder on delete
    candidate = models.ForeignKey("overview.CandidateElection", on_delete=models.CASCADE)
    comment = models.TextField(blank=True, default="")
    order = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        unique_together = (
            ("ranked_list", "candidate"),
            ("ranked_list", "order"),
        )
        ordering = ("order",)  # required for overwriting
