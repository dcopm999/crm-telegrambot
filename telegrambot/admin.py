# -*- coding: utf-8 -*-
from django.contrib import admin

from telegrambot import models


@admin.register(models.Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'request', 'response', 'created']
    date_hierarchy = 'created'
    readonly_fields = ['subscriber', 'request', 'response']
