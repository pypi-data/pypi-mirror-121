from . import client, methods
import typing

class AsyncPaperScroll:

    def __init__(
            self,
            access_token: typing.Optional[str] = None,
            merchant_id: typing.Optional[int] = None,
            **kwargs: typing.Any):
        """
        :param str access_token: Токен вашего магазина
        :param int merchant_id: Идентификатор вашего магазина
        """

        self.access_token = access_token
        self.merchant_id = merchant_id

        self.client = client.AsyncPaperScrollClient(access_token, merchant_id)
        self.api = methods.PaperScrollMethods(self.client)

    def getApi(self):
        return self.api
    
    def getClient(self):
        return self.client