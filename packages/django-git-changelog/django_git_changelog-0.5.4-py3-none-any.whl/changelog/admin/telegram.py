from django.contrib import admin
from changelog.models import TelegramBot, TelegramChat


class TelegramChatInline(admin.TabularInline):
    model = TelegramChat
    extra = 0
    

class TelegramBotAdmin(admin.ModelAdmin):
    model = TelegramBot
    inlines = [TelegramChatInline]


admin.site.register(TelegramBot, TelegramBotAdmin)
