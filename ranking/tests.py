from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

from overview import factories as overview_factories
from . import factories
from .models import RankedList


class GetList(TestCase):
    def test_logged_in_no_list(self):
        request = RequestFactory().get('/')
        request.user = overview_factories.User()
        request.session = {}

        self.assertEqual(
            RankedList.objects.for_request(request),
            request.user.rankedlist)

    def test_logged_in_with_list(self):
        request = RequestFactory().get('/')
        ranked_list = factories.RankedList()
        request.user = ranked_list.owner
        request.session = {}

        self.assertEqual(
            RankedList.objects.for_request(request),
            ranked_list)

    def test_logged_out_no_list(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        request.session = {}

        ranked_list = RankedList.objects.for_request(request)
        self.assertTrue(ranked_list)
        self.assertEqual(ranked_list.id, request.session['ranked_list_id'])

    def test_logged_out_with_list(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()

        ranked_list = factories.RankedList(owner=None)
        request.session = {"ranked_list_id": ranked_list.id}

        self.assertEqual(
            RankedList.objects.for_request(request).id,
            request.session['ranked_list_id'])


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
    def test_add_note(self):
        self.user = factories.RankedList().owner
        self.client.force_login(self.user)
        self.candidate = overview_factories.Candidate()

        self.user.rankedlist.annotated_candidates.create(candidate=self.candidate, order=1)

        resp = self.client.post(
            reverse("update_note", args=[self.candidate.slug]),
            {"comment": "No Comment"})

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.user.rankedlist.annotated_candidates.get().comment, "No Comment")

    def test_add_note_logged_out(self):
        ranked_list = factories.RankedList(owner=None)

        # everytime you read the client.session, it creates a new one
        session = self.client.session
        session["ranked_list_id"] = ranked_list.id
        session.save()

        self.assertTrue(self.client.session)

        self.candidate = overview_factories.Candidate()

        ranked_list.annotated_candidates.create(candidate=self.candidate, order=1)

        resp = self.client.post(
            reverse("update_note", args=[self.candidate.slug]),
            {"comment": "No Comment"})

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ranked_list.annotated_candidates.get().comment, "No Comment")


class ClaimList(TestCase):
    def test_claim_list(self):
        ranked_list = factories.RankedList(owner=None)
        session = self.client.session
        session["ranked_list_id"] = ranked_list.id
        session.save()

        resp = self.client.post(reverse("registration_register"), {
            "username": "kittens",
            "email": "kittens@example.com",
            "password1": "more cats",
            "password2": "more cats",
        })

        self.assertEqual(resp.status_code, 302)

        ranked_list.refresh_from_db()
        self.assertEqual(int(self.client.session['_auth_user_id']), ranked_list.owner.id)


class DeleteNote(TestCase):

    def test_delete_note(self):
        self.user = factories.RankedList().owner
        self.client.force_login(self.user)
        self.candidate = overview_factories.Candidate()

        self.user.rankedlist.annotated_candidates.create(candidate=self.candidate, order=1)

        resp = self.client.post(reverse("delete_note", args=[self.candidate.slug]))

        self.assertEqual(resp.status_code, 201)
        self.assertFalse(self.user.rankedlist.annotated_candidates.exists())

        self.candidate.refresh_from_db()
        self.assertTrue(self.candidate)
