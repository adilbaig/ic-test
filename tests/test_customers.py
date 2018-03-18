import unittest
from library.customers import *


class CustomersTestCase(unittest.TestCase):

    def _get_customer_array(self):
        return [
            '{"latitude": "51.8856167", "user_id": 2, "name": "Ian McArdle", "longitude": "-10.4240951"}',
            '{"latitude": "51.92893", "user_id": 1, "name": "Alice Cahill", "longitude": "-10.27699"}',
            '{"latitude": "52.986375", "user_id": 12, "name": "Christina McArdle", "longitude": "-6.043701"}',
            '{"user_id": 3, "name": "Test User", "latitude": 1}',  # Missing key
            '{"user_id": 4, "name": "Test User", "latitude": "A string", "longitude": 2}',  # Incorrect type of value
            '{}',  # Missing data
            '{blah}',  # Bad JSON
        ]

    def test_customer_list(self):
        """
        Ensure erroneous customer records are caught

        :return:
        """
        arr = [
            {'user_id': 1, 'name': 'Test User', 'latitude': 1, 'longitude': 2},
            {'user_id': 2, 'name': 'Test User', 'latitude': 1, 'longitude': 2},
            {'user_id': 3, 'name': 'Test User', 'latitude': 1},
            {'user_id': 4, 'name': 'Test User', 'latitude': 'A string', 'longitude': 2},
            {},
        ]

        self.assertIsNone(validate_row(arr[0]))
        self.assertIsNone(validate_row(arr[1]))

        with self.assertRaises(AttributeError):
            validate_row(arr[2])

        with self.assertRaises(AttributeError):
            validate_row(arr[4])

        with self.assertRaises(ValueError):
            validate_row(arr[3])

    def test_customer_list_load(self):
        """
        Ensure erroneous customer records are filtered out on load and distance is calculated
        :return:
        """
        arr = self._get_customer_array()
        customers = process_rows(arr)

        # Ensure bad results are filtered out
        self.assertEqual(len(customers), 3)

        # Ensure distance is calculated
        for c in customers:
            self.assertTrue('distance_hq' in c)

        # Ensure rows are ordered by distance
        self.assertEqual(customers[0]['user_id'], 12)
        self.assertEqual(customers[1]['user_id'], 1)
        self.assertEqual(customers[2]['user_id'], 2)
        self.assertEqual(round(customers[0]['distance_hq'], 3), 41.815)
        self.assertEqual(round(customers[1]['distance_hq'], 3), 313.6)
        self.assertEqual(round(customers[2]['distance_hq'], 3), 324.731)

    def test_find(self):
        """
        Check if `load_customers` and `find` works!

        :return:
        """
        arr = self._get_customer_array()
        customers = process_rows(arr)

        # Find should return values sorted by user_id
        ret = find(customers, 320)
        self.assertEqual(ret[0]['user_id'], 1)
        self.assertEqual(ret[1]['user_id'], 12)
