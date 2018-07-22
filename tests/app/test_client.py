import requests_mock
import unittest
from unittest.mock import Mock

from app.client import SosClient


class SosClientTestCase(unittest.TestCase):

    def setUp(self):
        self.candidate_listing_url = 'https://example.com/candidate_listing'
        self.candidate_details_url = 'https://example.com/candidate_details'
        self.client = SosClient(self.candidate_listing_url)
        self.transformed_candidate_listing = [
            ('Contest 1',
             ['ctl00_ContentPlaceHolder1_repOfficeLevel_ctl01_repJurisdiction_ctl00_repOffice_ctl00_repCandidate_ctl01_btnCandidateName']  # noqa
            ),
            ('Contest 2',
             ['ctl00_ContentPlaceHolder1_repOfficeLevel_ctl01_repJurisdiction_ctl00_repOffice_ctl01_repCandidate_ctl01_btnCandidateName',  # noqa

              'ctl00_ContentPlaceHolder1_repOfficeLevel_ctl01_repJurisdiction_ctl00_repOffice_ctl01_repCandidate_ctl02_btnCandidateName',  # noqa

              'ctl00_ContentPlaceHolder1_repOfficeLevel_ctl01_repJurisdiction_ctl00_repOffice_ctl01_repCandidate_ctl03_btnCandidateName']  # noqa

             )
        ]

        with open('tests/fixtures/pages/candidate_listing.html') as f:
            self.candidate_listing_html = f.read()

        with open('tests/fixtures/pages/candidate_details.html') as f:
            self.candidate_details_html = f.read()

        with open('tests/fixtures/pages/candidate_missing_details.html') as f:
            self.candidate_missing_details_html = f.read()

    def test__transform_candidate_detail_page__full_details(self):
        self.maxDiff = None
        expected_data = {
            'Filing Date': '6/05/2018',
            'Name': 'Test Person',
            'Political Party': 'Testing Party',
            'Residence Address': "123 MAIN STREET\nSAINT PAUL, MN 55100",
            'Campaign Address': "123 MAIN STREET\nSAINT PAUL, MN 55100",
            'Candidate Website': 'example.com',
            'Phone Number': '(555) 5555555',
            'Email': 'test@example.com'
        }

        self.assertEqual(
                self.client.transform_candidate_detail_page(
                    self.candidate_details_html),
                expected_data)

    def test__transform_candidate_detail_page__missing_details(self):
        expected_data = {
            'Filing Date': '6/05/2018',
            'Name': 'Test Person',
            'Political Party': 'Testing Party',
            'Residence Address': "123 MAIN STREET\nSAINT PAUL, MN 55100",
            'Email': 'test@example.com'
        }

        self.assertEqual(
                self.client.transform_candidate_detail_page(
                    self.candidate_missing_details_html),
                expected_data)

    @requests_mock.mock()
    def test__fetch_candidate_detail_page(self, mr):
        candidate_id = 'some_Id'

        def match_candidate_id(request):
            # Assert that required data is part of POST and is properly encoded
            return ('__EVENTTARGET=%s' %
                    candidate_id.replace('_', '%24')) in request.text

        mr.post(self.candidate_listing_url,
                additional_matcher=match_candidate_id,
                text=self.candidate_details_html)

        self.assertEqual(
            self.client.fetch_candidate_detail_page(candidate_id),
            self.candidate_details_html
        )

    @requests_mock.mock()
    def test__fetch_candidate_listing_page(self, mr):

        def not_match_candidate_id(request):
            # Assert that candidate identifying data is not part of POST
            return request.text is None or '__EVENTTARGET' not in request.text

        mr.get(self.candidate_listing_url,
               additional_matcher=not_match_candidate_id,
               text=self.candidate_listing_html)

        self.assertEqual(
            self.client.fetch_candidate_listing_page(),
            self.candidate_listing_html
        )

    def test__transform_candidate_listing_page(self):
        expected_data = self.transformed_candidate_listing
        self.assertEqual(
                self.client.transform_candidate_listing_page(
                    self.candidate_listing_html),
                expected_data)

    def test_get_candidate_data(self):
        self.maxDiff = None
        # Mock candidate listing page to return fixture
        self.client.fetch_candidate_listing_page = \
            Mock(return_value=self.candidate_listing_html)
        # Mock candidate listing transformer to return test data
        self.client.transform_candidate_listing_page = \
            Mock(return_value=self.transformed_candidate_listing)
        # Mock candidate details page to be an echo
        self.client.fetch_candidate_detail_page = \
            Mock(side_effect=lambda value: value)
        self.client.transform_candidate_detail_page = \
            Mock(side_effect=lambda value: {'name': value})

        expected_data = [{'name': candidate, 'contest': contest[0]} for contest
                         in self.transformed_candidate_listing
                         for candidate in contest[1]
                         ]
        retval_data, retval_keys = self.client.get_candidates_data()
        self.assertEqual(retval_data, expected_data)
        self.assertEqual(retval_keys, set(['name', 'contest']))
