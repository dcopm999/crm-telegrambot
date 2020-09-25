import logging
from django.conf import settings

from telegrambot import models as telegrambot_models
from products import models as products_models

logger = logging.getLogger(__name__)


class HistoryMixin:
    subscriber_model = telegrambot_models.Subscriber
    request_model = telegrambot_models.Request
    response_model = telegrambot_models.Response
    dialog_model = telegrambot_models.Dialog

    def run(self, request):
        logger.debug('%s: run()', self.__class__)
        self.chat_id = request.get('message').get('from').get('id')
        self.message_from = request.get('message').get('from')
        text_request = request.get('message').get('text')
        text_response = self.get_result()
        subscriber_query = self.subscriber_add(request)
        request_query = self.request_add(subscriber_query, text_request)
        response_query = self.response_add(subscriber_query, text_response)
        self.dialog_add(subscriber_query, request_query, response_query)

    def subscriber_add(self, request):
        try:
            subscriber = self.subscriber_model.objects.get(id=self.chat_id)
        except self.subscriber_model.DoesNotExist as msg:
            logger.exception(msg)
            subscriber = self.subscriber_model(**self.message_from)
            subscriber.save()
            logger.debug(f'{self.__class__}: Created new subscriber {subscriber}')
        else:
            self.subscriber_model.objects.select_for_update().filter(id=self.chat_id).update(**self.message_from)
            logger.debug(f'{self.__class__}: Updated subscriber {subscriber}')
        return subscriber

    def request_add(self, subscriber_query, text_request):
        return self.request_model.objects.create(subscriber=subscriber_query, text=text_request)

    def response_add(self, subscriber_query, text_response):
        return self.response_model.objects.create(subscriber=subscriber_query, text=text_response)

    def dialog_add(self, subscriber_query, request_query, response_query):
        return self.dialog_model.objects.create(subscriber=subscriber_query, request=request_query, response=response_query)


class CatalogMixin:
    def __init__(self):
        self.catalog_model = products_models.Catalog
        super(CatalogMixin, self).__init__()

    def get_product_by_categoty(self, category: str):
        try:
            products = self.catalog_model.objects.get(name=category).product_set.all()
        except self.catalog_model.DoesNotExist as msg:
            logger.exception(msg)
            products = None
        return products

