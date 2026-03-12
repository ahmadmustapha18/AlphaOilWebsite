from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Address, Order, OrderItem, PaymentMethod


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'pack_size', 'quantity', 'price', 'line_total')
    
    def line_total(self, obj):
        return f'Rs. {obj.price * obj.quantity:,.0f}'
    line_total.short_description = 'Total'


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'order_count', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_per_page = 25
    inlines = [AddressInline]
    
    def order_count(self, obj):
        count = Order.objects.filter(customer=obj).count()
        return format_html('<strong>{}</strong>', count)
    order_count.short_description = 'Orders'


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_code', 'customer_name', 'customer_phone',
        'status_badge', 'formatted_total', 'item_count',
        'whatsapp_badge', 'created_at'
    )
    list_filter = ('status', 'created_at', 'whatsapp_order')
    search_fields = ('customer__name', 'customer__phone', 'tracking_code')
    inlines = [OrderItemInline]
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('tracking_code', 'created_at', 'customer', 'address', 'total_amount')
    actions = ['mark_confirmed', 'mark_shipped', 'mark_delivered', 'mark_cancelled']
    
    def customer_name(self, obj):
        return obj.customer.name
    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'customer__name'
    
    def customer_phone(self, obj):
        phone = obj.customer.phone
        return format_html('<a href="tel:{}">{}</a>', phone, phone)
    customer_phone.short_description = 'Phone'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FF9800',
            'confirmed': '#2196F3',
            'shipped': '#9C27B0',
            'delivered': '#4CAF50',
            'cancelled': '#F44336',
        }
        color = colors.get(obj.status, '#757575')
        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def formatted_total(self, obj):
        return format_html('<strong>Rs. {:,.0f}</strong>', obj.total_amount)
    formatted_total.short_description = 'Total'
    formatted_total.admin_order_field = 'total_amount'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def whatsapp_badge(self, obj):
        if obj.whatsapp_order:
            return format_html('<span style="color:#25D366;">✓ WhatsApp</span>')
        return '—'
    whatsapp_badge.short_description = 'WhatsApp'
    
    # Bulk actions
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} order(s) marked as Confirmed.')
    mark_confirmed.short_description = '✅ Mark as Confirmed'
    
    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as Shipped.')
    mark_shipped.short_description = '📦 Mark as Shipped'
    
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as Delivered.')
    mark_delivered.short_description = '🎉 Mark as Delivered'
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} order(s) marked as Cancelled.')
    mark_cancelled.short_description = '❌ Mark as Cancelled'
