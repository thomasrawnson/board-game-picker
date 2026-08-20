from bgg.client import BGGClient


def test_bgg_client_can_be_created():
    client = BGGClient()

    assert client.timeout == 30.0
    assert client.max_retries == 5