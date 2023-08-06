import attr

from benchling_api_client.benchling_client import AuthorizationMethod


@attr.s(auto_attribs=True)
class ClientCredentialsOAuth2(AuthorizationMethod):
    """
    OAuth2 client credentials for authorization.

    Use in combination with the Benchling() client constructor to be authorized with OAuth2 client_credentials grant
    type.

    :param client_id: Client id in client_credentials grant type
    :param client_secret: Client secret in client_credentials grant type
    :param token_url: A fully-qualified URL pointing at the access token request endpoint such as
                      https://benchling.com/api/v2/token
    """

    client_id: str
    client_secret: str
    token_url: str

    def get_authorization_header(self) -> str:
        """Get OAuth2 content for a HTTP Authorization header."""
        raise NotImplementedError
