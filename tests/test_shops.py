from http import client as http

from flask import json

from tests import MakershopTestCase


class CreateShopTestCase(MakershopTestCase):
    def setUp(self):
        super(CreateShopTestCase, self).setUp()
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

    def test_make_shop(self):
        r = self.client.post(
            '/shop/create/',
            data={
                'name': 'Test Shop'
            }
        )

        self.assertEqual(http.OK, r.status_code)

        msg = json.loads(r.data)

        self.assertIsNotNone(msg.get('id'))


class ViewShopTestCase(MakershopTestCase):
    def setUp(self):
        super(ViewShopTestCase, self).setUp()
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
                'username': 'foo@bar.com',
                'password': 'asdfasdf',
            }
        )

        # make shop
        self.client.post(
            '/shop/create/',
            data={
                'name': 'Test Shop'
            }
        )

    def test_name(self):
        r = self.client.get('/shop/1/')

        self.assertEqual(
            {
                'name': 'Test Shop',
                'id': 1
            },
            json.loads(r.data),
        )