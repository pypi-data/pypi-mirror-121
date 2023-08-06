from . import client, methods
import typing


class RichDaddy:

    def __init__(
            self,
            access_token: typing.Optional[str] = None,
            **kwargs: typing.Any):
        """
        :param str access_token: Токен вашего сервиса
        """

        self.access_token = access_token

        self.client = client.RichDaddyClient(access_token)
        self.api = methods.RichDaddyMethods(self.client)

    def getApi(self):
        return self.api

    def getClient(self):
        return self.client
