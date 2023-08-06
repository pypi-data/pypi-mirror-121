from .client import AsyncPaperScrollClient
import asyncio
import typing

class PaperScrollMethods:

    def __init__(self, client: AsyncPaperScrollClient):
        """
        Создание экземпляра
        :param AsyncPaperScrollClient client: объект клиента AsyncPaperScrollClient
        """
        self.client = client

    async def getMerchants(
        self, merchant_ids: list = []) -> dict:
        """
        Возвращает информацию о магазинах по их идентификаторам
        :param list merchant_ids: ID магазинов, не больше 100 элементов. По умолчанию — идентификатор текущего магазина.
        :return dict:
        """
        return await self.client.request("merchants.get", {
            'merchant_ids': merchant_ids
        })

    async def editMerchant(
        self, newMerchantObject: dict) -> dict:
        """
        Редактирует информацию о текущем магазине
        :param dict newMerchantObject: Объект мерчанта, состоящий из name, group_id, avatar
        :return dict:
        """
        return await self.client.request("merchants.edit", newMerchantObject)

    async def getUsers(
        self, user_ids: list) -> dict:
        """
        Возвращает информацию о пользователях по их идентификаторам
        :param list user_ids: ID пользователей, не больше 100 элементов. Если профиль пользователя ещё не был создан в приложении, то объекта с его данными в ответе не будет.
        :return dict:
        """
        return await self.client.request("users.get", {
            'user_ids': user_ids
        })

    async def getUsersBalances(
        self, user_ids: list) -> dict:
        """
        Возвращает информацию о балансах пользователей по их идентификаторам
        :param list user_ids: ID пользователей, не больше 250 элементов
        :return dict:
        """
        return await self.client.request("users.getBalances", {
            'user_ids': user_ids
        })

    async def createTransfer(
        self, transferObject: dict) -> dict:
        """
        Запускает выполнение нового перевода
        :param dict transferObject: объект перевода состоящий из peer_id, object_type, object_type_id, amount
        :return dict:
        """
        return await self.client.request("transfers.create", transferObject)

    async def getTransfers(
        self, transfer_ids: list) -> dict:
        """
        Возвращает список переводов по их идентификаторам
        :param list transfer_ids: ID пользователей, не больше 100 элементов. Если профиль пользователя ещё не был создан в приложении, то объекта с его данными в ответе не будет.
        :return dict:
        """
        return await self.client.request("transfers.get", {
            'transfer_ids': transfer_ids
        })

    async def getHistoryTransfers(
        self, offset: typing.Optional[int] = 0, limit: typing.Optional[int] = 50) -> dict:
        """
        Возвращает список последних переводов
        :param int offset: Смещение относительно первого найденного перевода
        :param int limit: Количество возвращаемых переводов, не больше 250 элементов.
        :return dict:
        """
        return await self.client.request("transfers.getHistory", {
            'offset': offset,
            'limit': limit
        })

    async def getDisinfectantsStorage(self) -> dict:
        """
        Возвращает информацию об имеющихся средствах защиты в инвентаре
        :return dict:
        """
        return await self.client.request("storage.getDisinfectants", {})

    async def getItemsStorage(self) -> dict:
        """
        Возвращает информацию об имеющихся предметах в инвентаре
        :return dict:
        """
        return await self.client.request("storage.getItems", {})

    async def getWebhook(self) -> dict:
        """
        Возвращает информацию о текущем установленном сервере или ошибку при его отсутствии
        :return dict:
        """
        return await self.client.request("webhooks.get", {})

    async def createWebhook(
        self, url: typing.Optional[str], events: list) -> dict:
        """
        Настраивает Webhook для отправки уведомлений о событиях
        :param str url: URL для отправки уведомлений
        :param list events: Типы отправляемых событий на сервер
        :return dict:
        """
        return await self.client.request("webhooks.create", {
            'url': url,
            'events': events
        })

    async def deleteWebhook(self) -> dict:
        """
        Удялает текущий используемый сервер
        :return dict:
        """
        return await self.client.request("webhooks.delete", {})

    async def getLogsWebhook(self) -> dict:
        """
        Возвращает информацию о последних 20 ошибках при отправке событий
        :return dict:
        """
        return await self.client.request("webhooks.getLogs", {})

    async def callMethod(
        self, method: typing.Optional[str], params: dict) -> dict:
        """
        Вызывает кастомный метод с апи, при необходимости
        :param str method: Метод апи
        :param dict params: Параметры метода
        :return dict:
        """
        return await self.client.request(method, params)
