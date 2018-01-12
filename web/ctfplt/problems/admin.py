from django.contrib import admin
from .models import Problem, Tag

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'score')

#admin.site.register(Problem)
admin.site.register(Tag)
admin.site.register(Problem, ProblemAdmin)
