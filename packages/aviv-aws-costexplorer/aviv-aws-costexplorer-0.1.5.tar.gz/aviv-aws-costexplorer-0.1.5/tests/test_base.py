import pytest
from boto3 import (
    session
)
from botocore import (
    exceptions,
    client
)

from aviv_aws_costexplorer import base


@pytest.fixture
def aacli():
    return base.AWSClient()


def test_awsclient(aacli):
    assert isinstance(aacli, base.AWSClient)

    assert isinstance(aacli.sts, client.BaseClient)
    aid = None
    with pytest.raises((exceptions.NoCredentialsError, exceptions.UnauthorizedSSOTokenError)):
        aid = aacli.account_id()
    if not aid:
        return
    assert isinstance(aid, str)
    assert isinstance(aacli.client('ce'), client.BaseClient)
    assert isinstance(aacli.session(), session.Session)


def test_sts_credentials(aacli):
    creds = base.AWSClient.sts_credentials(dict(
        Credentials={
            'AccessKeyId': 'abc',
            'SecretAccessKey': 'def',
            'SessionToken': 'ghi'
        }
    ))
    assert 'aws_access_key_id' in creds
    assert 'aws_secret_access_key' in creds
    assert 'aws_session_token' in creds
    with pytest.raises(KeyError):
        base.AWSClient.sts_credentials({})
