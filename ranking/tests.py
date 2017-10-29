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


class OverwriteListTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = factories.RankedList().owner

    def test_swap(self):
        c1, c2, c3 = overview_factories.Candidate.create_batch(3)

        self.user.rankedlist.annotated_candidates.overwrite_list([c1, c2, c3])
        self.user.rankedlist.annotated_candidates.overwrite_list([c3, c1, c2])


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
            "candidates": candidate.slug
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
            "candidates": candidate.slug
        })
        self.assertEqual(resp.status_code, 302)

        self.assertTrue(self.user.rankedlist)
        self.assertTrue(self.user.rankedlist.annotated_candidates.get().candidate, candidate)

    def test_keep_comment(self):
        self.client.get(reverse("my_ranking"))

        candidate1, candidate2 = overview_factories.Candidate.create_batch(2)

        self.user.rankedlist.annotated_candidates.create(
            order=1,
            comment="My spoon is too big",
            candidate=candidate1)

        resp = self.client.post(reverse("my_ranking"), {
            "candidates": ','.join([candidate2.slug, candidate1.slug])
        })
        self.assertEqual(resp.status_code, 302)

        self.assertTrue(self.user.rankedlist)

        ranking1, ranking2 = self.user.rankedlist.annotated_candidates.all()

        self.assertEquals(ranking1.candidate, candidate2)
        self.assertFalse(ranking1.comment)

        self.assertEquals(ranking2.candidate, candidate1)
        self.assertEquals(ranking2.comment, "My spoon is too big")


class UpdateNotes(TestCase):
    def setUp(self):
        super().setUp()
        self.user = factories.RankedList().owner
        self.client.force_login(self.user)
        self.candidate = overview_factories.Candidate()

    def test_add_note(self):
        self.user.rankedlist.annotated_candidates.create(candidate=self.candidate, order=0)

        resp = self.client.post(
            reverse("update_note", args=[self.candidate.slug]),
            {"comment": "No Comment"})

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.user.rankedlist.annotated_candidates.get().comment, "No Comment")