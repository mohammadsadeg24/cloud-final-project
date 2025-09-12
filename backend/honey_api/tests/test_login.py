# backend/honey_api/tests/test_login.py

from django.test import TestCase, Client
from django.contrib.auth.models import User

class LoginTestCase(TestCase):
    def setUp(self):
        # ایجاد یک کاربر تستی در دیتابیس SQLite
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(
            username=self.username,
            email="test@example.com",
            password=self.password
        )
        self.client = Client()

    def test_login_success(self):
        """تست لاگین موفق با اطلاعات درست"""
        response = self.client.post("/login/", {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")  # بسته به محتوای view تغییر بده

    def test_login_fail_wrong_password(self):
        """تست لاگین ناموفق با پسورد اشتباه"""
        response = self.client.post("/login/", {
            "username": self.username,
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)  # معمولا صفحه لاگین رفرش میشه
        self.assertContains(response, "Invalid credentials")

    def test_login_fail_no_user(self):
        """تست لاگین کاربری که وجود ندارد"""
        response = self.client.post("/login/", {
            "username": "nouser",
            "password": "randompass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials")
