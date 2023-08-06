import datetime as dt

import pytest

from siti.exc import InvalidCredentials
from siti.http import Session


@pytest.mark.vcr
def test_invalid_auth():
    session = Session()
    with pytest.raises(InvalidCredentials) as e:
        session.configure(
            consumer_key='wrong', consumer_secret='creds', demo=True
        )
    assert (
        e.value.desc
        == 'A valid OAuth client could not be found for client_id: wrong'
    )


@pytest.mark.vcr
def test_expired_token():
    session = Session()
    session.configure(demo=True)
    session.oauth_token.expires_at = dt.datetime(2020, 10, 22)
    assert session.oauth_token.is_expired
    session.configure(demo=True)
    assert not session.oauth_token.is_expired
