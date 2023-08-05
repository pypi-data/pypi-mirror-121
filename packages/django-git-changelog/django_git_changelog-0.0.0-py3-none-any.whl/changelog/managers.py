from django.db import models


class CommitManager(models.Manager):
    def enabled(self):
        return self.get_queryset().filter(branches__enabled=True).distinct()


class BranchManager(models.Manager):
    def enabled(self):
        return self.get_queryset().filter(enabled=True)
