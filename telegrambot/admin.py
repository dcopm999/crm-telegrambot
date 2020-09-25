# -*- coding: utf-8 -*-
from django.contrib import admin

from telegrambot import models


@admin.register(models.Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'request', 'response', 'created']
    date_hierarchy = 'created'
    readonly_fields = ['subscriber', 'request', 'response']


class DialogInline(admin.StackedInline):
    model  = models.Dialog
    readonly_fields = ['subscriber', 'created', 'request', 'response']


@admin.register(models.Subscriber)
class SubsciberAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'is_bot', 'language_code']
    list_filter = ['is_bot', 'language_code']
    search_fields = ['id', 'first_name']
    date_hierarchy = 'created'
    inlines = [DialogInline]
