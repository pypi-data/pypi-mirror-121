from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from telegram.bot import Bot


class TelegramBot(models.Model):
    id = models.CharField(
        _('Token'),
        max_length=250,
        help_text=_('eg. 123456789:QwErtzuIoPpjHgHlkhKGkjlHLhjLhlK-749'),
        primary_key=True
    )

    class Meta:
        verbose_name = _('Telegram bot')
        verbose_name_plural = _('Telegram bots')

    @cached_property
    def bot(self):
        return Bot(token=self.id)

    def __str__(self):
        return self.bot.name


class TelegramChat(models.Model):
    class Type(models.TextChoices):
        PRIVATE = 'private', _('Private')
        GROUP = 'group', _('Group')
        SUPERGROUP = 'supergroup', _('Supergroup')
        CHANNEL = 'channel', _('Channel')

    id = models.BigIntegerField(
        _('Chat ID'),
        primary_key=True,
    )
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=10, choices=Type.choices)

    class Meta:
        verbose_name = _('Telegram chat')
        verbose_name_plural = _('Telegram chats')

    @cached_property
    def chat(self):
        return self.telegram_bot.bot.get_chat(self.id)

    def __str__(self):
        return self.chat.title
