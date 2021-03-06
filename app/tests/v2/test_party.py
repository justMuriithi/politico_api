from .base_test import Base


class TestParty(Base):

    def setUp(self):
        super().setUp()

        self.party = {
            "name": "Kanu",
            "hqaddress": "Eldoret"
        }
    # clear all lists after tests

    def tearDown(self):
        super().tearDown()

    def test_create_party(self):
        res = self.client.post('/api/v2/parties', json=self.party,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(
            data['message'], 'Your political party was created successfully')
        self.assertEqual(res.status_code, 201)

    def test_create_party_name_exists(self):
        res = self.client.post('/api/v2/parties', json=self.party,
                               headers=self.headers)
        res = self.client.post('/api/v2/parties', json=self.party,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 409)
        self.assertEqual(data['message'], 'Party already exists')
        self.assertEqual(res.status_code, 409)

    def test_create_party_missing_fields(self):
        res = self.client.post('/api/v2/parties', json={
            "hqaddress": "Eldoret"
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_party_no_data(self):
        res = self.client.post('/api/v2/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_get_parties(self):
        res = self.client.post('/api/v2/parties', json=self.party,
                               headers=self.headers)
        self.party['name'] = 'One name'
        res = self.client.post('/api/v2/parties', json=self.party,
                               headers=self.headers)
        self.party['name'] = 'Another name'
        res = self.client.get('/api/v2/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(res.status_code, 200)

    def test_get_parties_no_data(self):
        res = self.client.get('/api/v2/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    def test_get_party(self):
        self.client.post('/api/v2/parties', json=self.party,
                         headers=self.headers)

        res = self.client.get('/api/v2/parties/1',
                              headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_party_id_not_found(self):
        res = self.client.get('/api/v2/parties/35', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Party not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)

    def test_edit_party(self):
        self.client.post('/api/v2/parties', json=self.party,
                         headers=self.headers)

        res = self.client.patch('/api/v2/parties/1/name', json={
                "name": "PNU"
            }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'PNU updated successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(data['data'][0]['name'], 'Kanu')
        self.assertEqual(res.status_code, 200)

    def test_edit_party_id_not_found(self):
        res = self.client.get('/api/v2/parties/35', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Party not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)

    def test_delete_party(self):
        self.client.post('/api/v2/parties', json=self.party,
                         headers=self.headers)

        res = self.client.delete('/api/v2/parties/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Kanu deleted successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_party_id_not_found(self):
        res = self.client.get('/api/v2/parties/35', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Party not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)
