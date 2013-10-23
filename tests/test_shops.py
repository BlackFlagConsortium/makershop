from http import client as http

from flask import json, session
from nose.tools import *

from tests import MakershopTestCase, UserLoggedIn


class ViewShopTestCase(UserLoggedIn):
    def setUp(self):
        super(ViewShopTestCase, self).setUp()

        # make shop
        self.client.post(
            '/shop/create/',
            data={
                'name': 'Test Shop'
            }
        )

    def test_name(self):
        r = self.client.get('/shop/1/')

        assert_equal(
            {
                'name': 'Test Shop',
                'id': 1
            },
            json.loads(r.data),
        )