import asyncio
import aiohttp
import base64, typing

from loguru import logger
from .exceptions import NotImplementedError, ApiError

class AsyncPaperScrollClient:

    def __init__(
            self, 
            access_token: typing.Optional[str] = None, 
            merchant_id: typing.Optional[int] = None, 
            **kwargs: typing.Any):
        """
        :param str access_token: Токен вашего магазина
        :param int merchant_id: Идентификатор вашего магазина
        """

        if not access_token: 
            logger.error('Access token is not specifed!')
            raise NotImplementedError("Access token is not specified")

        if not merchant_id: 
            logger.error('Merchant ID is not specifed!')
            raise NotImplementedError("Merchant ID is not specified")

        self.access_token = access_token
        self.merchant_id = merchant_id

        self.token = base64.b64encode(
            f'{merchant_id}:{access_token}'.encode()).decode()
        self.api_url = 'https://paper-scroll.ru/api/{}'

    async def request(
        self, 
        method: typing.Optional[str] = None,
        params: typing.Optional[dict] = None,
        **kwargs: typing.Any
    ) -> dict: 
        async with aiohttp.ClientSession() as session, session.request('POST', 
            url = self.api_url.format(method), 
            json = params, 
            headers = {'Authorization': 'Basic {}'.format(self.token)}) as response:

                response = await response.json()

                if 'error' in response:
                    text_error=f"{response['error']['error_msg']} ({response['error']['error_code']}) - {response['error']['error_text']}"                    
                    logger.error(text_error)
                    raise ApiError(response['error']['error_code'],
                                   response['error']['error_msg'],
                                   response['error']['error_text'])

                return response['response']


                




            
        
