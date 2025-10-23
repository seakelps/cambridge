from django.test import TestCase
from django.urls import reverse

from . import factories


class SiteMapTest(TestCase):
    def test_sanity(self):
        factories.CandidateElection.create()
        factories.CandidateElection.create(is_running=False)

        resp = self.client.get(reverse("django.contrib.sitemaps.views.sitemap"))
        self.assertEqual(resp.status_code, 200)


class CandidateListTest(TestCase):
    def test_sanity(self):
        election = factories.Election()
        factories.CandidateElection.create(election=election)
        factories.CandidateElection.create(election=election, is_running=False)

        resp = self.client.get(reverse("election_candidates", args=[election.year, election.position]))
        self.assertEqual(resp.status_code, 200)


class BasicListTest(TestCase):
    def test_sanity(self):
        election = factories.Election()
        factories.CandidateElection.create(election=election)
        factories.CandidateElection.create(election=election, is_running=False)

        resp = self.client.get(reverse("basic_comparison", args=[election.year, election.position]))
        self.assertEqual(resp.status_code, 200)


class BikingTest(TestCase):
    def test_sanity(self):
        election = factories.Election()
        factories.CandidateElection.create(election=election)
        factories.CandidateElection.create(election=election, is_running=False)

        resp = self.client.get(reverse("biking_comparison", args=[election.year, election.position]))
        self.assertEqual(resp.status_code, 200)


class SuperintendentTest(TestCase):
    def test_sanity(self):
        election = factories.Election()
        c1 = factories.CandidateElection.create(election=election)
        c2 = factories.CandidateElection.create(election=election, is_running=False)

        prop = factories.SpecificProposal.create(
            fullname="Superintendent: Justice League",
            main_topic="education"
        )

        factories.CandidateSpecificProposalStance.create(
            candidate=c1.candidate,
            specific_proposal=prop,
        )

        resp = self.client.get(reverse("superintendent", args=[election.year, election.position]))
        self.assertEqual(resp.status_code, 200)


class ForumListTest(TestCase):
    def test_sanity(self):
        election = factories.Election(position="school")

        # School Committee Candidates
        c1 = factories.CandidateElection.create(election=election)
        factories.CandidateElection.create(election=election, is_running=False)

        fp1 = factories.ForumParticipant.create(candidate=c1.candidate)

        # City Council Candidates
        c3 = factories.CandidateElection.create(election__position="council")
        fp2 = factories.ForumParticipant.create(candidate=c3.candidate)

        resp = self.client.get(reverse("forum-list", args=[election.year, election.position]))
        self.assertEqual(resp.status_code, 200)
        self.assertInHTML(fp1.forum.name, resp.content.decode())
        self.assertNotInHTML(fp2.forum.name, resp.content.decode())


class WrittenCommentTest(TestCase):
    def test_sanity(self):
        election = factories.Election()
        factories.CandidateElection.create(election=election)
        factories.CandidateElection.create(election=election, is_running=False)

        resp = self.client.get(reverse("written-public-comment", args=[election.year, election.position]))
        self.assertEqual(resp.status_code, 200)


class ByOrganizationTest(TestCase):
    def setUp(self):
        super().setUp()
        self.election = factories.Election()
        factories.CandidateElection.create(election=self.election)
        factories.CandidateElection.create(election=self.election, is_running=False)

    def test_logged_out(self):
        resp = self.client.get(reverse("by-organization", args=[self.election.year, self.election.position]))
        self.assertEqual(resp.status_code, 200)

    def test_logged_in(self):
        user = factories.User.create()
        self.client.force_login(user)

        resp = self.client.get(reverse("by-organization", args=[self.election.year, self.election.position]))
        self.assertEqual(resp.status_code, 200)
