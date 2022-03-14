from unittest import TestCase
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import Client
import io

from store.models import Product

User = get_user_model()


class TestProduct(TestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(username="test", email="test@gmail.com")
        self.user.set_password('String@123')
        self.user.save()
        self.cli = Client()
        logged_in = self.cli.login(email='test@gmail.com', password='String@123')

    def test_create_products(self):
        product_data = {"owner": self.user.id, "name": "test", "price": 23.0, "file": io.StringIO("Data into the file")}
        response = self.cli.post("/api/v1/store/product/", product_data)
        self.assertEqual(response.status_code, 201)

    def test_get_products(self):
        response = self.cli.get("/api/v1/store/product/")
        self.assertEqual(response.status_code, 200)


class TestGetTransaction(TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(username="test", email="test@gmail.com")
        self.user.set_password('String@123')
        self.user.save()
        self.cli = Client()
        logged_in = self.cli.login(email='test@gmail.com', password='String@123')

    def test_get_transaction(self):
        response = self.cli.get("/api/v1/store/show_transaction/")
        self.assertEqual(response.status_code, 200)


class TestCreateTransaction(TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(username="test", email="test@gmail.com")
        self.user.set_password('String@123')
        self.user.save()
        self.cli = Client()
        logged_in = self.cli.login(email='test@gmail.com', password='String@123')

    def test_create_transaction(self):
        user, _ = User.objects.get_or_create(username="testProduct", email="testproduct@gmail.com")
        user.set_password('String@123')
        user.save()
        file = ContentFile('test', 'name')
        product, _ = Product.objects.get_or_create(owner_id=user.id, name="test", price=20.0,
                                                   file=file)
        data = {"product_id": product.id}
        response = self.cli.post("/api/v1/store/create_transaction/", data)
        self.assertEqual(response.status_code, 201)
