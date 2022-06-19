import logging

from django.contrib.auth import get_user_model
from products import models as products_models

from telegrambot import models as telegrambot_models

logger = logging.getLogger(__name__)


class HistoryMixin:
    def __init__(self):
        self.user_model = get_user_model()
        self.subscriber_model = telegrambot_models.Subscriber
        self.request_model = telegrambot_models.Request
        self.response_model = telegrambot_models.Response
        self.dialog_model = telegrambot_models.Dialog
        super(HistoryMixin, self).__init__()

    def run(self, request):
        logger.debug("%s: run()", self.__class__)
        if request.get("message", False):
            logger.debug(f"{self.__class__}: is_message")
            self.chat_id = request.get("message").get("from").get("id")
            self.message_from = request.get("message").get("from")
            text_request = request.get("message").get("text")
        elif request.get("callback_query", False):
            self.chat_id = (
                request.get("callback_query").get("message").get("chat").get("id")
            )
            self.message_from = request.get("callback_query").get("from")
            text_request = request.get("callback_query").get("message").get("caption")
        text_response = self.get_result()
        subscriber_query = self.subscriber_add(request)
        request_query = self.request_add(subscriber_query, text_request)
        response_query = self.response_add(subscriber_query, text_response)
        self.dialog_add(subscriber_query, request_query, response_query)

    def subscriber_add(self, request):
        logger.debug(f"{self.__class__}: subscriber_add()")
        username = self.message_from.get("username", f"telegram_{self.chat_id}")
        self.message_from["username"] = username
        if "id" in self.message_from.keys():
            self.message_from.pop("id")

        try:
            subscriber = self.subscriber_model.objects.get(telegram_id=self.chat_id)
        except self.subscriber_model.DoesNotExist:
            logger.debug(
                f"User create: telegram_id={self.chat_id} message_from={self.message_from}"
            )
            user, _ = self.user_model.objects.get_or_create(
                username=self.message_from["username"]
            )
            subscriber = self.subscriber_model(
                user=user,
                telegram_id=self.chat_id,
                name=self.message_from["first_name"],
                is_bot=self.message_from["is_bot"],
            )
            # subscriber = self.subscriber_model(telegram_id=self.chat_id, **self.message_from)
            subscriber.save()
            logger.debug(f"{self.__class__}: Created new subscriber {subscriber}")
        else:
            logger.debug(
                f"User update: telegram_id={self.chat_id} message_from={self.message_from}"
            )
            user, _ = self.user_model.objects.get_or_create(
                username=self.message_from["username"]
            )
            self.subscriber_model.objects.select_for_update().filter(
                telegram_id=self.chat_id
            ).update(
                user=user,
                telegram_id=self.chat_id,
                name=self.message_from["first_name"],
                is_bot=self.message_from["is_bot"],
            )
            logger.debug(f"{self.__class__}: Updated subscriber {subscriber}")
        return subscriber

    def request_add(self, subscriber_query, text_request):
        return self.request_model.objects.create(
            subscriber=subscriber_query, text=text_request
        )

    def response_add(self, subscriber_query, text_response):
        return self.response_model.objects.create(
            subscriber=subscriber_query, text=text_response
        )

    def dialog_add(self, subscriber_query, request_query, response_query):
        return self.dialog_model.objects.create(
            subscriber=subscriber_query, request=request_query, response=response_query
        )


class CatalogMixin:
    def __init__(self):
        self.catalog_model = products_models.Catalog
        self.product_model = products_models.Product
        self.order_model = products_models.Order
        self.user_model = get_user_model()
        super(CatalogMixin, self).__init__()

    def get_product_by_categoty(self, category: str):
        try:
            products = self.catalog_model.objects.get(name=category).product_set.all()
        except self.catalog_model.DoesNotExist:
            products = None
        return products

    def set_product_order(self, chat_id: int, product_id: int):
        user = self.user_model.objects.get(telegram_id=chat_id)
        product = self.product_model.objects.get(id=product_id)
        order = self.order_model(user=user, product=product)
        order.save()
