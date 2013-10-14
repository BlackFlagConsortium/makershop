from http import client as http

from flask import json
from nose.tools import *

from tests import MakershopTestCase


class ProductTestCase(MakershopTestCase):
    def setUp(self):
        super(ProductTestCase, self).setUp()
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


class CreateProductTestCase(ProductTestCase):

    def test_status_code(self):
        assert_equal(http.CREATED, self.r.status_code)

    def test_redirect_location(self):
        assert_equal(
            'http://localhost/shop/1/product/1/',
            self.r.headers.get('Location'),
        )

    def test_return_dict(self):
        assert_equal(
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


class UpdateProductTestCase(ProductTestCase):
    def setUp(self):
        super(UpdateProductTestCase, self).setUp()
        self.update_response = self.client.put(
            self.r.headers.get('Location'),
            data={
                'title': 'Changed Title',
                'base_price': 150,
                'description': 'Changed Description',
                'visible': 1,
            }
        )

        self.get_response = self.client.get(self.r.headers.get('Location'))

    expected_dict = {
        'id': 1,
        'shop_id': 1,
        'title': 'Changed Title',
        'base_price': 150,
        'description': 'Changed Description',
        'visible': True,
    }

    def test_put_status_code(self):
        assert_equal(http.OK, self.update_response.status_code)

    def test_put_dict(self):
        assert_equal(
            self.expected_dict,
            json.loads(self.update_response.data)
        )

    def test_get_dict(self):
        print(self.get_response.data)
        assert_equal(
            self.expected_dict,
            json.loads(self.get_response.data)
        )
