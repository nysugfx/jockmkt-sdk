from unittest import mock, main, TestCase
import pytest
import requests
import sys
import json
from datetime import datetime, timedelta
sys.path.insert(1, 'src/jockmkt_sdk')
import client

authorization_res = json.load(open('./test_resources/authorization.json'))
account_activity_res = json.load(open('./test_resources/account_activity.json'))
entities_res = json.load(open('./test_resources/entities.json'))
entry_res = json.load(open('./test_resources/entry.json'))
event_res = json.load(open('./test_resources/event.json'))
events_res = json.load(open('./test_resources/events.json'))
game_logs_res = json.load(open('./test_resources/game_logs.json'))
games_res = json.load(open('./test_resources/games.json'))
orders_res = json.load(open('./test_resources/orders.json'))
position_res = json.load(open('./test_resources/position.json'))
place_order_res = json.load(open('./test_resources/order_place.json'))


_test_api_key = "jm_key_xxx"
_test_secret_key = "xxx"

_test_auth_token = 'eyXXX'
_test_auth_expiration1 = round(datetime.now().timestamp()*1000)
_test_auth_expiration2 = round(((datetime.now().timestamp()) + 2592000)*1000)
_test_auth_expired = round((datetime.now().timestamp()-3600)*1000)

mock_auth_header = {'Authorization': f'Bearer {_test_auth_token}'}
# GIVEN: BASE LAYER INFO
# WHEN:
# THEN:

class TestClient(TestCase):
    mock_init = client.Client(_test_secret_key, _test_api_key)

    def test_build_auth_token(self):
        _test_bearer_object = f'Bearer {_test_auth_token}'
        test_header = self.mock_init._build_auth_header(_test_auth_token)
        self.assertEqual(test_header['Authorization'], _test_bearer_object)

    @mock.patch("client.requests.post")
    def test_get_auth_token(self, get_auth_token_mock):
        mock_auth_response = mock.Mock(status_code=200)
        mock_auth_response.json.return_value = authorization_res
        get_auth_token_mock.return_value = mock_auth_response

        mock_key_map = f'{_test_api_key}:{_test_secret_key}'
        mock_auth_request = self.mock_init._get_auth_token()

        mock_auth_dict = {'token': mock_auth_response.json()['token']['access_token'],
                          'expired_at': mock_auth_response.json()['token']['expired_at']}
        self.assertEqual(mock_auth_request, _test_auth_token)
        self.assertIn(mock_key_map, self.mock_init._AUTH_TOKEN_MAP)
        self.assertEqual(self.mock_init._AUTH_TOKEN_MAP[mock_key_map], mock_auth_dict)

    @mock.patch("client.requests")
    def test_requests(self, request_mock):
        pass

    @mock.patch("client._requests")
    @mock.patch("client.requests.post")
    def test_place_order(self, place_order_mock, _requests_mock):
        mock_auth_response = mock.Mock(status_code=200)
        mock_auth_response.json.return_value = place_order_res

        place_order_mock.return_value = mock_auth_response
        mock_order_place = self.mock_init.place_order('tdbl_xxx', price=10, side='buy', phase='ipo', quantity=10)
        self.assertEqual(mock_order_place, place_order_mock)
        # assert mock_order_place == place_order_mock


class ClientTest(TestCase):
    pass
