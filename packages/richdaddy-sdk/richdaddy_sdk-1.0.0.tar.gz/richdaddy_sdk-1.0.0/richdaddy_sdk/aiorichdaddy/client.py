import asyncio
import aiohttp
import typing, json

from loguru import logger


class AsyncRichDaddyClient:

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


    async def request(
        self, 
        method: typing.Optional[str] = None,
        params: typing.Optional[dict] = None,
        **kwargs: typing.Any) -> dict:
        
        async with aiohttp.ClientSession() as session, session.request('POST',
            url=self.api_url.format(method),json=params) as response:
            
            try:
                response = await response.json(content_type=None)
                return response
            except ValueError:
                response = await response.text()
                logger.error(response)
                return response

