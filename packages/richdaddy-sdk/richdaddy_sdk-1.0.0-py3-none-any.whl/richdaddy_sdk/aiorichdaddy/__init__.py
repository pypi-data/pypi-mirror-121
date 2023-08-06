from . import client, methods
import typing


class AsyncRichDaddy:

    def __init__(
            self,
            access_token: typing.Optional[str] = None,
            **kwargs: typing.Any):
        """
        :param str access_token: Токен вашего сервиса
        """

        self.access_token = access_token

        self.client = client.AsyncRichDaddyClient(access_token)
        self.api = methods.ARichDaddyMethods(self.client)

    def getApi(self):
        return self.api

    def getClient(self):
        return self.client
