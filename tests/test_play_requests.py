#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `play_requests` package."""

import os
import pytest


@pytest.fixture(scope='session')
def variables():
    return {'skins': {'skin1': {'base_url': 'http://', 'credentials': {}}}}


def test_post1(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'ok'})
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_POST({
            'provider': 'play_requests',
            'type': 'POST',
            'url': 'http://something/1',
            'parameters': {
                'json': {
                    'foo': 'bar',
                    },
                'timeout': 2.5
                 },
        })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5


def test_post_variables(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'ok'})
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_POST({
            'provider': 'play_requests',
            'type': 'POST',
            'url': 'http://something/1',
            'variable': 'myvar',
            'variable_expression': 'response.json()',
            'parameters': {
                'json': {
                    'foo': 'bar',
                    },
                'timeout': 2.5
                 },
        })

        assert 'myvar' in mock_engine.variables
        assert mock_engine.variables['myvar']['status'] == 'ok'
        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5


def test_post_variables_assert(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'ok'})
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_POST({
            'provider': 'play_requests',
            'type': 'POST',
            'url': 'http://something/1',
            'variable': 'myvar',
            'variable_expression': 'response.json()',
            'assertion': 'variables["myvar"]["status"] == "ok"',
            'parameters': {
                'json': {
                    'foo': 'bar',
                    },
                'timeout': 2.5
                 },
        })

        assert 'myvar' in mock_engine.variables
        assert mock_engine.variables['myvar']['status'] == 'ok'
        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5


def test_post_variables_assert_ko(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'KO'})
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        with pytest.raises(AssertionError):
            provider.command_POST({
                'provider': 'play_requests',
                'type': 'POST',
                'url': 'http://something/1',
                'variable': 'myvar',
                'variable_expression': 'response.json()',
                'assertion': 'variables["myvar"]["status"] == "ok"',
                'parameters': {
                    'json': {
                        'foo': 'bar',
                        },
                    'timeout': 2.5
                     },
            })

        assert 'myvar' in mock_engine.variables
        assert mock_engine.variables['myvar']['status'] == 'KO'
        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5


def test_get(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('GET',
                  'http://something/1',
                  text='OK')
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_GET({
            'provider': 'play_requests',
            'type': 'GET',
            'url': 'http://something/1',
            'parameters': {
                'timeout': 2.5
                 },
        })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'GET'
        assert history[0].url == 'http://something/1'
        # mock requests bug
        # assert history[0].text == 'OK'
        assert history[0].timeout == 2.5


def test_no_parameters(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('GET',
                  'http://something/1',
                  text='OK')
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_GET({
            'provider': 'play_requests',
            'type': 'GET',
            'url': 'http://something/1',
        })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'GET'
        assert history[0].url == 'http://something/1'
        # mock requests bug
        # assert history[0].text == 'OK'


def test_get_params_simple(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('GET',
                  'http://something/1',
                  text='OK')
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_GET({
            'provider': 'play_requests',
            'type': 'GET',
            'url': 'http://something/1',
            'parameters': {
                'params': {'foo': 'bar'},
                'timeout': 2.5
                 },
        })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'GET'
        assert history[0].url == 'http://something/1?foo=bar'
        # mock requests bug
        # assert history[0].text == 'OK'
        assert history[0].timeout == 2.5


def test_get_params_multi(play_json):
    import requests_mock
    import re
    with requests_mock.mock() as m:
        m.request('GET',
                  'http://something/1',
                  text='OK')
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_GET({
            'provider': 'play_requests',
            'type': 'GET',
            'url': 'http://something/1',
            'parameters': {
                'params': {'foo': ['bar', 'baz']},
                'timeout': 2.5
                 },
        })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'GET'
        match = re.search(
            r'http\://something/1\?foo=(bar|baz)&foo=(bar|baz)',
            history[0].url)
        foo1 = match.group(1)
        foo2 = match.group(2)
        assert foo1 != foo2
        assert foo1 in ('bar', 'baz')
        assert foo2 in ('bar', 'baz')
        assert history[0].timeout == 2.5


def test_post_headers(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        headers = {'user-agent': 'my-app/0.0.1'}
        m.request('POST',
                  'http://something/1',
                  request_headers=headers,
                  json={'status': 'ok'})
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_POST({
            'provider': 'play_requests',
            'type': 'POST',
            'url': 'http://something/1',
            'parameters': {
                'headers': headers,
                'json': {
                    'foo': 'bar',
                    },
                'timeout': 2.5
                 },
        })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5

        # no headers
        with pytest.raises(requests_mock.exceptions.NoMockAddress):
            provider.command_POST({
                'provider': 'play_requests',
                'type': 'POST',
                'url': 'http://something/1',
                'parameters': {
                    'json': {
                        'foo': 'bar',
                        },
                    'timeout': 2.5
                     },
            })


@pytest.mark.parametrize('command', [
    {'provider': 'play_requests',
     'type': 'POST',
     'url': 'http://something/1',
     'parameters': {
         'files': {
             'filecsv': (
                 'report.csv',
                 'some,data',
                 )
             },
         },
     },
    {'provider': 'play_requests',
     'type': 'POST',
     'url': 'http://something/1',
     'parameters': {
         'files': {
             'filecsv': (
                 'report.csv',
                 'some,data',
                 'application/csv',
                 {'Expires': '0'},
                 )
             },
         },
     },
    {'provider': 'play_requests',
     'type': 'POST',
     'url': 'http://something/1',
     'parameters': {
         'files': {
             'filecsv1': (
                 'report.csv',
                 'some,data',
                 ),
             'filecsv': (
                 'report.csv',
                 'some,data',
                 'application/csv',
                 {'Expires': '0'},
                 )
             },
         },
     },
])
def test_post_files(command, play_json):
    import mock
    with mock.patch('play_requests.providers.requests.request') \
            as mock_requests:
        mock_engine = play_json
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_POST(command)

        assert mock_requests.assert_called_once_with(
            command['type'],
            command['url'],
            files=command['parameters']['files']) is None


def test_post_files_path(play_json):
    file_path = os.path.join(os.path.dirname(__file__), 'file.csv')
    command = {
         'provider': 'play_requests',
         'type': 'POST',
         'url': 'http://something/1',
         'parameters': {
             'files': {
                 'filecsv': (
                     'file.csv',
                     'path:{0}'.format(file_path),
                     )
                 },
             },
         }
    import mock
    with mock.patch('play_requests.providers.requests.request') \
            as mock_requests:
        with mock.patch('play_requests.providers.open') \
                as mock_open:
            file_mock = mock.MagicMock()
            mock_open.return_value = file_mock
            mock_engine = play_json
            mock_engine.variables = {}
            from play_requests import providers
            provider = providers.RequestsProvider(mock_engine)
            assert provider.engine is mock_engine
            provider.command_POST(command)
            assert mock_requests.assert_called_once_with(
                command['type'],
                command['url'],
                files={'filecsv': ('file.csv', file_mock)}) is None
            assert mock_open.assert_called_once_with(
                file_path, 'rb') is None


@pytest.mark.parametrize('assertion', [
    'response.status_code == 200',
    'response.status_code != 404',
    'response.status_code == 200 and response.json()["status"] == "ok"',
    '"status" in response.json()',
    'variables["foo"] == "baz"',
    '"foo" in variables',
    'len([1]) == 1',
    '[1][0] == 1',
    'len(list(response.json().items())) == 1',
    'variables["foo"].upper() == "BAZ"',
    'match(r"^([0-9]*)-data", "123-data")',
    'match(r"^([0-9]*)-data", "123-data").group(1) == "123"'
])
def test_post_assertion(assertion, play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'ok'})
        mock_engine = play_json
        mock_engine.variables = {'foo': 'baz'}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_POST({
            'provider': 'play_requests',
            'type': 'POST',
            'url': 'http://something/1',
            'parameters': {
                'json': {
                    'foo': 'bar',
                    },
                'timeout': 2.5
                 },
            'assertion': assertion
        })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5


def test_post_assertion_ko(play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'ok'})
        mock_engine = play_json
        mock_engine.variables = {'foo': 'baz'}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        with pytest.raises(AssertionError):
            provider.command_POST({
                'provider': 'play_requests',
                'type': 'POST',
                'url': 'http://something/1',
                'parameters': {
                    'json': {
                        'foo': 'bar',
                        },
                    'timeout': 2.5
                     },
                'assertion': 'response.status_code == 404'
            })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5


@pytest.mark.parametrize('assertion', [
    'open("/etc/passwd", "r")',
    'open',
    'import os',
    '__file__',
    '__file__',
    '__builtins__.__dict__["bytes"]',
    '__builtins__.__dict__["bytes"] = "pluto"',
    'prova = lambda: 1',
    'os = 1',
])
def test_post_assertion_bad(assertion, play_json):
    import requests_mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'ok'})
        mock_engine = play_json
        mock_engine.variables = {'foo': 'baz'}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        with pytest.raises(Exception):
            provider.command_POST({
                'provider': 'play_requests',
                'type': 'POST',
                'url': 'http://something/1',
                'parameters': {
                    'json': {
                        'foo': 'bar',
                        },
                    'timeout': 2.5
                     },
                'assertion': assertion
            })

        history = m.request_history
        assert len(history) == 1
        assert history[0].method == 'POST'
        assert history[0].url == 'http://something/1'
        assert history[0].json() == {'foo': 'bar'}
        assert history[0].timeout == 2.5


@pytest.mark.parametrize('verb', [
    'OPTIONS',
    'HEAD',
    'PUT',
    'PATCH',
    'DELETE',
])
def test_other_verbs(verb, play_json):
    """ """
    import mock
    _make_request = mock.MagicMock()
    from play_requests import providers
    provider = providers.RequestsProvider(play_json)
    provider._make_request = _make_request
    command = {'provider': 'play_requests', 'type': verb}
    getattr(provider, 'command_{0}'.format(verb))(command, foo='bar')
    assert _make_request.assert_called_once_with(verb, command) is None
