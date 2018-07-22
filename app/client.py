from bs4 import BeautifulSoup
import requests


class SosClient:

    def __init__(self, url):
        self.url = url

    def get_candidates_data(self):
        candidates_data = []
        keys = set()
        listing_page = self.fetch_candidate_listing_page()
        contests_data = self.transform_candidate_listing_page(listing_page)
        for contest in contests_data:
            contest_candidates = []
            for candidate_id in contest[1]:
                candidate_page = self.fetch_candidate_detail_page(candidate_id)
                candidate_data = self \
                    .transform_candidate_detail_page(candidate_page)
                candidate_data['contest'] = contest[0]
                contest_candidates.append(candidate_data)
                keys.update(list(candidate_data.keys()))

            candidates_data.extend(contest_candidates)

        return candidates_data, keys

    def fetch_candidate_listing_page(self):
        response = requests.get(self.url)

        if response.status_code == requests.codes.ok:
            return response.text

        return None

    def transform_candidate_listing_page(self, page):
        def is_heading_row(tag):
            return (tag.name == 'tr' and
                    tag.get('style') == 'height:30px;')

        def is_candidate_row(tag):
            return (tag.name == 'tr' and
                    any(class_ in ['evenRow', 'oddRow']
                        for class_ in tag.get('class', [])
                        )
                    )

        def contest_row_matcher(tag):
            return is_heading_row or is_candidate_row

        def extract_contest_name(tag):
            return tag.select('td span')[0].text

        def extract_candidate_id(tag):
            return tag.select('td a')[0].get('id')

        retval = []
        soup = BeautifulSoup(page, 'html.parser')
        contest_rows = soup.select('table[width=700px]')[0] \
                           .find_all(contest_row_matcher)

        for row in contest_rows:
            if is_heading_row(row):
                retval.append((extract_contest_name(row), []))
            elif is_candidate_row(row):
                retval[-1][1].append(extract_candidate_id(row))

        return retval

    def fetch_candidate_detail_page(self, candidate_id):
        request_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/xml;q=0.9'
        }
        response = requests.post(
                self.url,
                headers=request_headers,
                data={'__EVENTTARGET': candidate_id.replace('_', '$')}
        )

        if response.status_code == requests.codes.ok:
            return response.text

        return None

    def transform_candidate_detail_page(self, page):
        def extract(container):
            if not container:
                return None

            retval = container.get_text("\n")

            if retval:
                retval = retval.strip()

            return retval if retval else None

        candidate_data = {}
        soup = BeautifulSoup(page, 'html.parser')
        table_rows = soup.select('table[width=758]')[0].find_all('tr')

        # Structure of this table:
        # Row 0: Home link
        # Row 1: Empty
        # Row 2: Header and Filing Date
        # Row 3: Empty
        # Row 4+: 3 Row Groupings where
        #   Row 1: 2 Attribute names
        #   Row 2: 2 Attribute values
        #   Rows 3: Empty
        candidate_data['Filing Date'] = table_rows[2].find('span').string
        for row_num in range(4, len(table_rows), 3):
            names_columns = table_rows[row_num].find_all('td')
            values_columns = table_rows[row_num + 1].find_all('td')
            for col_num in range(len(names_columns)):
                name = extract(names_columns[col_num])
                value = extract(values_columns[col_num].find(['span', 'a']))
                if value:
                    candidate_data[name] = value
                    if name == 'Name':
                        print(value)

        return candidate_data
