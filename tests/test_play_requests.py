#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `play_requests` package."""


def test_post():
    from play_requests import providers
    provider = providers.RequestsProvider(None)
    assert provider.engine is None
    provider.command_post({
        'provider': 'play_requests',
        'type': 'post',
        'url': 'http://something/1',
        'parameters': {
            'json': {
                'foo': 'bar',
                },
            'timeout': 2.5
             },
    })
