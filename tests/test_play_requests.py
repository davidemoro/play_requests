#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `play_requests` package."""


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
        provider.command_POST({
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
