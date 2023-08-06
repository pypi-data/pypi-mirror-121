from subprocess import check_output
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from git.cmd import Git
from git.repo.base import Repo
from ..models import Commit, Tag
from ..managers import BranchManager
from ..decorators import start_new_thread


class Repository(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=50,
        unique=True,
    )
    path = models.CharField(
        _('Path'),
        max_length=150,
        unique=True,
        blank=True,
        help_text=_('Basedir if blank'),
    )

    class Meta:
        verbose_name = _('Repository')
        verbose_name_plural = _('Repositories')

    @cached_property
    def repository(self):
        return Repo(path=self.path)

    @cached_property
    def git(self):
        return Git(self.path)

    def get_version(self):
        version = check_output(['python', f'{self.path}/setup.py', '--version'])
        return version.decode('utf-8').strip()

    def clean(self):
        if not self.path:
            self.path = settings.BASE_DIR
        if not str(self.path).startswith('/'):
            self.path = f'{settings.BASE_DIR}/{self.path}'
        super().clean()

    def fetch(self):
        self.repository.remote().fetch()

    def refresh_tags(self):
        for tag in self.repository.tags:
            Tag.objects.get_or_create(
                commit_id=tag.commit.hexsha,
                name=tag.name,
            )

    def refresh(self):
        disabled_branches = [branch.name for branch in self.branches.all()
                             if branch.enabled==False]
        for git_branch in self.repository.branches:
            if git_branch.name not in disabled_branches:
                branch = Branch.objects.get_or_create(
                    repository = self,
                    name=git_branch.name,
                )[0]
                commits = []
                for git_commit in self.repository.iter_commits(git_branch.name):
                    commit, updated = Commit.objects.update_or_create(
                        id=git_commit.hexsha,
                        repository=self,
                        defaults={
                            'message': git_commit.message,
                            'created_at': git_commit.committed_datetime,
                        }
                    )
                    commits.append(commit)
                branch.commits.set(commits)
        self.refresh_tags()

    def __str__(self):
        return self.name


@receiver(post_save, sender=Repository, dispatch_uid="update_stock_count")
def refresh_on_save(instance, **kwargs):
    instance.refresh()


class Branch(models.Model):
    repository = models.ForeignKey(
        'Repository',
        related_name='branches',
        on_delete=models.CASCADE,
    )
    commits = models.ManyToManyField(
        'Commit',
        related_name='branches',
        blank=True,
    )
    name = models.CharField(
        _('Name'),
        max_length=50,
    )
    enabled = models.BooleanField(
        _('Enabled'),
        default=True,
    )

    objects = BranchManager()

    class Meta:
        unique_together = ['repository', 'name']
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')

    def __str__(self):
        return f'{self.repository.name}: {self.name}'
