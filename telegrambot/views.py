import json
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from telegrambot.handlers import HandlerCommandHelp, HandlerCommandStart


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    http_method_names = ['post']
    handlers = [HandlerCommandHelp, HandlerCommandStart]

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            message = json.loads(request.body)
            handler = self.get_handler()
            handler.handle(message)
            return HttpResponse('ok')

    def get_handler(self):
        for num, item in enumerate(self.handlers):
            if num == 0:
                handler = item()
                before = handler
            else:
                item = item()
                before.set_next(item)
                before = item
        return handler
