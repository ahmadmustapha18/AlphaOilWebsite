from django.core.mail import send_mail
def contact(request):
	success = False
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		message = request.POST.get('message')
		# Send email or save to DB (for now, just simulate success)
		# send_mail('Contact Form', f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}', email, ['info@alphacookingoil.com.pk'])
		success = True
	return render(request, 'main_site/contact.html', {'success': success})
def where_to_buy(request):
	return render(request, 'main_site/where_to_buy.html')
from .models import Certification
def certifications(request):
	certifications = Certification.objects.all()
	return render(request, 'main_site/certifications.html', {'certifications': certifications})
from .models import Product
def products(request):
	products = Product.objects.filter(is_active=True)
	return render(request, 'main_site/products.html', {'products': products})
def about(request):
	return render(request, 'main_site/about.html')

from django.shortcuts import render

def home(request):
	return render(request, 'main_site/home.html')

# Create your views here.
