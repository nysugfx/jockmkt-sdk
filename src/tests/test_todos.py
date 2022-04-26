from unittest import mock, main, TestCase
import pytest
import requests
import sys
sys.path.insert(1, '/Users/alexfriedman/Documents/jockmkt-sdk/src/jockmkt_sdk')
import client


_test_api_key = "jm_key_xxx"
_test_secret_key = "xxx"

_test_auth_token = 'eyXXX'
_test_auth_expiration1 = 1653587495000
_test_auth_expiration2 = 1650995495000


def test_build_auth_token():
    _test_bearer_object = f'Bearer {_test_auth_token}'
    test_header = client.Client()._build_auth_header(_test_auth_token)
    assert 'Authorization' in test_header
    assert test_header['Authorization'] == _test_bearer_object


@mock.patch("client.requests.post")
def test_get_auth_token(get_auth_header_mock):
    mock_auth_response = mock.Mock(status_code=200)
    mock_auth_response.json.return_value = {
        'status': 'success',
        'token': {
            'access_token': _test_auth_token,
            'object': 'session',
            'created_at': _test_auth_expiration1,
            'expired_at': _test_auth_expiration2
        }
    }
    get_auth_header_mock.return_value = mock_auth_response
    print(get_auth_header_mock)

    mock_key_map = f'{_test_api_key}:{_test_secret_key}'

    mock_init = client.Client(_test_secret_key, _test_api_key)
    mock_auth_request = mock_init._get_auth_token()

    mock_auth_dict = {'token': mock_auth_response.json()['token']['access_token'],
                      'expired_at': mock_auth_response.json()['token']['expired_at']}

    assert mock_auth_request == _test_auth_token
    assert mock_key_map in mock_init._AUTH_TOKEN_MAP
    assert mock_init._AUTH_TOKEN_MAP[mock_key_map] == mock_auth_dict





