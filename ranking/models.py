from django.db import models
from django.conf import settings


class RankedListManager(models.Manager):
    def for_user(self, user):
        try:
            return user.rankedlist
        except RankedList.DoesNotExist:
            ranked_list = RankedList.objects.create(owner=user)
            ranked_list.save()
            ranked_list.owner = user
            ranked_list.save()
            return ranked_list


class RankedList(models.Model):
    objects = RankedListManager()

    last_modified = models.DateTimeField(auto_now=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    public = models.BooleanField(default=False)


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

    ranked_list = models.ForeignKey(RankedList, related_name="annotated_candidates")
    candidate = models.ForeignKey("overview.Candidate")
    comment = models.TextField(blank=True, default="")
    order = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        unique_together = (
            ("ranked_list", "candidate"),
            ("ranked_list", "order"),
        )
        ordering = "order",  # required for overwriting
