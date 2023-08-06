from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.utils.timezone import now
from telegram.error import TimedOut
from ..decorators import start_new_thread

User = get_user_model()


class Release(models.Model):
    repository = models.ForeignKey(
        'Repository',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=20,
        editable=False,
        blank=True,
    )
    text = models.TextField(
        _('Text'),
        blank=True, null=True,
    )
    commits = models.ManyToManyField(
        'Commit',
        blank=True,
        related_name='releases',
    )
    telegram_chats = models.ManyToManyField(
        'TelegramChat',
        blank=True,
        related_name='releases',
    )
    email_recipient_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='releases',
    )
    sent_at = models.DateTimeField(
        _('Sent at'),
        editable=False,
        blank=True, null=True,
    )

    class Meta:
        unique_together = ('repository', 'version')
        verbose_name = _('Release')
        verbose_name_plural = _('Release')

    @classmethod
    def from_profile(cls, profile):
        repository = profile.repository
        release, created = cls.objects.get_or_create(
            repository=repository,
            version=repository.get_version(),
            defaults={
                'text': profile.text
            }
        )
        if created:
            release.email_recipient_users.set(profile.recipient_users.all())
            release.telegram_chats.set(profile.telegram_chats.all())
        return release

    def clean(self):
        if not self.version:
            self.version = self.repository.get_version()
        super().clean()

    def get_context(self):
        return {'release': self, }

    def send_telegram_message(self, bot,  chat_id, text, **kwargs):
        try:
            bot.send_message(chat_id=chat_id, text=text, parse_mode='html')
        except TimedOut:
            pass

    @start_new_thread
    def send_telegram(self):
        ctx = self.get_context()
        for chat in self.telegram_chats.all():
            bot = chat.telegram_bot.bot
            first_ctx = {**ctx, 'text': self.text}
            rendered = get_template('changelog/telegram_first.html'
                                    ).render(first_ctx)
            self.send_telegram_message(bot, chat.id, rendered)
            for commit in self.commits.all():
                commit_ctx = {**ctx, 'commit': commit}
                rendered = get_template('changelog/telegram.html'
                                        ).render(commit_ctx)
                self.send_telegram_message(bot, chat.id, rendered)

    @start_new_thread
    def send_email(self):
        ctx = self.get_context()
        recipients = [f'{user.get_full_name()} <{user.email}>' for user
                      in self.email_recipient_users.all()]
        subject = get_template('changelog/subject.txt').render(ctx)
        subject = subject.replace("\n", "").replace("\r", "")
        body = get_template('changelog/email.txt').render(ctx)
        html = get_template('changelog/email.html').render(ctx)
        email = EmailMultiAlternatives(
                subject,
                body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients,
                # attachments=content_attachments,
            )
        email.attach_alternative(html, "text/html")
        email.send()

    def send(self):
        if self.sent_at and not settings.DEBUG:
            return
        self.commits.update(sent=True, hidden=True)
        self.send_telegram()
        self.send_email()
        self.sent_at = now()
        self.save()

    def __str__(self):
        result = self.repository.name
        if self.version:
            result += f' ver. {self.version}'
        return result


class ReleaseAttachment(models.Model):
    release = models.ForeignKey(
        'Release',
        related_name='attachments',
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        _('File'),
    )

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')


class ReleaseProfile(models.Model):
    repository = models.ForeignKey(
        'Repository',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        _('Profile name'),
        max_length=50,
        unique=True,
    )
    text = models.TextField(
        _('Text'),
        blank=True, null=True,
    )
    recipient_users = models.ManyToManyField(
        User,
        related_name='release_profiles',
        blank=True,
    )
    telegram_chats = models.ManyToManyField(
        'TelegramChat',
        related_name='release_profiles',
        blank=True,
    )

    class Meta:
        unique_together = ('name', 'repository')
        verbose_name = _('Release Profile')
        verbose_name_plural = _('Release Profiles')

    def __str__(self):
        return self.name
