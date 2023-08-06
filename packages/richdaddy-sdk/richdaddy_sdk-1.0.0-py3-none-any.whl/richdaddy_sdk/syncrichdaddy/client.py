import requests
import typing

from loguru import logger

class RichDaddyClient:
    
    def __init__(
            self, 
            access_token: typing.Optional[str] = None,  
            **kwargs: typing.Any):
        """
        :param str access_token: Токен вашего сервиса

        """

        if not access_token: 
            logger.error('Access token is not specifed!')

        self.access_token = access_token

        self.api_url = 'https://richda.dooal.ru/richda/api/{}'

    def accessToken(self,):
        return self.access_token

    def request(
        self,
        method: typing.Optional[str] = None,
        params: typing.Optional[dict] = None,
        **kwargs: typing.Any) -> dict:

        response = requests.post(url=self.api_url.format(method), json=params)

        try:
            response = response.json()
            return response
        except ValueError:
            response = response.text
            logger.error(response)
            return response
