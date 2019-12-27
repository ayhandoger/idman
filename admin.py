"""
from django.contrib import admin
from .models import Innovator, Idea

# Register your models here.

# class InnovatorInline(admin.StackedInline):
# 	model = Innovator
# extra = 3

class IdeaAdmin(admin.ModelAdmin):
	fieldsets = [
		((None, 			 {'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
		]
	
#    inlines = [InnovatorInline]

	admin.site.register(Idea, IdeaAdmin)
"""
	
from django.contrib import admin
from .models import Innovator, Idea

class InnovatorInline(admin.TabularInline):
	model = Innovator
	extra = 3

class IdeaAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['idea_text']}),
		('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	list_display = ('idea_text', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['idea_text']
	
	inlines = [InnovatorInline]
	
admin.site.register(Idea, IdeaAdmin)