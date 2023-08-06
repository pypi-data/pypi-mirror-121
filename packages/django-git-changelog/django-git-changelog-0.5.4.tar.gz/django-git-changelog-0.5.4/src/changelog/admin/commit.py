from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from ..models import Commit, Tag, Branch, Release, ReleaseProfile


class BranchFilter(admin.SimpleListFilter):
    title = _('Branches')
    parameter_name = 'branches'

    def lookups(self, request, model_admin):
        for branch in Branch.objects.enabled().select_related('repository'):
            yield (branch.id, str(branch))

    def queryset(self, request, queryset):
        return queryset.filter(id__in=Commit.objects.enabled())


class TagInline(admin.TabularInline):
    model = Tag
    readonly_fields = ('commit', 'name', 'message')


class CommitAdmin(admin.ModelAdmin):
    change_form_template = 'admin/commit_change_form.html'
    model = Commit
    list_display = ('head', 'body', 'created_at', 'sent', 'hidden')
    list_filter = ('created_at', 'hidden', 'sent', BranchFilter,
                   'releases')
    readonly_fields = ('id', 'message')
    fields = readonly_fields
    search_fields = (
        'id', 'message', 'tags__name', 'tags__message', 'releases__version',
        'releases__email_recipient_users__email',
        'releases__messages__telegram_text',
        'releases__messages__email_subject',
        'releases__messages__email_text',
        'releases__messages__email_html',
    )
    actions = ['hide', 'unhide']

    def get_queryset(self, request):
        return Commit.objects.enabled()

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = {}
        for profile in ReleaseProfile.objects.all():
            func = self.__class__.add_to_release
            actions[str(profile)] = (
                func,
                str(profile),
                f'{func.short_description}: {profile}',
            )
        return actions

    @admin.display(description=_('Tags'))
    def get_tags_str(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    @admin.action(description=_('Add to release'))
    def add_to_release(self, request, queryset):
        profile = ReleaseProfile.objects.get(name=request.POST['action'])
        repository = profile.repository
        commits = queryset.filter(branches__repository=repository)
        release = Release.from_profile(profile)
        release.commits.add(*commits)
        return redirect('admin:changelog_release_change', release.id)

    @admin.action(description=_('Hide selected'))
    def done(self, request, queryset):
        queryset.update(done=True)

    @admin.action(description=_('Unhide selected'))
    def undone(self, request, queryset):
        queryset.update(done=False)


admin.site.register(Commit, CommitAdmin)
