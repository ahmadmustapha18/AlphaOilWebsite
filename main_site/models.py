
from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class PackSize(models.Model):
	size_display = models.CharField(max_length=20)  # e.g. "1L", "3L"
	volume_ml = models.PositiveIntegerField()

	def __str__(self):
		return self.size_display

class Certification(models.Model):
	name = models.CharField(max_length=100)
	logo = models.ImageField(upload_to='certifications/', blank=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.TextField()
	image = models.ImageField(upload_to='products/')
	certifications = models.ManyToManyField(Certification, blank=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Price(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	pack_size = models.ForeignKey(PackSize, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	is_active = models.BooleanField(default=True)
	effective_from = models.DateField()
	effective_to = models.DateField(null=True, blank=True)

	def __str__(self):
		return f"{self.product} - {self.pack_size}: {self.price}"

class Inventory(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	pack_size = models.ForeignKey(PackSize, on_delete=models.CASCADE)
	stock = models.PositiveIntegerField()
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.product} - {self.pack_size}: {self.stock} in stock"

# Create your models here.
