from django.core.management.base import BaseCommand, CommandError
from accounts.models import RegularAccount, BusinessAccount, BillingAddress
from core.models import OrderProduct, Order, Category, ProductImage, Product, Product_Shop, Product_Variant, ProductReview, Shop, ShopReview

from django.core.files import File
from django.utils.timezone import now
import datetime
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Setup the Database for initial manual testing'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        # accounts models population starts here
        try:
            self.stdout.write('Setting up Regular Users')
            user1 = RegularAccount.objects.create(
                username=9897659505, email="manav123@gmail.com", isbusiness=False, dob=datetime.date(2000, 11, 19), gender="M", is_staff=True, is_superuser=True, first_name="Manav",
                last_name="Agarwal")
            user2 = RegularAccount.objects.create(
                username=8076841502, email="khushi123@gmail.com", isbusiness=False, dob=datetime.date(1999, 10, 9), gender="F", is_staff=True, is_superuser=True, first_name="khushi",
                last_name="rauniyar")
            user3 = RegularAccount.objects.create(
                username=8726625518, email="aashutosh123@gmail.com", isbusiness=False, gender="M", is_staff=True, is_superuser=True, first_name="aashutosh",
                last_name="agrawal")
            user4 = RegularAccount.objects.create(
                username=8960734951, email="avanya123@gmail.com", isbusiness=False, gender="F", is_staff=True, is_superuser=True, first_name="avanya",
                last_name="wadhva")
            user5 = RegularAccount.objects.create(
                username=8076841512, email="dummy123@gmail.com", isbusiness=True)
            user6 = RegularAccount.objects.create(
                username=8076841522, email="dummy124@gmail.com", isbusiness=True)
            user7 = RegularAccount.objects.create(
                username=8076841532, email="dummy125@gmail.com", isbusiness=True)
            user8 = RegularAccount.objects.create(
                username=8076841542, email="dummy126@gmail.com", isbusiness=True)
            user9 = RegularAccount.objects.create(
                username=8076841552, email="dummy127@gmail.com", isbusiness=True)
            user10 = RegularAccount.objects.create(
                username=8076841562, email="dummy128@gmail.com")
            user1.set_password("manav")
            user2.set_password("khushi")
            user3.set_password("aashutosh")
            user4.set_password("avanya")
            user5.set_password("manav")
            user6.set_password("manav")
            user7.set_password("manav")
            user8.set_password("manav")
            user9.set_password("manav")
            user10.set_password("manav")

            user1.save()
            user2.save()
            user3.save()
            user4.save()
            user5.save()
            user6.save()
            user7.save()
            user8.save()
            user9.save()
            user10.save()

            self.stdout.write(self.style.SUCCESS(
                'Regular Users Setup Successful'))
        except IntegrityError:
            user1 = RegularAccount.objects.get(
                username=9897659505)
            user2 = RegularAccount.objects.get(
                username=8076841502)
            user3 = RegularAccount.objects.get(
                username=8726625518)
            user4 = RegularAccount.objects.get(
                username=8960734951)
            user5 = RegularAccount.objects.get(
                username=8076841512)
            user6 = RegularAccount.objects.get(
                username=8076841522)
            user7 = RegularAccount.objects.get(
                username=8076841532)
            user8 = RegularAccount.objects.get(
                username=8076841542)
            user9 = RegularAccount.objects.get(
                username=8076841552)
            user10 = RegularAccount.objects.get(
                username=8076841562)
            self.stdout.write(self.style.SUCCESS(
                'Regular Users already Setup'))
        try:
            self.stdout.write('Setting up Business Accounts')
            businessAccount1 = BusinessAccount.objects.create(
                user=user5, pan_number="ABCDE1234A")
            businessAccount2 = BusinessAccount.objects.create(
                user=user6, pan_number="ABCDE1234B")
            businessAccount3 = BusinessAccount.objects.create(
                user=user7, pan_number="ABCDE1234C")
            businessAccount4 = BusinessAccount.objects.create(
                user=user8, pan_number="ABCDE1234D")
            businessAccount5 = BusinessAccount.objects.create(
                user=user9, pan_number="ABCDE1234E")
            self.stdout.write(self.style.SUCCESS(
                'Business Accounts Setup Successful'))
        except IntegrityError:
            businessAccount1 = BusinessAccount.objects.get(
                user=user5, pan_number="ABCDE1234A")
            businessAccount2 = BusinessAccount.objects.get(
                user=user6, pan_number="ABCDE1234B")
            businessAccount3 = BusinessAccount.objects.get(
                user=user7, pan_number="ABCDE1234C")
            businessAccount4 = BusinessAccount.objects.get(
                user=user8, pan_number="ABCDE1234D")
            businessAccount5 = BusinessAccount.objects.get(
                user=user9, pan_number="ABCDE1234E")
            self.stdout.write(self.style.SUCCESS(
                'Business Accounts already Setup'))
        try:
            self.stdout.write('Setting up Billing Addresses')
            billingAddress1 = BillingAddress.objects.create(user=user1, name="manav", contact=9897659505, contact2=6757465748, apartment_address="some apartment",
                                                            street_address="some street", area_pincode="201010", city="ghaziabad", state="UP", address_type="Work", default_shipping=True,
                                                            )
            billingAddress11 = BillingAddress.objects.create(user=user1, name="Manav's Home", contact=8075482541, apartment_address="Mera Apartment",
                                                             street_address="Meri Gali", area_pincode="122045", city="GundaNagar", state="UP", address_type="Home",
                                                             default_billing=True)

            billingAddress2 = BillingAddress.objects.create(user=user2, name="khushi", contact=8076841502, contact2=9876567854, apartment_address="some apartment",
                                                            street_address="some street", area_pincode="201010", city="ghaziabad", state="UP", address_type="Work", default_shipping=True,
                                                            default_billing=False)

            billingAddress3 = BillingAddress.objects.create(user=user3, name="aashutosh", contact=8726625518, contact2=8976456378, apartment_address="some apartment",
                                                            street_address="some street", area_pincode="201010", city="ghaziabad", state="UP", address_type="Work", default_shipping=True,
                                                            default_billing=True)

            billingAddress4 = BillingAddress.objects.create(user=user4, name="avanya", contact=8960734951, contact2=7584657893, apartment_address="some apartment",
                                                            street_address="some street", area_pincode="201010", city="ghaziabad", state="UP", address_type="Work", default_shipping=True,
                                                            default_billing=True)

            billingAddress5 = BillingAddress.objects.create(user=user5, name="dummy1", contact=9897659515, apartment_address="abcd123",
                                                            street_address="abcd1232", area_pincode="201010", city="ghaziabad", state="UP", address_type="Home", default_shipping=True,
                                                            default_billing=False)

            billingAddress6 = BillingAddress.objects.create(user=user6, name="dummy2", contact=9897659525, apartment_address="abcd123",
                                                            street_address="abcd1232", area_pincode="201010", city="ghaziabad", state="UP", address_type="Other", default_shipping=False,
                                                            default_billing=False)

            billingAddress7 = BillingAddress.objects.create(user=user7, name="dummy3", contact=9897659535, apartment_address="abcd123",
                                                            street_address="abcd1232", area_pincode="201010", city="ghaziabad", state="UP", address_type="Home", default_shipping=False,
                                                            default_billing=True)

            billingAddress8 = BillingAddress.objects.create(user=user8, name="dummy4", contact=9897659545, apartment_address="abcd123",
                                                            street_address="abcd1232", area_pincode="201010", city="ghaziabad", state="UP", address_type="Home", default_shipping=True,
                                                            default_billing=True)

            billingAddress9 = BillingAddress.objects.create(user=user9, name="dummy5", contact=9897659555, apartment_address="abcd123",
                                                            street_address="abcd1232", area_pincode="201010", city="ghaziabad", state="UP", address_type="Home", default_shipping=True,
                                                            default_billing=False)

            # billingAddress10 = BillingAddress.objects.create(user=user9, name="dummy6", contact=9897659565, apartment_address="abcd123",
            #                                                  street_address="abcd1232", area_pincode="201010", city="ghaziabad", state="UP", address_type="Home", default_shipping=True,
            #                                                  default_billing=False)

            self.stdout.write(self.style.SUCCESS(
                'Billing Addresses Setup Successful'))
        except IntegrityError:
            billingAddress1 = BillingAddress.objects.get(
                user=user1, name="manav")
            billingAddress11 = BillingAddress.objects.get(
                user=user1, name="Manav's Home")

            billingAddress2 = BillingAddress.objects.get(
                user=user2, name="khushi")

            billingAddress3 = BillingAddress.objects.get(
                user=user3, name="aashutosh")

            billingAddress4 = BillingAddress.objects.get(
                user=user4, name="avanya")

            billingAddress5 = BillingAddress.objects.get(
                user=user5, name="dummy1")

            billingAddress6 = BillingAddress.objects.get(
                user=user6, name="dummy2")

            billingAddress7 = BillingAddress.objects.get(
                user=user7, name="dummy3")

            billingAddress8 = BillingAddress.objects.get(
                user=user8, name="dummy4")

            billingAddress9 = BillingAddress.objects.get(
                user=user9, name="dummy5")

            # billingAddress10 = BillingAddress.objects.get(user=user9, name="dummy6", contact=9897659565, apartment_address="abcd123",
            #                                                  street_address="abcd1232", area_pincode="201010", city="ghaziabad", state="UP", address_type="Home", default_shipping=True,
            #                                                  default_billing=False)

            self.stdout.write(self.style.SUCCESS(
                'Billing Addresses already Setup'))
        # accounts models population ends here

        # Core models population starts here
        try:
            self.stdout.write('Setting up Product Categories')
            category1 = Category.objects.create(
                name="electronics", description="all kinds of electronics avalaible", other_details="battery life,power")
            category2 = Category.objects.create(
                name="fashion", description="all kinds of clothes avalaible", other_details="colour,sleeves type")
            category3 = Category.objects.create(
                name="dairy", description="all kinds of dairy products avalaible")
            category4 = Category.objects.create(
                name="home", description="all kinds of home products avalaible", other_details="size,weight")
            category5 = Category.objects.create(
                name="appliances", description="all kinds of appliances avalaible", other_details="power,size,weight")
            category6 = Category.objects.create(
                name="office", description="all kinds of office products avalaible", other_details="size,weight,length,height")
            category7 = Category.objects.create(
                name="accessories", description="all kinds of accessories products avalaible", other_details="length,size,weight")
            category8 = Category.objects.create(
                name="beauty", description="all kinds of beauty products avalaible", other_details="colour,washable,organic")
            category9 = Category.objects.create(
                name="gift card", description="Gift Cards avalaible")
            category10 = Category.objects.create(
                name="dummy7", description="all kinds of dummy products avalaible", other_details="")
            self.stdout.write(self.style.SUCCESS(
                'Product Categories Setup Successful'))
        except IntegrityError:
            category1 = Category.objects.get(name="electronics")
            category2 = Category.objects.get(name="fashion")
            category3 = Category.objects.get(name="dairy")
            category4 = Category.objects.get(name="home")
            category5 = Category.objects.get(name="appliances")
            category6 = Category.objects.get(name="office")
            category7 = Category.objects.get(name="accessories")
            category8 = Category.objects.get(name="beauty")
            category9 = Category.objects.get(name="gift card")
            category10 = Category.objects.get(name="dummy7")
            self.stdout.write(self.style.SUCCESS('Categories already Setup'))

        try:
            self.stdout.write('Setting up Shops')
            shop1 = Shop.objects.create(business=businessAccount1, name="Agarwal General Store", gstin_number="09ACDPS9765D1ZY", longitude=77.7814200001,
                                        latitude=28.7406100100, contact=9897659505, address='some aapartment', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0), closed_days="SUNDAY,SATURDAY", image=File(open("assets/shops/manavs-shop.png", "rb")))

            shop1.products_categories.set(
                [category1, category2, category3, category4, category5, category6])

            shop2 = Shop.objects.create(business=businessAccount2, name="Rauniyar Mega Store", gstin_number="01ACDPS5745D1ZY", longitude=77.8214200000,
                                        latitude=28.7106200000, contact=8897659505, address='some buailding', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0), closed_days="MONDAY,SUNDAY", image=File(open("assets/shops/khushi-ki-dukaan.jpg", "rb")))

            shop2.products_categories.set(
                [category10, category8, category6, category4, category2])

            shop3 = Shop.objects.create(business=businessAccount3, name="Wadhva's Shopping Hub", gstin_number="19ACDPS5765D1ZY", longitude=77.7214200000,
                                        latitude=28.7406200000, contact=9897459505, address='some buialding', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about afdfasdfadsfadfasdfasdfgasdfasdfa d adgkhakfhadjkfhalkdjh dakjh adsfh jaksdlhf akjlhd jkahds fkjahdfjkh dahkjthe shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0), closed_days="SUNDAY,TUESDAY", image=File(open("assets/shops/avanyas-store.jpg", "rb")))

            shop3.products_categories.set(
                [category3, category9, category7, category1])

            shop4 = Shop.objects.create(business=businessAccount4, name="Agrawal Shopping Center", gstin_number="09BCDPS5765D1ZY", longitude=77.9814200000,
                                        latitude=28.9106200000, contact=9890659505, address='some buialdaing', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0), image=File(open("assets/shops/adsfaf.png", "rb")))

            shop4.products_categories.set([category4, category1, category2])

            shop5 = Shop.objects.create(business=businessAccount1, name="manav's shop 2", gstin_number="18ACDPS5765D1ZY", longitude=77.9214211000,
                                        latitude=28.7116200000, contact=9897659502, address='some buaialdinag', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0), image=File(open("assets/shops/adsfaf.png", "rb")))

            shop5.products_categories.set([category5, category2, category8])

            shop6 = Shop.objects.create(business=businessAccount5, name="Rashan Shop", gstin_number="09ACDPS5765D2ZY", longitude=77.9034200000,
                                        latitude=28.7107500000, contact=9897659503, address='saome buildingaa', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0), image=File(open("assets/shops/adsfaf.png", "rb")))

            shop6.products_categories.set([category6, category10])

            shop7 = Shop.objects.create(business=businessAccount2, name="All in One General Store", gstin_number="09ACDPS5765E1ZY", longitude=77.9211200000,
                                        latitude=28.7106200010, contact=9897659504, address='some buildidfnag', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0),  image=File(open("assets/shops/adsfaf.png", "rb")))

            shop7.products_categories.set(
                [category10, category4, category6, category5])

            shop8 = Shop.objects.create(business=businessAccount3, name="Agarwal Traders", gstin_number="09ACDPS5765D3ZY", longitude=77.9218200000,
                                        latitude=28.7106200900, contact=9897659506, address='some buaaaildadsfing', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0),  image=File(open("assets/shops/adsfaf.png", "rb")))

            shop8.products_categories.set([category1, category2, category3, category4,
                                           category5, category6, category7, category8, category9, category10])

            shop9 = Shop.objects.create(business=businessAccount2, name="shakti and Sons", gstin_number="09ACDPS5765D4ZY", longitude=77.9217200000,
                                        latitude=28.7116200000, contact=9897659507, address='some buildsdsing', street="somewhere", city="ghaziabad",
                                        area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                        open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0), closed_days="SUNDAY,WEDNESDAY", image=File(open("assets/shops/adsfaf.png", "rb")))

            shop9.products_categories.set([category9, category7, category1])

            shop10 = Shop.objects.create(business=businessAccount1, name="Agarwal and Sons", gstin_number="09ACDPS5765D5ZY", longitude=77.9211207000,
                                         latitude=28.7106210009, contact=9897659508, address='some buildasing', street="somewhere", city="ghaziabad",
                                         area_pincode="201016", state="UP", description="some description about the shop", rating=0.0, total_reviews=0,
                                         open_time=datetime.time(6, 0, 0), close_time=datetime.time(18, 0, 0),  image=File(open("assets/shops/adsfaf.png", "rb")))

            shop10.products_categories.set([category1])
            self.stdout.write(self.style.SUCCESS(
                'Shops Setup Successful'))
        except IntegrityError:
            shop1 = Shop.objects.get(
                business=businessAccount1, name="Agarwal General Store", gstin_number="09ACDPS9765D1ZY")
            shop2 = Shop.objects.get(
                business=businessAccount2, name="Rauniyar Mega Store", gstin_number="01ACDPS5745D1ZY")
            shop3 = Shop.objects.get(
                business=businessAccount3, name="Wadhva's Shopping Hub", gstin_number="19ACDPS5765D1ZY")
            shop4 = Shop.objects.get(
                business=businessAccount4, name="Agrawal Shopping Center", gstin_number="09BCDPS5765D1ZY")
            shop5 = Shop.objects.get(
                business=businessAccount1, name="manav's shop 2", gstin_number="18ACDPS5765D1ZY")
            shop6 = Shop.objects.get(
                business=businessAccount5, name="Rashan Shop", gstin_number="09ACDPS5765D2ZY")
            shop7 = Shop.objects.get(
                business=businessAccount2, name="All in One General Store", gstin_number="09ACDPS5765E1ZY")
            shop8 = Shop.objects.get(
                business=businessAccount3, name="Agarwal Traders", gstin_number="09ACDPS5765D3ZY")
            shop9 = Shop.objects.get(
                business=businessAccount2, name="shakti and Sons", gstin_number="09ACDPS5765D4ZY")
            shop10 = Shop.objects.get(
                business=businessAccount1, name="Agarwal and Sons", gstin_number="09ACDPS5765D5ZY")
            self.stdout.write(self.style.SUCCESS(
                'Shops Already Exists'))

        try:
            self.stdout.write('Setting up Shop Reviews')
            shopReview1 = ShopReview.objects.create(
                user=user1, shop=shop1, review="Amazing shop", rating=4, date=now())
            shopReview2 = ShopReview.objects.create(
                user=user2, shop=shop1, review="Wonderful shop", rating=5, date=now())
            shopReview3 = ShopReview.objects.create(
                user=user1, shop=shop2, review="Worst shop", rating=1, date=now())
            shopReview4 = ShopReview.objects.create(
                user=user2, shop=shop2, review="Amazing shop", rating=4, date=now())
            shopReview5 = ShopReview.objects.create(
                user=user3, shop=shop1, review="Poor shop", rating=2, date=now())
            shopReview6 = ShopReview.objects.create(
                user=user3, shop=shop3, review="Dummy Review", rating=4, date=now())
            shopReview7 = ShopReview.objects.create(
                user=user4, shop=shop4, review="Dummy Review", rating=1, date=now())
            shopReview8 = ShopReview.objects.create(
                user=user5, shop=shop5, review="Dummy Review", rating=3, date=now())
            shopReview9 = ShopReview.objects.create(
                user=user6, shop=shop6, review="Dummy Review", rating=4, date=now())
            shopReview10 = ShopReview.objects.create(
                user=user7, shop=shop7, review="Dummy Review", rating=2, date=now())
            shopReview11 = ShopReview.objects.create(
                user=user8, shop=shop7, review="Dummy Review", rating=4, date=now())
            self.stdout.write(self.style.SUCCESS(
                'Shop Reviews Setup Successful'))
        except IntegrityError:
            shopReview1 = ShopReview.objects.get(
                user=user1, shop=shop1)
            shopReview2 = ShopReview.objects.get(
                user=user2, shop=shop1)
            shopReview3 = ShopReview.objects.get(
                user=user1, shop=shop2)
            shopReview4 = ShopReview.objects.get(
                user=user2, shop=shop2)
            shopReview5 = ShopReview.objects.get(
                user=user3, shop=shop1)
            shopReview6 = ShopReview.objects.get(
                user=user3, shop=shop3)
            shopReview7 = ShopReview.objects.get(
                user=user4, shop=shop4)
            shopReview8 = ShopReview.objects.get(
                user=user5, shop=shop5)
            shopReview9 = ShopReview.objects.get(
                user=user6, shop=shop6)
            shopReview10 = ShopReview.objects.get(
                user=user7, shop=shop7)
            shopReview11 = ShopReview.objects.get(
                user=user8, shop=shop7)
            self.stdout.write(self.style.SUCCESS(
                'Shop Reviews already setup'))

        # self.stdout.write('Setting up Products')
        # product1 = Product.objects.create(name="Trimmer", description="some description", sku="abcd12a3", mrp=100, hsn_code=10012,
        #                                   rating=0, total_reviews=0, weight=100)

        # product1.category.set([category1, category2])

        # product2 = Product.objects.create(name="IceCream", description="some description", sku="abcdd124", mrp=200, hsn_code=11012,
        #                                   rating=0, total_reviews=0, weight=100)

        # product2.category.set([category3, category4])

        # product3 = Product.objects.create(name="Clothes", description="some description", sku="abcvd125", mrp=2000, hsn_code=12012,
        #                                   rating=0, total_reviews=0, weight=200)

        # product3.category.set([category2, category5])

        # product4 = Product.objects.create(name="Dummy1", description="some description", sku="abcxd126", mrp=1000, hsn_code=12013,
        #                                   rating=0, total_reviews=0, weight=300)

        # product4.category.set([category5])

        # product5 = Product.objects.create(name="Dummy2", description="some description", sku="abcdd127", mrp=1001, hsn_code=12014,
        #                                   rating=0, total_reviews=0, weight=305)

        # product5.category.set([category6, category7])

        # product6 = Product.objects.create(name="Dummy3", description="some description", sku="abcad128", mrp=1002, hsn_code=12015,
        #                                   rating=0, total_reviews=0, weight=310)

        # product6.category.set([category7])

        # product7 = Product.objects.create(name="Dummy4", description="some description", sku="abcde128", mrp=1001, hsn_code=12015,
        #                                   rating=0, total_reviews=0, weight=305)

        # product7.category.set([category6, category7])

        # product8 = Product.objects.create(name="Dummy5", description="some description", sku="abcqd128", mrp=1001, hsn_code=12016,
        #                                   rating=0, total_reviews=0, weight=305)

        # product8.category.set([category8, category9, category10])

        # product9 = Product.objects.create(name="Dummy6", description="some description", sku="abcid129", mrp=1001, hsn_code=12017,
        #                                   rating=0, total_reviews=0, weight=305)

        # product9.category.set([category10])

        # product10 = Product.objects.create(name="Dummy7", description="some description", sku="abcdg130", mrp=1001, hsn_code=12018,
        #                                    rating=0, total_reviews=0, weight=305)

        # product10.category.set([category9])
        # self.stdout.write(self.style.SUCCESS(
        #     'Products Setup Successful'))

        # self.stdout.write('Setting up Regular Users')
        # productVariant1 = Product_Variant.objects.create(
        #     name="Variant1", product=product1, mrp=1500, other_details={"battery": "yes"})
        # productVariant2 = Product_Variant.objects.create(
        #     name="Variant2", product=product1, mrp=500, other_details={"battery": "no"})
        # productVariant3 = Product_Variant.objects.create(
        #     name="Variant1", product=product2, mrp=500, other_details={"brick": "yes"})
        # productVariant4 = Product_Variant.objects.create(
        #     name="Variant2", product=product2, mrp=600, other_details={"brick": "yes"})
        # productVariant5 = Product_Variant.objects.create(
        #     name="Variant3", product=product2, mrp=600, other_details={"dry_fruits": "yes"})
        # productVariant6 = Product_Variant.objects.create(
        #     name="DummyVariant1", product=product3, mrp=100, other_details={})
        # productVariant7 = Product_Variant.objects.create(
        #     name="DummyVariant2", product=product4, mrp=100, other_details={})
        # productVariant8 = Product_Variant.objects.create(
        #     name="DummyVariant3", product=product5, mrp=100, other_details={})
        # productVariant9 = Product_Variant.objects.create(
        #     name="DummyVariant4", product=product6, mrp=100, other_details={"dummy_key": "dummy_value2"})
        # productVariant10 = Product_Variant.objects.create(
        #     name="DummyVariant5", product=product7, mrp=100, other_details={})
        # self.stdout.write(self.style.SUCCESS(
        #     'Regular Users Setup Successful'))

        # self.stdout.write('Setting up Regular Users')
        # productShop1 = Product_Shop.objects.create(
        #     product=product1, seller=shop1, variant=productVariant1, seller_price=100)
        # productShop2 = Product_Shop.objects.create(
        #     product=product1, seller=shop1, variant=productVariant2, seller_price=400)
        # productShop3 = Product_Shop.objects.create(
        #     product=product2, seller=shop2, variant=productVariant3, seller_price=300)
        # productShop4 = Product_Shop.objects.create(
        #     product=product2, seller=shop2, variant=productVariant4, seller_price=200)
        # productShop5 = Product_Shop.objects.create(
        #     product=product2, seller=shop2, variant=productVariant5, seller_price=500)
        # productShop6 = Product_Shop.objects.create(
        #     product=product3, seller=shop3, variant=productVariant6, seller_price=100)
        # productShop7 = Product_Shop.objects.create(
        #     product=product4, seller=shop4, variant=productVariant7, seller_price=110)
        # productShop8 = Product_Shop.objects.create(
        #     product=product5, seller=shop5, variant=productVariant8, seller_price=200)
        # productShop9 = Product_Shop.objects.create(
        #     product=product6, seller=shop6, variant=productVariant9, seller_price=300)
        # productShop10 = Product_Shop.objects.create(
        #     product=product7, seller=shop7, variant=productVariant10, seller_price=400)
        # self.stdout.write(self.style.SUCCESS(
        #     'Regular Users Setup Successful'))

        # self.stdout.write('Setting up Regular Users')
        # productImage1 = ProductImage.objects.create(product=product1, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage2 = ProductImage.objects.create(product=product2, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage3 = ProductImage.objects.create(product=product3, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage4 = ProductImage.objects.create(product=product4, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage5 = ProductImage.objects.create(product=product5, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage6 = ProductImage.objects.create(product=product6, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage7 = ProductImage.objects.create(product=product7, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage8 = ProductImage.objects.create(product=product8, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage9 = ProductImage.objects.create(product=product9, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # productImage10 = ProductImage.objects.create(product=product10, image=File(
        #     open("assets/products/dairy-milk/c005685f8f804b0aaa637228f507f10d.jpg", "rb")))
        # self.stdout.write(self.style.SUCCESS(
        #     'Regular Users Setup Successful'))

        # self.stdout.write('Setting up Regular Users')
        # productReview1 = ProductReview.objects.create(
        #     user=user1, product=product1, review="Amazing product", rating=5, date=now())
        # productReview2 = ProductReview.objects.create(
        #     user=user1, product=product2, review="Good product", rating=4, date=now())
        # productReview3 = ProductReview.objects.create(
        #     user=user2, product=product1, review="Brilliant product", rating=5, date=now())
        # productReview4 = ProductReview.objects.create(
        #     user=user3, product=product3, review="Ok Ok", rating=3, date=now())
        # productReview5 = ProductReview.objects.create(
        #     user=user3, product=product3, review="Worst product", rating=1, date=now())
        # productReview6 = ProductReview.objects.create(
        #     user=user4, product=product4, review="Dummy Review", rating=2, date=now())
        # productReview7 = ProductReview.objects.create(
        #     user=user5, product=product5, review="Dummy Review", rating=3, date=now())
        # productReview8 = ProductReview.objects.create(
        #     user=user6, product=product6, review="Dummy Review", rating=5, date=now())
        # productReview9 = ProductReview.objects.create(
        #     user=user7, product=product7, review="Dummy Review", rating=3, date=now())
        # productReview10 = ProductReview.objects.create(
        #     user=user8, product=product8, review="Dummy Review", rating=4, date=now())
        # self.stdout.write(self.style.SUCCESS(
        #     'Regular Users Setup Successful'))
        # Core models population ends here
