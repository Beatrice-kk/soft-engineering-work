from django.test import TestCase
from django.urls import reverse
from myapp.models import Train, Arrange, Stop

class TrainWithStopsTests(TestCase):

    def setUp(self):
        # 创建测试航班.
        self.train = Train.objects.create(
            f_id='T0001',
            f_s_place='City A',
            f_e_place='City B',
            f_s_airfield='Station A',
            f_e_airfield='Station B'
        )
        # 创建测试安排
        self.arrange = Arrange.objects.create(
            a_id='A0001',
            f=self.train,
            a_date='2023-10-01',
            a_s_time='10:00:00',
            a_e_time='12:00:00',
            price=100.00
        )

    def test_add_stop_success(self):
        # 测试成功添加途径点
        response = self.client.post(reverse('add_stop'), {
            'train_id': 'T0001',
            'stop_name': 'City C',
            'stop_order': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'message': 'Stop added successfully'
        })

        # 验证途径点是否被添加
        stop = Stop.objects.get(stop_name='City C')
        self.assertIsNotNone(stop)
        self.assertEqual(stop.train, self.train)

    def test_add_stop_duplicate(self):
        # 测试添加重复途径点
        Stop.objects.create(train=self.train, stop_name='City C', stop_order=1)
        response = self.client.post(reverse('add_stop'), {
            'train_id': 'T0001',
            'stop_name': 'City C',
            'stop_order': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'info',
            'message': 'Stop already exists'
        })

    def test_get_stops_success(self):
        # 测试成功获取航班.的途径点
        Stop.objects.create(train=self.train, stop_name='City C', stop_order=1)
        Stop.objects.create(train=self.train, stop_name='City D', stop_order=2)

        response = self.client.get(reverse('get_stops'), {
            'train_id': 'T0001'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'data': [
                {'stop_name': 'City C', 'stop_order': 1},
                {'stop_name': 'City D', 'stop_order': 2}
            ]
        })

    def test_del_stop_success(self):
        # 测试成功删除途径点
        stop = Stop.objects.create(train=self.train, stop_name='City C', stop_order=1)
        response = self.client.post(reverse('del_stop'), {
            'stop_id': stop.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'message': 'Stop deleted successfully'
        })

        # 验证途径点是否被删除
        with self.assertRaises(Stop.DoesNotExist):
            Stop.objects.get(id=stop.id)

    def test_del_stop_not_found(self):
        # 测试删除不存在的途径点
        response = self.client.post(reverse('del_stop'), {
            'stop_id': 9999  # 假设这个ID不存在
        })
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'error',
            'message': 'Stop not found'
        }) 