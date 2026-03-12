
from django.contrib import admin
from .models import Category, PackSize, Product, Certification, Price, Inventory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ("name", "slug")

@admin.register(PackSize)
class PackSizeAdmin(admin.ModelAdmin):
	list_display = ("size_display", "volume_ml")

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
	list_display = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ("name", "category", "is_active")
	list_filter = ("category", "is_active")
	search_fields = ("name",)
	filter_horizontal = ("certifications",)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
	list_display = ("product", "pack_size", "price", "is_active", "effective_from", "effective_to")
	list_filter = ("is_active", "effective_from", "effective_to")

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
	list_display = ("product", "pack_size", "stock", "updated_at")

# Register your models here.
