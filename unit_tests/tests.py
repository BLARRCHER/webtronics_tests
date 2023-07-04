import aiohttp
import asynctest
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def response():
    resp = MagicMock()
    resp.content.aiter.return_value = [b"line 1", b"line 2", b"line 3"]
    return resp

@pytest.fixture
def session(response):
    session = MagicMock()
    session.get.return_value.aenter.return_value = response
    return session

@pytest.fixture
def connector(session):
    connector = MagicMock()
    connector.connect.return_value = session
    return connector

class TestLogs:
    async def test_logs_prints_lines(self, connector):
        cont = "test_cont"
        name = "test_name"

        await logs(cont, name)

        connector.connect.assert_called_once_with(path="/var/run/docker.sock")
        session = aiohttp.ClientSession(connector=connector).return_value.__aenter__.return_value
        session.get.assert_called_once_with("http://xx/containers/test_cont/logs?follow=1&stdout=1")

        assert session.get.return_value.__aenter__.return_value.content.__aiter__.call_count == 1
        assert session.get.return_value.__aenter__.return_value.content.__aiter__.return_value == [b"line 1", b"line 2",
                                                                                                   b"line 3"]

        print_calls = [call for call in asynctest.mock_print.call_args_list if call[0][0] == ("test_name",)]
        assert len(print_calls) == 3
        assert print_calls[0][0][1] == b"line 1"
        assert print_calls[1][0][1] == b"line 2"
        assert print_calls[2][0][1] == b"line 3"
