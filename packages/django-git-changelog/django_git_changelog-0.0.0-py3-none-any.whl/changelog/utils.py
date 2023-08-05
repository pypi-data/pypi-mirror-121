from django.utils.functional import cached_property
from .models import Repository


class Changelog:
    @cached_property
    def repositories(self):
        return Repository.objects.all()

    def fetch(self):
        for repo in self.repositories:
            repo.fetch()

    def refresh(self):
        for repo in self.repositories:
            repo.refresh()
