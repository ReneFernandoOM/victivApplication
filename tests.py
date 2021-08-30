import unittest

from app import create_app

class ApiDistanceEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.api_endpoint = '/api/distance_to_mkad'

    def test_address_outside_ring(self):
        params = {'address': 'Malecon, La Paz, Baja California Sur'}
        response = self.client.get(self.api_endpoint, query_string=params)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()['data']), 0)

    def test_address_inside_ring(self):
        address = 'Russia, Moscow, Москва, округ Обручевский, 117198, Улица Академика Опарина'
        params = {'address': address}
        response = self.client.get(self.api_endpoint, query_string=params)
        data = response.get_json()['data']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[address]['distance'], 'This address is inside the Moscow Ring Road')

    def test_wrong_adress(self):
        address = 'ajlkfdjal'
        params = {'address': address}
        response = self.client.get(self.api_endpoint, query_string=params)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], 'Address not found.')

    def test_no_address(self):
        response = self.client.get(self.api_endpoint)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], 'You must provide an address')

if __name__ == "__main__":
    unittest.main()