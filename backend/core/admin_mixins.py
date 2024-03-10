from django.contrib import admin


class ModelAdminElementsWidthMixIn(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(__class__, self).get_form(request, obj, **kwargs)
        for field in form.base_fields:
            form.base_fields[field].widget.attrs['style'] = 'width: 90%'

        return form
