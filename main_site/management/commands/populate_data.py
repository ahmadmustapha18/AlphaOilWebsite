from django.core.management.base import BaseCommand
from main_site.models import Category, PackSize, Certification, Product, Price
from shop.models import PaymentMethod
from datetime import date
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate database with sample data for Alpha Cooking Oil'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')
        
        # Create Categories
        cat, _ = Category.objects.get_or_create(
            slug='cooking-oil',
            defaults={'name': 'Cooking Oil', 'description': 'Premium cooking oils'}
        )
        
        # Create Pack Sizes
        pack_1l, _ = PackSize.objects.get_or_create(size_display='1L', defaults={'volume_ml': 1000})
        pack_3l, _ = PackSize.objects.get_or_create(size_display='3L', defaults={'volume_ml': 3000})
        pack_5l, _ = PackSize.objects.get_or_create(size_display='5L', defaults={'volume_ml': 5000})
        pack_tin, _ = PackSize.objects.get_or_create(size_display='16L Tin', defaults={'volume_ml': 16000})
        
        # Create Certifications (without images for now - you can add them later via admin)
        cert_psqca, _ = Certification.objects.get_or_create(
            name='PSQCA Certified',
            defaults={'description': 'Pakistan Standards and Quality Control Authority certified for quality and safety'}
        )
        cert_halal, _ = Certification.objects.get_or_create(
            name='Halal Certified',
            defaults={'description': 'Certified Halal by Islamic authorities'}
        )
        cert_hygiene, _ = Certification.objects.get_or_create(
            name='Hygiene Assured',
            defaults={'description': 'International hygiene standards maintained throughout production'}
        )
        
        # Create Products
        products_data = [
            {
                'name': 'Alpha Pure Cooking Oil',
                'slug': 'alpha-pure-cooking-oil',
                'description': 'Perfect for everyday cooking, frying, and baking. Enriched with Vitamin A & D for your family\'s health.',
                'image': 'alpha-cooking-oil-pouch-1ltr.jpg',
                'prices': {pack_1l: 450, pack_3l: 1300, pack_5l: 2100, pack_tin: 6500}
            },
            {
                'name': 'Alpha Premium Banaspati',
                'slug': 'alpha-premium-banaspati',
                'description': 'Premium quality banaspati ghee for rich, flavorful cooking. Perfect for traditional recipes.',
                'image': 'alpha-banaspati-pouch-1kg-front.jpg',
                'prices': {pack_1l: 500, pack_3l: 1450, pack_5l: 2350}
            },
            {
                'name': 'Alpha Canola Oil',
                'slug': 'alpha-canola-oil',
                'description': 'Low in saturated fats, rich in omega-3 fatty acids. The healthy choice for your family.',
                'image': 'alpha-canola-cooking-oil-pouch-1ltr.jpg',
                'prices': {pack_1l: 550, pack_3l: 1600, pack_5l: 2600}
            },
            {
                'name': 'Alpha Cooking Oil Bottle',
                'slug': 'alpha-cooking-oil-bottle',
                'description': 'Versatile and light, perfect for all-purpose cooking. Available in convenient bottle packaging.',
                'image': 'alpha-cooking-oil-bottle-5ltr.jpg',
                'prices': {pack_3l: 1250, pack_5l: 2000}
            },
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    'name': prod_data['name'],
                    'category': cat,
                    'description': prod_data['description'],
                    'image': prod_data['image'],
                    'is_active': True
                }
            )
            
            if created:
                product.certifications.add(cert_psqca, cert_halal, cert_hygiene)
                
                # Create prices
                for pack_size, price in prod_data['prices'].items():
                    Price.objects.get_or_create(
                        product=product,
                        pack_size=pack_size,
                        defaults={
                            'price': price,
                            'is_active': True,
                            'effective_from': date.today()
                        }
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
        
        # Create Payment Method
        PaymentMethod.objects.get_or_create(
            name='Cash on Delivery',
            defaults={'is_active': True}
        )
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(self.style.WARNING('Note: Product images are set to placeholder. Please add actual images via Django admin.'))
