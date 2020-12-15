from django.contrib import admin

# Register your models here.
from cheaters.models import Report, Entry


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    # HACK for django admin
    # Any changes here should also be applied in Model save method.
    def save_related(self, request, form, formsets, change):
        super(EntryAdmin, self).save_related(request, form, formsets, change)
        if not change:
            form.instance.parent = form.instance
            form.instance.save()
            if form.instance.report.last is not None and form.instance.report.last.get_parent() != form.instance.get_parent():
                form.instance.merge(form.instance.report.last)
                form.instance.neighbours.add(form.instance.report.last)

            neighbours = Entry.objects.filter(key=form.instance.key, value=form.instance.value)
            for neighbour in neighbours.all():
                if form.instance.get_parent() != neighbour.get_parent() and form.instance != neighbour:
                    form.instance.merge(neighbour)
                    form.instance.neighbours.add(neighbour)

            form.instance.report.last = form.instance
            form.instance.report.save()
            form.instance.save()
