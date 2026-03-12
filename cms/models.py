
from django.db import models

class PageContent(models.Model):
	page = models.CharField(max_length=100)  # e.g. "home", "about", "contact"
	section = models.CharField(max_length=100)  # e.g. "hero", "mission"
	content_type = models.CharField(max_length=20, choices=[('text', 'Text'), ('html', 'HTML')])
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.page} - {self.section}"

class LanguageContent(models.Model):
	page_content = models.ForeignKey(PageContent, on_delete=models.CASCADE)
	language = models.CharField(max_length=10, choices=[('en', 'English'), ('ur', 'Urdu')])
	content = models.TextField()

	def __str__(self):
		return f"{self.page_content} ({self.language})"

# Create your models here.
