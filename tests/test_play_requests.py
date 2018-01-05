#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `play_requests` package."""

import os
import pytest


def test_post():
    import requests_mock
    import mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  json={'status': 'ok'})
        mock_engine = mock.MagicMock()
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


def test_get():
    import requests_mock
    import mock
    with requests_mock.mock() as m:
        m.request('GET',
                  'http://something/1',
                  text='OK')
        mock_engine = mock.MagicMock()
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


def test_get_params_simple():
    import requests_mock
    import mock
    with requests_mock.mock() as m:
        m.request('GET',
                  'http://something/1',
                  text='OK')
        mock_engine = mock.MagicMock()
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


def test_get_params_multi():
    import requests_mock
    import re
    import mock
    with requests_mock.mock() as m:
        m.request('GET',
                  'http://something/1',
                  text='OK')
        mock_engine = mock.MagicMock()
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


def test_post_headers():
    import requests_mock
    import mock
    with requests_mock.mock() as m:
        headers = {'user-agent': 'my-app/0.0.1'}
        m.request('POST',
                  'http://something/1',
                  request_headers=headers,
                  json={'status': 'ok'})
        mock_engine = mock.MagicMock()
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
def test_post_files(command):
    import mock
    with mock.patch('play_requests.providers.requests.request') \
            as mock_requests:
        mock_engine = mock.MagicMock()
        mock_engine.variables = {}
        from play_requests import providers
        provider = providers.RequestsProvider(mock_engine)
        assert provider.engine is mock_engine
        provider.command_POST(command)

        assert mock_requests.assert_called_once_with(
            command['type'],
            command['url'],
            files=command['parameters']['files']) is None


def test_post_files_path():
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
            mock_engine = mock.MagicMock()
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


def test_post_default_parameters():
    """ If all of your calls have a set of common parameters
        you can omit them creating some defaults in the
        engine variables
    """
    import requests_mock
    import mock
    with requests_mock.mock() as m:
        headers = {'user-agent': 'my-app/0.0.1'}
        m.request('POST',
                  'http://something/1',
                  request_headers=headers,
                  json={'status': 'ok'})
        mock_engine = mock.MagicMock()
        mock_engine.variables = {
            'play_requests': {
                'parameters': {
                    'headers': headers
                }
            }
        }

        def _parametrize(x):
            from pypom_navigation.parametrizer import Parametrizer
            parametrizer = Parametrizer(mock_engine.variables)
            return parametrizer.parametrize(x)

        mock_engine.parametrizer.parametrize = _parametrize
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


def test_post_default_parameters_parametrized():
    """ If all of your calls have a set of common parameters
        you can omit them creating some defaults in the
        engine variables
    """
    import requests_mock
    import mock
    with requests_mock.mock() as m:
        m.request('POST',
                  'http://something/1',
                  request_headers={
                      'user-agent': 'my-app/0.0.1'},
                  json={'status': 'ok'})
        mock_engine = mock.MagicMock()
        mock_engine.variables = {
            'myapp': 'my-app',
            'play_requests': {
                'parameters': {
                    'headers': {
                        'user-agent': '$myapp/0.0.1'
                    }
                }
            }
        }

        def _parametrize(x):
            from pypom_navigation.parametrizer import Parametrizer
            parametrizer = Parametrizer(mock_engine.variables)
            return parametrizer.parametrize(x)

        mock_engine.parametrizer.parametrize = _parametrize
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
