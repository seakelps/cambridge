from urllib.parse import urlencode

from django.test import TestCase
from django.core.urlresolvers import reverse

from overview.models import Candidate


class ComparisonTest(TestCase):
    def test_compare_sanity(self):
        # not much to test yet, so make sure the page loads
        nadeem = Candidate.objects.create(
            slug="nadeem",
            fullname="Nadeem Mazen",
            shortname="Nadeem")

        jan = Candidate.objects.create(
            slug="jan",
            fullname="Jan Deveroux",
            shortname="Jan")

        qs = urlencode([("cand", nadeem.slug), ("cand", jan.slug)])
        resp = self.client.get("{}?{}".format(reverse("compare_candidates"), qs))
        self.assertEqual(resp.status_code, 200)

        found = resp.context['found_candidates']
        self.assertIn(nadeem, found)
        self.assertIn(jan, found)
