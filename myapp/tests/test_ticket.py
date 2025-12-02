from django.test import TestCase
from django.urls import reverse
from myapp.models import Ticket, Arrange, Train, Passenger
from datetime import datetime

class TicketTests(TestCase):

    def setUp(self):
        # 创建测试乘客
        self.passenger = Passenger.objects.create(
            p_id='P0001',
            p_name='Test User',
            p_tel='1234567890',
            p_sex='Male',
            p_age=30,
            p_card='123456789012345678'
        )
        # 创建测试列车和安排
        self.train = Train.objects.create(
            f_id='T0001',
            f_s_place='City A',
            f_e_place='City B',
            f_s_airfield='Station A',
            f_e_airfield='Station B'
        )
        self.arrange = Arrange.objects.create(
            a_id='A0001',
            f=self.train,
            a_date='2023-10-01',
            a_s_time='10:00:00',
            a_e_time='12:00:00',
            price=100.00
        )
        # 创建测试航班
        self.ticket = Ticket.objects.create(
            a=self.arrange,
            t_id='TICKET001',
            t_seat='1A',
            t_available='未支付',
            p_take=None,
            p_pay=None,
            t_paytime=datetime.now()  # 设置一个默认的支付时间
        )

    def test_get_ticket_success(self):
        # 测试获取航班成功
        response = self.client.get(reverse('get_ticket'), {
            'start': 'City A',
            'end': 'City B',
            'date': '2023-10-01'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('tickets', response.json())

    def test_book_ticket_success(self):
        # 测试成功预订航班
        response = self.client.get(reverse('book_ticket'), {
            'p_ids': 'P0001',
            'a_id': 'A0001',
            'p_main': 'P0001'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'message': 'Ticket booked successfully'
        })

    def test_del_ticket_success(self):
        # 测试成功删除航班
        response = self.client.get(reverse('del_ticket'), {
            't_id': 'TICKET001'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'success': 'Tickets deleted'
        })

    def test_del_ticket_not_found(self):
        # 测试删除不存在的航班
        response = self.client.get(reverse('del_ticket'), {
            't_id': 'NON_EXISTENT_TICKET'
        })
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'error': 'One or more Tickets do not exist'
        })
