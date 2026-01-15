from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ecommerce.models import Store, Product, Profile

class Command(BaseCommand):
    help = 'Populate the database with sample stores and products'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample vendors
        vendors_data = [
            {'username': 'techstore', 'email': 'tech@example.com', 'first_name': 'Tech', 'last_name': 'Store'},
            {'username': 'fashionhub', 'email': 'fashion@example.com', 'first_name': 'Fashion', 'last_name': 'Hub'},
            {'username': 'homestyle', 'email': 'home@example.com', 'first_name': 'Home', 'last_name': 'Style'},
            {'username': 'sportsworld', 'email': 'sports@example.com', 'first_name': 'Sports', 'last_name': 'World'},
        ]

        vendors = []
        for vendor_data in vendors_data:
            user, created = User.objects.get_or_create(
                username=vendor_data['username'],
                defaults={
                    'email': vendor_data['email'],
                    'first_name': vendor_data['first_name'],
                    'last_name': vendor_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                Profile.objects.get_or_create(user=user, defaults={'role': 'vendor'})
                self.stdout.write(f'Created vendor: {user.username}')
            else:
                # Update existing user's profile if needed
                profile, profile_created = Profile.objects.get_or_create(user=user, defaults={'role': 'vendor'})
                if profile_created:
                    self.stdout.write(f'Created profile for existing vendor: {user.username}')
            vendors.append(user)

        # Create sample stores
        stores_data = [
            {
                'name': 'TechZone Electronics',
                'description': 'Your one-stop shop for the latest electronics and gadgets. We offer smartphones, laptops, gaming consoles, and accessories.',
                'vendor': vendors[0]
            },
            {
                'name': 'Fashion Forward',
                'description': 'Trendy clothing and accessories for men and women. Discover the latest fashion trends and express your unique style.',
                'vendor': vendors[1]
            },
            {
                'name': 'Home & Living',
                'description': 'Beautiful home decor, furniture, and lifestyle products. Transform your living space with our curated collection.',
                'vendor': vendors[2]
            },
            {
                'name': 'Sports Pro Shop',
                'description': 'Premium sporting goods and fitness equipment. Gear up for your next adventure with our high-quality products.',
                'vendor': vendors[3]
            },
        ]

        stores = []
        for store_data in stores_data:
            store, created = Store.objects.get_or_create(
                name=store_data['name'],
                owner=store_data['vendor'],
                defaults={'description': store_data['description']}
            )
            if created:
                self.stdout.write(f'Created store: {store.name}')
            stores.append(store)

        # Create sample products with South African Rand pricing
        products_data = [
            # Tech Store Products (realistic SA pricing)
            {'name': 'iPhone 15 Pro', 'description': 'Latest iPhone with advanced camera system and A17 Pro chip', 'price': 25999.99, 'store': stores[0]},
            {'name': 'Samsung Galaxy S24', 'description': 'Flagship Android smartphone with AI features', 'price': 18999.99, 'store': stores[0]},
            {'name': 'Sony WH-1000XM5', 'description': 'Premium wireless noise-canceling headphones', 'price': 8999.99, 'store': stores[0]},
            {'name': 'iPad Pro 12.9"', 'description': 'Professional tablet with M2 chip and Liquid Retina XDR display', 'price': 28999.99, 'store': stores[0]},
            {'name': 'Gaming Laptop', 'description': 'High-performance gaming laptop with RTX graphics', 'price': 34999.99, 'store': stores[0]},

            # Fashion Store Products
            {'name': 'Designer Leather Jacket', 'description': 'Premium leather jacket with modern cut and superior craftsmanship', 'price': 7999.99, 'store': stores[1]},
            {'name': 'Nike Air Max Sneakers', 'description': 'Comfortable athletic shoes with advanced cushioning technology', 'price': 3499.99, 'store': stores[1]},
            {'name': 'Designer Sunglasses', 'description': 'UV protection sunglasses with polarized lenses', 'price': 2499.99, 'store': stores[1]},
            {'name': 'Cotton T-Shirt', 'description': 'Soft, breathable cotton t-shirt in multiple colors', 'price': 399.99, 'store': stores[1]},
            {'name': 'Levi\'s Denim Jeans', 'description': 'Classic fit denim jeans with comfortable stretch', 'price': 1299.99, 'store': stores[1]},

            # Home Store Products
            {'name': 'Modern Sofa', 'description': 'Contemporary 3-seater sofa with premium fabric upholstery', 'price': 18999.99, 'store': stores[2]},
            {'name': 'Ceramic Dinner Set', 'description': '16-piece porcelain dinnerware set for 4 people', 'price': 2499.99, 'store': stores[2]},
            {'name': 'Floor Lamp', 'description': 'Adjustable modern floor lamp with LED lighting', 'price': 2999.99, 'store': stores[2]},
            {'name': 'Throw Pillows Set', 'description': 'Set of 4 decorative throw pillows in various patterns', 'price': 899.99, 'store': stores[2]},
            {'name': 'Wall Art Canvas', 'description': 'Large canvas wall art print, 40x60 inches', 'price': 1499.99, 'store': stores[2]},

            # Sports Store Products
            {'name': 'Yoga Mat', 'description': 'Non-slip exercise mat with carrying strap, 6mm thick', 'price': 699.99, 'store': stores[3]},
            {'name': 'Dumbbell Set', 'description': 'Adjustable dumbbells from 5-50 lbs, space-saving design', 'price': 4999.99, 'store': stores[3]},
            {'name': 'Basketball', 'description': 'Official size indoor/outdoor basketball with superior grip', 'price': 899.99, 'store': stores[3]},
            {'name': 'Tennis Racket', 'description': 'Professional grade tennis racket with graphite construction', 'price': 2999.99, 'store': stores[3]},
            {'name': 'Swimming Goggles', 'description': 'Anti-fog swimming goggles with UV protection', 'price': 349.99, 'store': stores[3]},
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                store=product_data['store'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price']
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name} in {product.store.name}')

        # Create sample buyers
        buyers_data = [
            {'username': 'buyer1', 'email': 'buyer1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'buyer2', 'email': 'buyer2@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        ]

        for buyer_data in buyers_data:
            user, created = User.objects.get_or_create(
                username=buyer_data['username'],
                defaults={
                    'email': buyer_data['email'],
                    'first_name': buyer_data['first_name'],
                    'last_name': buyer_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                Profile.objects.get_or_create(user=user, defaults={'role': 'buyer'})
                self.stdout.write(f'Created buyer: {user.username}')
            else:
                # Update existing user's profile if needed
                profile, profile_created = Profile.objects.get_or_create(user=user, defaults={'role': 'buyer'})
                if profile_created:
                    self.stdout.write(f'Created profile for existing buyer: {user.username}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
        self.stdout.write(f'Created {len(vendors)} vendors, {len(stores)} stores, and {len(products_data)} products.')