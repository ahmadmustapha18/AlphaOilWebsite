
from django.contrib import admin
from .models import PageContent, LanguageContent

class LanguageContentInline(admin.TabularInline):
	model = LanguageContent
	extra = 0

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
	list_display = ("page", "section", "content_type", "is_active")
	inlines = [LanguageContentInline]

@admin.register(LanguageContent)
class LanguageContentAdmin(admin.ModelAdmin):
	list_display = ("page_content", "language")

# Register your models here.
