from django.test import TestCase
from django.urls import reverse
from myapp.models import PassengerAccount, Passenger
import json  # 导入json模块

class UserAuthTests(TestCase):

    def setUp(self):
        self.passenger_account = PassengerAccount.objects.create(
            p_id='P0001',
            p_account='testuser',
            p_password='testpass'
        )
        self.passenger = Passenger.objects.create(
            p_id='P0001',
            p_name='Test User',
            p_tel='1234567890',
            p_sex='Male',
            p_age=30,
            p_card='123456789012345678'
        )

    def test_login_success(self):
        response = self.client.get(reverse('login'), {'name': 'testuser', 'pass': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'res': 1, 'p_id': 'P0001', 'username': 'testuser'})

    def test_login_failure_wrong_password(self):
        response = self.client.get(reverse('login'), {'name': 'testuser', 'pass': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'res': 0})

    def test_login_failure_user_not_exist(self):
        response = self.client.get(reverse('login'), {'name': 'nonexistuser', 'pass': 'testpass'})
        self.assertEqual(response.status_code, 200) 
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'res': 0})

    def test_login_missing_parameters(self):
        response = self.client.get(reverse('login'), {'name': 'testuser'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('login'), {'pass': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        response = self.client.post(reverse('register'), json.dumps({
            'account': 'newuser',
            'pass': 'newpass',
            'name': 'New User',
            'phone': '0987654321',
            'sex': '1',
            'age': 25,
            'card': '987654321012345678'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'res': 3})

        # 验证账户是否真的创建成功
        new_account = PassengerAccount.objects.filter(p_account='newuser').first()
        self.assertIsNotNone(new_account)
        self.assertEqual(new_account.p_password, 'newpass')

        # 验证乘客信息是否创建成功
        new_passenger = Passenger.objects.filter(p_name='New User').first()
        self.assertIsNotNone(new_passenger)
        self.assertEqual(new_passenger.p_tel, '0987654321')

    def test_register_existing_account(self):
        response = self.client.post(reverse('register'), json.dumps({
            'account': 'testuser',
            'pass': 'testpass',
            'name': 'Another User',
            'phone': '1234567890',
            'sex': '1',
            'age': 25,
            'card': '987654321012345678'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'res': 1})

    def test_register_existing_card(self):
        response = self.client.post(reverse('register'), json.dumps({
            'account': 'newuser2',
            'pass': 'testpass2',
            'name': 'Another User',
            'phone': '1234567890',
            'sex': '1',
            'age': 25,
            'card': '123456789012345678'  # 使用已存在的身份证号
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'res': 2})

    def test_register_invalid_parameters(self):
        # 测试无效的手机号格式
        response = self.client.post(reverse('register'), json.dumps({
            'account': 'newuser',
            'pass': 'newpass',
            'name': 'New User',
            'phone': 'invalid_phone',
            'sex': '1',
            'age': 25,
            'card': '987654321012345678'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_register_invalid_card(self):
        # 测试无效的身份证号格式
        response = self.client.post(reverse('register'), json.dumps({
            'account': 'newuser',
            'pass': 'newpass',
            'name': 'New User',
            'phone': '1234567890',
            'sex': '1',
            'age': 25,
            'card': 'invalid_card'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)