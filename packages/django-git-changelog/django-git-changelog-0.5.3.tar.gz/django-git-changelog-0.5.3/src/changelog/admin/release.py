from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.conf import settings
from ..models import Release, ReleaseAttachment


class ReleaseAttachmentInline(admin.TabularInline):
    model = ReleaseAttachment
    extra = 0


class ReleaseAdmin(admin.ModelAdmin):
    change_form_template = 'admin/release_change_form.html'
    model = Release
    inlines = [ReleaseAttachmentInline]
    readonly_fields = ('sent_at', 'version',)
    filter_horizontal = ('commits', 'email_recipient_users', 'telegram_chats')
    fieldsets = (
        (None, {
            'fields': ('repository', 'version', 'text', 'sent_at',)
        }),
        (_('Linked objects'), {
            'classes': ('collapse',),
            'fields': filter_horizontal,
        }),
    )

    def has_change_permission(self, request, obj=None):
        return (obj and obj.sent_at == None) or settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return (obj and obj.sent_at == None) or settings.DEBUG

    def change_view(self, request, object_id, extra_context=None, *args,
                    **kwargs):
        extra_context = extra_context or {}
        obj = self.model.objects.get(id=object_id)
        extra_context['send_button_enabled'] = self.has_change_permission(
            request, obj
        )
        return super().change_view(
            request, object_id, extra_context=extra_context
        )

    def response_change(self, request, obj):
        if 'send' in request.POST:
            obj.save()
            result = obj.send()
            if result:
                self.message_user(request, _('E-Mail was sent.'))
            return redirect('admin:changelog_release_change', obj.id)
        return admin.ModelAdmin.response_change(self, request, obj)


admin.site.register(Release, ReleaseAdmin)
