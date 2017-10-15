from django.test import TestCase
from django.urls import reverse
from overview import factories as overview_factories
from . import factories


class ListViewTest(TestCase):
    def test_empty(self):
        resp = self.client.get(reverse("list_explore"))
        self.assertEqual(resp.status_code, 200)

    def test_public_loggedout(self):
        public_list = factories.RankedList()
        factories.RankedElement.create_batch(10, ranked_list=public_list)

        resp = self.client.get(reverse("list_explore"))
        self.assertEqual(resp.status_code, 200)

    def test_public_loggedin(self):
        user = overview_factories.User()
        self.client.force_login(user)

        public_list = factories.RankedList()
        factories.RankedElement.create_batch(10, ranked_list=public_list)

        resp = self.client.get(reverse("list_explore"))
        self.assertEqual(resp.status_code, 200)


class MyListTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = overview_factories.User()
        self.client.force_login(self.user)

    def test_create_list(self):
        resp = self.client.get(reverse("my_ranking"))
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(self.user.rankedlist)

    def test_save_candidate(self):
        self.client.get(reverse("my_ranking"))
        candidate = overview_factories.Candidate()

        resp = self.client.post(reverse("my_ranking"), {
            "candidates": [candidate.slug]
        })
        self.assertEqual(resp.status_code, 302)

        self.assertTrue(self.user.rankedlist)
        self.assertTrue(self.user.rankedlist.annotated_candidates.all())

    def test_overwrite(self):
        self.client.get(reverse("my_ranking"))

        self.user.rankedlist.annotated_candidates.create(
            order=1,
            candidate=overview_factories.Candidate())

        candidate = overview_factories.Candidate()

        resp = self.client.post(reverse("my_ranking"), {
            "candidates": [candidate.slug]
        })
        self.assertEqual(resp.status_code, 302)

        self.assertTrue(self.user.rankedlist)
        self.assertTrue(self.user.rankedlist.annotated_candidates.get().candidate, candidate)
