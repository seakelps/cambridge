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
        self.all().delete()  # I thought set would do this...
        print(list(enumerate(candidates)))
        self.set(
            [RankedElement(candidate=c, order=i) for i, c in enumerate(candidates)],
            bulk=False)


class RankedElement(models.Model):
    objects = RankedElementManager()

    ranked_list = models.ForeignKey(RankedList, related_name="annotated_candidates")
    candidate = models.ForeignKey("overview.Candidate")
    comment = models.TextField()
    order = models.PositiveSmallIntegerField(blank=True)

    class Meta:
        unique_together = (
            ("ranked_list", "candidate"),
            ("ranked_list", "order"),
        )
        ordering = "order",  # required for overwriting
