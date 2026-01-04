from django.test import TestCase
from django.urls import reverse
from myapp.models import Passenger, Relationships

class RelationshipTests(TestCase):

    def setUp(self):
        # 创建测试乘客
        self.passenger1 = Passenger.objects.create(
            p_id='P0001',
            p_name='Test User 1',
            p_tel='1234567890',
            p_sex='Male',
            p_age=30,
            p_card='123456789012345678'
        )
        self.passenger2 = Passenger.objects.create(
            p_id='P0002',
            p_name='Test User 2',
            p_tel='0987654321',
            p_sex='Female',
            p_age=25,
            p_card='987654321012345678'
        )

    def test_add_relation_success(self):
        # 测试成功添加关系
        response = self.client.get(reverse('add_relation'), {
            'p_main': 'P0001',
            'p_name': 'Test User 2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'message': '关联人添加成功'
        })

        # 验证关系是否被添加
        relation = Relationships.objects.get(p_main='P0001', p_related='P0002')
        self.assertIsNotNone(relation)

    def test_add_relation_duplicate(self):
        # 测试添加重复关系
        Relationships.objects.create(p_main='P0001', p_related='P0002')  # 先创建一个关系
        response = self.client.get(reverse('add_relation'), {
            'p_main': 'P0001',
            'p_name': 'Test User 2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'info',
            'message': '关系已存在'
        })

    def test_get_relation_success(self):
        # 测试成功获取关系
        Relationships.objects.create(p_main='P0001', p_related='P0002')  # 创建关系
        response = self.client.get(reverse('get_relation'), {
            'p_id': 'P0001'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'data': {
                'relation': [{
                    'name': 'Test User 2',
                    'phone': '0987654321',
                    'card': '987654321012345678'
                }]
            }
        })

    # def test_get_relation_not_found(self):
    #     # 测试获取关系失败（没有关系）
    #     response = self.client.get(reverse('get_relation'), {
    #         'p_id': '1234'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(str(response.content, encoding='utf8'), {
    #         'status': 'error',
    #         'message': 'Passenger not found'
    #     })

    def test_del_relation_success(self):
        # 测试成功删除关系
        relation = Relationships.objects.create(p_main='P0001', p_related='P0002')  # 创建关系
        response = self.client.get(reverse('del_relation'), {
            'p_main': 'P0001',
            'card': '987654321012345678'  # 假设使用身份证号来删除
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'message': '关联人删除成功'
        })

        # 验证关系是否被删除
        with self.assertRaises(Relationships.DoesNotExist):
            Relationships.objects.get(p_main='P0001', p_related='P0002')

    def test_del_relation_not_found(self):
        # 测试删除关系失败（关系不存在）
        response = self.client.get(reverse('del_relation'), {
            'p_main': 'P0001',
            'card': 'nonexistent_card'
        })
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'error',
            'message': '找不到指定的关联人'
        })
