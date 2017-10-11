import random
from django.utils.text import slugify
import factory.fuzzy
from . import models
from faker.providers import BaseProvider
from overview.factories import User, Candidate


@factory.Faker.add_provider
class OrganizationProvider(BaseProvider):
    formats = (
        "A {{adjectiver}} Cambridge",
        "{{job}} local {{number}}",
        "{{adjective}} {{job}} Alliance",
        "{{job}}",
    )

    def org_name(self):
        pattern = self.random_element(self.formats)
        return self.generator.parse(pattern)

    def number(self):
        return str(random.randint(100, 1000))

    def adjective(self):
        return self.random_element([
            "Democratic", "Socialist", "Red", "Black",
            "Silly", "Smelly", "Sweaty", "Sticky",
        ])

    def adjectiver(self):
        adj = self.adjective()
        if adj.endswith("e"):
            return adj + "r"
        else:
            return adj + "er"


class RankedList(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RankedList
        django_get_or_create = 'slug',

    owner = factory.SubFactory(User)
    name = factory.Faker("org_name")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    public = True


class RankedElement(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RankedElement

    ranked_list = factory.SubFactory(RankedList)
    candidate = factory.SubFactory(Candidate)
    comment = factory.Faker("paragraph")
    order = factory.Sequence(lambda n: n)
