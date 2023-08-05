from django.db import models
from django.utils.translation import gettext_lazy as _
from ..managers import CommitManager
from django.utils.functional import cached_property


class Commit(models.Model):
    id = models.CharField(
        'SHA',
        max_length=40,
        primary_key=True,
    )
    repository = models.ForeignKey(
        'Repository',
        related_name='commits',
        on_delete=models.CASCADE,
    )
    message = models.TextField(
        _('Message'),
    )
    created_at = models.DateTimeField(
        _('Created at')
    )
    hidden = models.BooleanField(
        _('Hidden'),
        default=False,
    )
    sent = models.BooleanField(
        _('Sent'),
        default=False,
    )
    done = models.BooleanField(
        _('Done'),
        default=False,
    )

    objects = CommitManager()

    class Meta:
        ordering = ['-created_at']

    @cached_property
    def commit(self):
        for git_commit in self.repository.repository.iter_commits():
            if git_commit.hexsha == self.id:
                return git_commit

    @property
    def git(self):
        return self.repository.git

    @property
    def head(self):
        return self.message.split('\n', 1)[0]

    @property
    def body(self):
        return self.message.split('\n', 1)[1] if '\n' in self.message else None

    @property
    def stat(self):
        return self.git.show(self.id, stat=True)

    @property
    def details(self):
        return self.git.show(self.id)

    @property
    def files(self):
        return self.git.diff_tree(
            self.id, no_commit_id=True, name_only=True, r=True)

    @property
    def all_files(self):
        return self.git.ls_tree(self.id, name_only=True, r=True,)

    def __str__(self):
        return self.head


class Tag(models.Model):
    commit = models.ForeignKey(
        'Commit',
        on_delete=models.CASCADE,
        related_name='tags',
    )
    name = models.CharField(
        _('Name'),
        max_length=50,
    )
    message = models.TextField(
        _('Message'),
        blank=True, null=True,
    )

    class Meta:
        unique_together = ['commit', 'name']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name
