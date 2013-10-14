from http import client as http

from flask import json

from tests import MakershopTestCase


class CreateProductCase(MakershopTestCase):
    def setUp(self):
        super(CreateProductCase, self).setUp()
        self.client = self.app.test_client(use_cookies=True)

        # register
        self.client.post(
            '/user/register/',
            data={
                'email': 'foo@bar.com',
                'password': 'asdfasdf',
                'name': 'Test User',
            }
        )

        # login
        self.client.post(
            '/user/login/',
            data={
                'email': 'foo@bar.com',
                'password': 'asdfasdf',
            }
        )

        # make a shop
        self.shop = json.loads(
            self.client.post(
                '/shop/create/',
                data={
                    'name': 'Test Shop'
                }
            ).data
        )

        self.r = self.client.post(
            '/shop/{}/product/'.format(self.shop['id']),
            data={
                'title': 'Test Product'
            }
        )

    def test_status_code(self):
        self.assertEqual(http.CREATED, self.r.status_code)

    def test_redirect_location(self):
        self.assertEqual(
            'http://localhost/shop/1/product/1/',
            self.r.headers.get('Location'),
        )

    def test_return_dict(self):
        self.assertEqual(
            {
                'id': 1,
                'shop_id': 1,
                'title': 'Test Product',
                'base_price': None,
                'description': None,
                'visible': False,
            },
            json.loads(self.r.data)
        )