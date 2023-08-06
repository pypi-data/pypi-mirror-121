from .client import RichDaddyClient
import typing
from loguru import logger


class RichDaddyMethods:
    
    def __init__(self, client: RichDaddyClient):
        """
        Создание экземпляра
            :param AsyncRichDaddyClient client: объект клиента AsyncRichDaddyClient
        """
        self.client = client

    def usersGet(
        self,
        userIds: typing.List[str] = None,
        userVkIds: typing.List[int] = None,
        fieldsType: typing.Optional[str] = 'mainPublicFields',
        **kwargs: typing.Any) -> dict:
        """
        Получить информацию об определенных пользователях
            :param userIds list(str): Обязательно если не указан userVkIds. Игровые идентификаторы пользователей.
            :param userVkIds list(int): Обязательно если не указан userIds. Идентификаторы пользователей ВК.
            :param fieldsType str: Необязательно. Может содержать:
                - mainPublicFields — По умолчанию. Основные поля пользователей (имя, фамилия, аватарка…)
                - publicFields — Все поля пользователей (скорость клика, капитал бизнесов…)

            :return dict:
        """


        if userIds is None:
            if not list(userVkIds):
                logger.error('"userVkIds" parameter must contain: List')
            return self.client.request("users/get/", {
                'userVkIds': userVkIds,
                'fieldsType': fieldsType
            })
        elif userVkIds is None:
            if not list(userIds):
                logger.error('"userIds" parameter must contain: List')
            return self.client.request("users/get/", {
                'userIds': userIds,
                'fieldsType': fieldsType
            })
        else:
            if userIds != list(userIds) or userVkIds != list(userVkIds):
                logger.error('This parameter must contain: List')
            return self.client.request("users/get/", {
                'userIds': userIds,
                'userVkIds': userVkIds,
                'fieldsType': fieldsType
            })

    def transfersCreate(
            self,
            id: str,
            direction: str = 'Users',
            amount: int = 1000,
            dialog: bool = False,
            title: typing.Optional[str] = None,
            label: typing.Optional[str] = None,
            **kwargs: typing.Any) -> dict:
        """
        Сделать перевод от вашего сервиса к пользователю
            :param id str: Идентификатор пользователя в игре
            :param direction str: Направление. Всегда должен содержать «Users».
            :param amount int: Сумма перевода. Минимум 1000
            :param dialog bool: Необязателен. Объект игрового диалога у пользователя о новом переводе.
            :param title str: Заголовок. От 5 до 35 символов
            :param label str: Описание. От 5 до 200 символов

        :return dict:
        """

        if dialog == True:
            return self.client.request("transfers/create/", {
                'accessToken': self.client.accessToken(),
                'to': [{'id': id,
                        'direction': direction,
                        'amount': amount
                        }],
                'dialog': {
                    'title': title,
                    'label': label
                }
            })

        else:
            return self.client.request("transfers/create/", {
                'accessToken': self.client.accessToken(),
                'to': [{'id': id,
                        'direction': direction,
                        'amount': amount
                        }]

            })

    def transfersGet(
            self,
            skip: typing.Optional[int] = 0,
            limit: typing.Optional[int] = 100,
            **kwargs: typing.Any) -> dict:
        """
        Получить блоки переводов, каждый блок содержит до 100 переводов
            :param skip int: Необязательно. Смещение переводов.
            :param limit int: Необязательно. Лимит блока переводов, максимум 100.

        :return dict:
        """

        return self.client.request("transfers/get/", {
            'accessToken': self.client.accessToken(),
            'skip': skip,
            'limit': limit
        })
