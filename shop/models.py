
from django.db import models

class Customer(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Address(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	address_line = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	province = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	is_primary = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.address_line}, {self.city}"

class PaymentMethod(models.Model):
	name = models.CharField(max_length=50)  # e.g. "Cash on Delivery"
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=[
		('pending', 'Pending'),
		('confirmed', 'Confirmed'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
	], default='pending')
	payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	whatsapp_order = models.BooleanField(default=False)
	tracking_code = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return f"Order {self.id} - {self.customer.name}"

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey('main_site.Product', on_delete=models.CASCADE)
	pack_size = models.ForeignKey('main_site.PackSize', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return f"{self.product} ({self.pack_size}) x {self.quantity}"

# Create your models here.
