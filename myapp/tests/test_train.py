from django.test import TestCase
from django.urls import reverse
from myapp.models import Train, Arrange

class TrainTests(TestCase):

    def setUp(self):
        # 创建测试列车
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

    def test_get_train_success(self):
        # 测试成功获取列车信息
        response = self.client.get(reverse('get_train'), {
            'start': 'City A',
            'end': 'City B'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('train_list', response.json())

    def test_del_train_success(self):
        # 测试成功删除列车
        response = self.client.get(reverse('del_arrange'), {
            'f_id': 'T0001'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'success',
            'message': 'Arrange deleted successfully'
        })

    def test_del_train_not_found(self):
        # 测试删除不存在的列车
        response = self.client.get(reverse('del_arrange'), {
            'f_id': 'NON_EXISTENT_TRAIN'
        })
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'status': 'error',
            'message': 'Arrange not found'
        })
