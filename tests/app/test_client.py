import unittest

from app.client import SosClient


class SosClientTestCase(unittest.TestCase):

    def setUp(self):
        self.candidate_listing_url = 'https://example.com/candidate_listing'
        self.candidate_details_url = 'https://example.com/candidate_details'
        self.client = SosClient(self.candidate_listing_url)

        with open('tests/fixtures/pages/candidate_details.html') as f:
            self.candidate_details_html = f.read()

        with open('tests/fixtures/pages/candidate_missing_details.html') as f:
            self.candidate_missing_details_html = f.read()

    def test___transform_candidate_page__full_details(self):
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
                self.client.__transform_candidate_page__(
                    self.candidate_details_html),
                expected_data)

    def test___transform_candidate_page__missing_details(self):
        expected_data = {
            'Filing Date': '6/05/2018',
            'Name': 'Test Person',
            'Political Party': 'Testing Party',
            'Residence Address': "123 MAIN STREET\nSAINT PAUL, MN 55100",
            'Email': 'test@example.com'
        }

        self.assertEqual(
                self.client.__transform_candidate_page__(
                    self.candidate_missing_details_html),
                expected_data)
