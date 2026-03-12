from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from main_site.models import Product, PackSize, Price
from .models import Customer, Address, PaymentMethod, Order, OrderItem
import random
import string
from urllib.parse import quote
from django.core.mail import send_mail
from django.conf import settings


def product_list(request):
	products = Product.objects.filter(is_active=True)
	return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug, is_active=True)
	if request.method == 'POST':
		pack_size_id = request.POST.get('pack_size')
		quantity = int(request.POST.get('quantity', 1))
		cart = request.session.get('cart', {})
		key = f"{product.id}_{pack_size_id}"
		if key in cart:
			cart[key]['quantity'] += quantity
		else:
			cart[key] = {
				'product_id': product.id,
				'pack_size_id': int(pack_size_id),
				'quantity': quantity,
			}
		request.session['cart'] = cart
		return redirect('shop:cart')
	return render(request, 'shop/product_detail.html', {'product': product})


def get_cart(request):
	cart = request.session.get('cart', {})
	items = []
	total = 0
	for key, item in cart.items():
		try:
			product = Product.objects.get(id=item['product_id'])
			pack_size = PackSize.objects.get(id=item['pack_size_id'])
			price = Price.objects.get(product=product, pack_size=pack_size, is_active=True)
			quantity = item['quantity']
			item_total = price.price * quantity
			items.append({
				'id': key,
				'product': product,
				'pack_size': pack_size,
				'price': price.price,
				'quantity': quantity,
				'total': item_total,
			})
			total += item_total
		except Exception:
			continue
	return {
		'items': items,
		'total': total,
		'remaining_for_free': max(0, 2000 - total),
	}


def cart(request):
	cart = request.session.get('cart', {})
	if request.method == 'POST':
		if 'remove' in request.POST:
			remove_id = request.POST['remove']
			if remove_id in cart:
				del cart[remove_id]
		else:
			for key in cart.keys():
				qty = request.POST.get(f'quantity_{key}')
				if qty:
					cart[key]['quantity'] = int(qty)
		request.session['cart'] = cart
		return redirect('shop:cart')
	cart_data = get_cart(request)
	return render(request, 'shop/cart.html', {'cart': cart_data})


def checkout(request):
	cart_data = get_cart(request)
	if not cart_data['items']:
		return redirect('shop:cart')
	if request.method == 'POST':
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		address_line = request.POST.get('address')
		city = request.POST.get('city')
		province = request.POST.get('province')
		payment_method = PaymentMethod.objects.filter(name__iexact='Cash on Delivery').first()
		whatsapp_order = bool(request.POST.get('whatsapp_order'))

		customer, _ = Customer.objects.get_or_create(phone=phone, defaults={'name': name})
		address = Address.objects.create(
			customer=customer,
			address_line=address_line,
			city=city,
			province=province,
			postal_code='',
			is_primary=True
		)
		tracking_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
		order = Order.objects.create(
			customer=customer,
			address=address,
			status='pending',
			payment_method=payment_method,
			total_amount=cart_data['total'],
			whatsapp_order=whatsapp_order,
			tracking_code=tracking_code,
		)
		for item in cart_data['items']:
			OrderItem.objects.create(
				order=order,
				product=item['product'],
				pack_size=item['pack_size'],
				quantity=item['quantity'],
				price=item['price'],
			)
		request.session['cart'] = {}

		# Send order notification email
		try:
			items_text = '\n'.join([f"  • {item['product'].name} ({item['pack_size'].size_display}) × {item['quantity']} = Rs.{int(item['total'])}" for item in cart_data['items']])
			email_body = f"""New Order Received!\n
Order #{tracking_code}
Customer: {name}
Phone: {phone}
Address: {address_line}, {city}, {province}

Items:
{items_text}

Total: Rs.{int(cart_data['total'])}
Payment: Cash on Delivery
WhatsApp Order: {'Yes' if whatsapp_order else 'No'}

Manage this order at: /admin/shop/order/
"""
			send_mail(
				f'New Order #{tracking_code} — Rs.{int(cart_data["total"])}',
				email_body,
				settings.DEFAULT_FROM_EMAIL,
				[settings.EMAIL_HOST_USER],
				fail_silently=True,
			)
		except Exception:
			pass  # Email not configured yet

		# If WhatsApp order, redirect to WhatsApp with order details
		if whatsapp_order:
			msg_lines = [
				f"🛒 *New Order — Alpha Oil & Ghee*",
				f"📋 Order: #{tracking_code}",
				f"👤 Name: {name}",
				f"📞 Phone: {phone}",
				f"📍 Address: {address_line}, {city}, {province}",
				f"",
				f"*Items:*",
			]
			for item in cart_data['items']:
				msg_lines.append(f"• {item['product'].name} ({item['pack_size'].size_display}) × {item['quantity']} = Rs.{int(item['total'])}")
			msg_lines.append(f"")
			msg_lines.append(f"💰 *Total: Rs.{int(cart_data['total'])}*")
			msg_lines.append(f"💳 Payment: Cash on Delivery")
			wa_msg = quote('\n'.join(msg_lines))
			request.session['whatsapp_url'] = f"https://wa.me/923019730869?text={wa_msg}"

		return redirect('shop:order_confirmation', tracking_code=tracking_code)
	return render(request, 'shop/checkout.html', {'cart': cart_data})


def order_confirmation(request, tracking_code):
	whatsapp_url = request.session.pop('whatsapp_url', None)
	return render(request, 'shop/order_confirmation.html', {
		'tracking_code': tracking_code,
		'whatsapp_url': whatsapp_url,
	})


def order_status(request):
	order = None
	searched = False
	tracking_code = request.GET.get('tracking_code')
	if tracking_code:
		searched = True
		try:
			order = Order.objects.get(tracking_code=tracking_code)
		except Order.DoesNotExist:
			order = None
	return render(request, 'shop/order_status.html', {'order': order, 'searched': searched})


def cart_count(request):
	cart = request.session.get('cart', {})
	count = sum(item.get('quantity', 0) for item in cart.values())
	return JsonResponse({'count': count})
