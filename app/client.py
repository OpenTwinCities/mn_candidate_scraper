from bs4 import BeautifulSoup
# import requests


class SosClient:

    def __init__(self, url):
        self.url = url

    def get_candidate_data(self):
        data_list = [
            {'foo': 'bar', 'biz': 'bang'},
            {'foo': 'foo', 'name': 'John'}
        ]
        keys = set(['foo', 'biz', 'name'])

        return data_list, keys

    def __transform_candidate_page__(self, page):

        def sanitize(container):
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
                name = sanitize(names_columns[col_num])
                value = sanitize(values_columns[col_num].find(['span', 'a']))
                if value:
                    candidate_data[name] = value

        return candidate_data
