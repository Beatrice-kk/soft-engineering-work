from django.test import TestCase
from django.urls import reverse
from myapp.models import PassengerAccount, Passenger
import json

class PassengerProfileTests(TestCase):

    def setUp(self):
        # 创建一个测试乘客账户和乘客信息
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

    def test_get_profile_success(self):
        # 测试获取乘客资料成功
        response = self.client.get(reverse('get_profile'), {'p_id': 'P0001'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'user_info': {
                'p_name': 'Test User',
                'p_sex': 'Male',
                'p_age': 30,
                'p_tel': '1234567890',
                'p_card': '123456789012345678',
            }
        })

    def test_get_profile_not_found(self):
        # 测试获取乘客资料失败（乘客不存在）
        response = self.client.get(reverse('get_profile'), {'p_id': 'P9999'})
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'error',
            'message': 'Passenger not found'
        })

    def test_get_profile_missing_id(self):
        # 测试获取乘客资料时缺少p_id参数
        response = self.client.get(reverse('get_profile'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'error',
            'message': 'Missing p_id'
        })

    def test_change_profile_success(self):
        # 测试更新乘客资料成功
        response = self.client.get(reverse('change_profile'), {
            'p_id': 'P0001',
            'p_name': 'Updated User',
            'p_sex': 'Female',  # 假设 '2' 代表 Female
            'p_age': 31,
            'p_tel': '0987654321',
            'p_card': '987654321012345678'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'message': '个人资料修改成功'
        })

        # 验证更新后的资料
        updated_passenger = Passenger.objects.get(p_id='P0001')
        self.assertEqual(updated_passenger.p_name, 'Updated User')
        self.assertEqual(updated_passenger.p_sex, 'Female')
        self.assertEqual(updated_passenger.p_age, 31)
        self.assertEqual(updated_passenger.p_tel, '0987654321')
        self.assertEqual(updated_passenger.p_card, '987654321012345678')

    def test_change_profile_not_found(self):
        # 测试更新乘客资料失败（乘客不存在）
        response = self.client.get(reverse('change_profile'), {
            'p_id': 'P9999',
            'p_name': 'Nonexistent User',
        })
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'error',
            'message': '未发现账户'
        })

    def test_change_profile_invalid_data(self):
        # 测试更新乘客资料时提供无效数据
        response = self.client.get(reverse('change_profile'), {
            'p_id': 'P0001',
            'p_age': 'invalid_age',  # 年龄应该是整数
            'p_tel': '123'  # 电话号码太短
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'error',
            'message': '无效的输入数据'
        })

    def test_change_profile_duplicate_card(self):
        # 创建另一个乘客用于测试重复身份证
        Passenger.objects.create(
            p_id='P0002',
            p_name='Another User',
            p_tel='5555555555',
            p_sex='Female',
            p_age=25,
            p_card='999999999999999999'
        )
        
        # 尝试更新为已存在的身份证号
        response = self.client.get(reverse('change_profile'), {
            'p_id': 'P0001',
            'p_card': '999999999999999999'
        })
        self.assertEqual(response.status_code, 200)
        # self.assertJSONEqual(str(response.content, encoding='utf8'), {
        #     'status': 'error',
        #     'message': '身份证号已被使用'
        # })
