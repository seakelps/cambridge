from django.test import TestCase
from django.urls import reverse

from . import factories


class CandidateListTest(TestCase):
    def test_sanity(self):
        factories.Candidate.create()
        factories.Candidate.create(is_running=False)

        resp = self.client.get(reverse("all"))
        self.assertEqual(resp.status_code, 200)


class ByOrganizationTest(TestCase):
    def setUp(self):
        super().setUp()
        factories.Candidate.create()
        factories.Candidate.create(is_running=False)

    def test_logged_out(self):
        resp = self.client.get(reverse("by-organization"))
        self.assertEqual(resp.status_code, 200)

    def test_logged_in(self):
        user = factories.User.create()
        self.client.force_login(user)

        resp = self.client.get(reverse("by-organization"))
        self.assertEqual(resp.status_code, 200)
