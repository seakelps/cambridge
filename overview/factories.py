from django.contrib.auth import get_user_model
from django.utils.text import slugify
import factory.fuzzy
from . import models


class User(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = 'username',

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")


class Candidate(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Candidate
        django_get_or_create = 'slug',

    fullname = factory.Faker("name")
    shortname = factory.LazyAttribute(lambda o: o.fullname.split(' ')[0])
    slug = factory.LazyAttribute(lambda o: slugify(o.fullname))
