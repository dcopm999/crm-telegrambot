import logging
from telegrambot import models

logger = logging.getLogger(__name__)


class HistoryMixin:
    subscriber_model = models.Subscriber
    request_model = models.Request
    response_model = models.Response
    dialog_model = models.Dialog

    def run(self, request):
        logger.debug('%s: run()', self.__class__)
        text_request = request.get('message').get('text')
        text_response = self.get_result()
        subscriber_query = self.subscriber_add(request)
        request_query = self.request_add(subscriber_query, text_request)
        response_query = self.response_add(subscriber_query, text_response)
        self.dialog_add(subscriber_query, request_query, response_query)

    def subscriber_add(self, request):
        subscriber, result =  self.subscriber_model.objects.update_or_create(**request.get('message').get('from'))
        if result:
            logger.debug('%s: run() Subscriber %s created' % (self.__class__, subscriber))
        else:
            logger.debug('%s: run() Subscriber %s updated' % (self.__class__, subscriber))
        return subscriber

    def request_add(self, subscriber_query, text_request):
        return self.request_model.objects.create(subscriber=subscriber_query, text=text_request)

    def response_add(self, subscriber_query, text_response):
        return self.response_model.objects.create(subscriber=subscriber_query, text=text_response)

    def dialog_add(self, subscriber_query, request_query, response_query):
        return self.dialog_model.objects.create(subscriber=subscriber_query, request=request_query, response=response_query)
