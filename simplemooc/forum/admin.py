from django.contrib import admin

from .models import Thread , Reply
# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'created', 'modified']
	search_fields = ['title', 'author__email'] #autor é uma fk/ outro model, para filtrar usamos o __ para ir no email
	prepopulated_fields = { 'slug': ('title',)}

class ReplyAdmin(admin.ModelAdmin):
	list_display = ['thread', 'author', 'created', 'modified']
	search_fields = ['thread__title', 'reply', 'author__email']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
