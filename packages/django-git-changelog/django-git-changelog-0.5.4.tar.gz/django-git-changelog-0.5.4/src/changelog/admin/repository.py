from django.contrib import admin
from django.shortcuts import redirect
from ..models import Repository, Branch, ReleaseProfile


class BranchInline(admin.TabularInline):
    model = Branch
    fields = ('name', 'enabled')
    list_fields = ('name', 'enabled')
    readonly_fields = ('name',)
    extra = 0


class ReleaseProfileInline(admin.StackedInline):
    model = ReleaseProfile
    extra = 0
    filter_horizontal = ('recipient_users', 'telegram_chats')


class RepositoryAdmin(admin.ModelAdmin):
    model = Repository
    inlines = [BranchInline, ReleaseProfileInline]

    def response_change(self, request, obj):
        if 'refresh' in request.POST:
            obj.fetch()
            obj.send()
            self.message_user(request, _('Refreshed all Repository objects.'))
            return redirect('admin:changelog_release_change', obj.id)
        return admin.ModelAdmin.response_change(self, request, obj)


admin.site.register(Repository, RepositoryAdmin)
