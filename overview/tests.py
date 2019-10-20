from django.test import TestCase
from django.urls import reverse

from .models import Candidate


class CandidateListTest(TestCase):
    def test_sanity(self):
        Candidate.objects.create(fullname="R McRunner", slug="runner")
        Candidate.objects.create(is_running=False, fullname="N McStationary", slug="non-runner")

        resp = self.client.get(reverse("all"))
        self.assertEqual(resp.status_code, 200)
