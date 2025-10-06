import unittest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from overview import factories as overview_factories
from . import factories
from .models import RankedList


class GetList(TestCase):
    def setUp(self):
        super().setUp()
        self.election = overview_factories.Election.create()

    @unittest.expectedFailure
    def test_logged_in_no_list(self):
        request = RequestFactory().get("/")
        request.user = overview_factories.User()
        request.session = {}

        self.assertEqual(
            RankedList.objects.for_request(
                request,
                force=True,
                election=self.election,
            ), request.user.rankedlist
        )

    def test_logged_in_with_list(self):
        request = RequestFactory().get("/")
        ranked_list = factories.RankedList.create()
        request.user = ranked_list.owner
        request.session = {}

        self.assertEqual(
            RankedList.objects.for_request(
                request,
                force=True,
                election=self.election
            ),
            ranked_list
        )

    def test_logged_out_no_list(self):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        request.session = {}

        ranked_list = RankedList.objects.for_request(request, force=True, election=self.election)
        self.assertTrue(ranked_list)
        self.assertEqual(ranked_list.id, request.session["ranked_list_id"])

    def test_logged_out_with_list(self):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()

        ranked_list = factories.RankedList(owner=None, election=self.election)
        request.session = {"ranked_list_id": ranked_list.id}

        self.assertEqual(
            RankedList.objects.for_request(request, force=True, election=self.election).id,
            request.session["ranked_list_id"],
        )


class OverwriteListTest(TestCase):
    def test_swap(self):
        c1, c2, c3 = overview_factories.CandidateElection.create_batch(3)

        ranked_list = factories.RankedList.create()

        ranked_list.annotated_candidates.overwrite_list([c1, c2, c3])
        ranked_list.annotated_candidates.overwrite_list([c3, c1, c2])


class MyListTest(TestCase):
    fixtures = ["current_elections"]

    def setUp(self):
        super().setUp()
        self.user = overview_factories.User()
        self.client.force_login(self.user)

        self.council_url = reverse("my_ranking", args=[settings.ELECTION_DATE.year, "council"])
        self.school_url = reverse("my_ranking", args=[settings.ELECTION_DATE.year, "school"])

    def test_create_list(self):
        resp = self.client.get(self.council_url)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(self.user.rankedlist_set.count(), 1)

        resp = self.client.get(self.school_url)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(self.user.rankedlist_set.count(), 2)

    def test_save_candidate(self):
        self.client.get(self.council_url)
        candidate = overview_factories.CandidateElection()

        resp = self.client.post(self.council_url, {"candidates": candidate.candidate.slug})
        self.assertEqual(resp.status_code, 302)

        council_list = self.user.rankedlist_set.get(election__position="council")
        self.assertTrue(council_list.annotated_candidates.all())

    def test_view_list(self):
        factories.RankedElement.create(
            ranked_list__owner=self.user,
            ranked_list__election__position="council"
        )
        self.client.get(self.council_url)

    def test_overwrite(self):
        self.client.get(self.council_url)

        council_list = self.user.rankedlist_set.get(election__position="council")
        council_list.annotated_candidates.create(
            order=1, candidate=overview_factories.CandidateElection()
        )

        candidate = overview_factories.CandidateElection()

        resp = self.client.post(self.council_url, {"candidates": candidate.candidate.slug})
        self.assertEqual(resp.status_code, 302)

        self.assertTrue(council_list.annotated_candidates.get().candidate, candidate)

    def test_keep_comment(self):
        self.client.get(self.council_url)

        candidate1, candidate2 = overview_factories.CandidateElection.create_batch(2)

        council_list = self.user.rankedlist_set.get(election__position="council")
        council_list.annotated_candidates.create(
            order=1, comment="My spoon is too big", candidate=candidate1
        )

        resp = self.client.post(
            self.council_url, {"candidates": ",".join([candidate2.candidate.slug, candidate1.candidate.slug])}
        )
        self.assertEqual(resp.status_code, 302)

        ranking1, ranking2 = council_list.annotated_candidates.all()

        self.assertEqual(ranking1.candidate, candidate2)
        self.assertFalse(ranking1.comment)

        self.assertEqual(ranking2.candidate, candidate1)
        self.assertEqual(ranking2.comment, "My spoon is too big")


class UpdateNotes(TestCase):
    def test_add_note(self):
        self.user = factories.RankedList().owner
        self.client.force_login(self.user)
        self.candidate = overview_factories.CandidateElection()

        self.user.rankedlist.annotated_candidates.create(candidate=self.candidate, order=1)

        resp = self.client.post(
            reverse("update_note", args=[self.candidate.candidate.slug]), {"comment": "No Comment"}
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.user.rankedlist.annotated_candidates.get().comment, "No Comment")

    def test_add_note_logged_out(self):
        ranked_list = factories.RankedList(owner=None)

        # everytime you read the client.session, it creates a new one
        session = self.client.session
        session["ranked_list_id"] = ranked_list.id
        session.save()

        self.assertTrue(self.client.session)

        self.candidate = overview_factories.CandidateElection()

        ranked_list.annotated_candidates.create(candidate=self.candidate, order=1)

        resp = self.client.post(
            reverse("update_note", args=[self.candidate.candidate.slug]), {"comment": "No Comment"}
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ranked_list.annotated_candidates.get().comment, "No Comment")


class ClaimList(TestCase):
    def test_claim_list(self):
        ranked_list = factories.RankedList(owner=None)
        session = self.client.session
        session["ranked_list_id"] = ranked_list.id
        session.save()

        resp = self.client.post(
            reverse("django_registration_register"),
            {
                "username": "kittens",
                "email": "kittens@example.com",
                "password1": "more cats",
                "password2": "more cats",
            },
        )

        self.assertEqual(resp.status_code, 302)

        ranked_list.refresh_from_db()
        self.assertIn("kittens", ranked_list.name)
        self.assertIn("kittens", ranked_list.slug)
        self.assertEqual(int(self.client.session["_auth_user_id"]), ranked_list.owner.id)


class DeleteNote(TestCase):

    def test_delete_note(self):
        self.user = factories.RankedList().owner
        self.client.force_login(self.user)
        self.candidate = overview_factories.CandidateElection()

        self.user.rankedlist.annotated_candidates.create(candidate=self.candidate, order=1)

        resp = self.client.post(reverse("delete_note", args=[self.candidate.candidate.slug]))

        self.assertEqual(resp.status_code, 201)
        self.assertFalse(self.user.rankedlist.annotated_candidates.exists())

        self.candidate.refresh_from_db()
        self.assertTrue(self.candidate)


class AppendToList(TestCase):
    def test_append(self):
        user = factories.RankedList().owner
        self.client.force_login(user)

        candidate0 = overview_factories.CandidateElection(is_running=True)
        candidate1 = overview_factories.CandidateElection(is_running=True)

        self.client.post(reverse("append_to_ballot", args=[candidate0.candidate.slug]))
        self.client.post(reverse("append_to_ballot", args=[candidate1.candidate.slug]))

        self.assertEqual(user.rankedlist.annotated_candidates.get(order=0).candidate, candidate0)
        self.assertEqual(user.rankedlist.annotated_candidates.get(order=1).candidate, candidate1)

    def test_append_not_running(self):
        user = factories.RankedList().owner
        self.client.force_login(user)

        candidate = overview_factories.CandidateElection(is_running=False)
        self.client.post(reverse("append_to_ballot", args=[candidate.candidate.slug]))

        self.assertFalse(user.rankedlist.annotated_candidates.count())


class MakePublic(TestCase):
    def test_make_public(self):
        ranked_list = factories.RankedList(public=False)
        self.client.force_login(ranked_list.owner)
        self.client.post(reverse("make_public"), {"public": True})

        ranked_list.refresh_from_db()
        self.assertTrue(ranked_list.public)

    def test_make_private(self):
        ranked_list = factories.RankedList(public=True)
        self.client.force_login(ranked_list.owner)
        self.client.post(reverse("make_public"), {"public": False})

        ranked_list.refresh_from_db()
        self.assertFalse(ranked_list.public)


class MakeOrdered(TestCase):
    def test_make_ordered(self):
        ranked_list = factories.RankedList(ordered=False)
        self.client.force_login(ranked_list.owner)
        self.client.post(reverse("make_ordered"), {"ordered": True})

        ranked_list.refresh_from_db()
        self.assertTrue(ranked_list.ordered)

    def test_make_private(self):
        ranked_list = factories.RankedList(ordered=True)
        self.client.force_login(ranked_list.owner)
        self.client.post(reverse("make_ordered"), {"ordered": False})

        ranked_list.refresh_from_db()
        self.assertFalse(ranked_list.ordered)
