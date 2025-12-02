from django.test import TestCase
from myapp.models import Passenger, Train, Ticket, WaitingList, Stop, Seat
from django.urls import reverse

class TrainDelayTests(TestCase):

    def setUp(self):
        # 创建乘客 A 和 B
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.passenger_b = Passenger.objects.create(name='Passenger B')

        # 创建列车 K123 和 D456
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin', departure_time='10:00')
        self.train_d456 = Train.objects.create(name='D456', route='Tianjin-Nanjing', departure_time='12:00')

        # 创建乘客 A 的航班
        self.ticket_a1 = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat='1A')
        self.ticket_a2 = Ticket.objects.create(passenger=self.passenger_a, train=self.train_d456, seat='2B')

        # 创建候补乘客 B 的排队信息
        self.waiting_list_b = WaitingList.objects.create(passenger=self.passenger_b, train=self.train_k123)

    def test_train_delay(self):
        # 模拟列车 K123 起飞时间推迟 1 小时
        response = self.client.post(reverse('delay_train'), {'train_id': self.train_k123.id, 'delay': 60})
        self.assertEqual(response.status_code, 200)

        # 检查乘客 A 的换乘行程是否被标记为冲突，并允许改签
        self.ticket_a2.refresh_from_db()
        self.assertTrue(self.ticket_a2.is_conflict)
        self.assertTrue(self.ticket_a2.allow_reschedule)

        # 检查候补乘客 B 是否仍在队列中，并且乘车时间同步更新
        self.waiting_list_b.refresh_from_db()
        self.assertEqual(self.waiting_list_b.train.departure_time, '11:00')

        # 检查列车 D456 的相关换乘影响是否被重新计算
        self.assertTrue(self.train_d456.recalculate_transfer_impact())

    def test_train_delay_no_conflict(self):
        # 模拟列车 K123 起飞时间推迟 30 分钟，不会影响换乘
        response = self.client.post(reverse('delay_train'), {'train_id': self.train_k123.id, 'delay': 30})
        self.assertEqual(response.status_code, 200)

        # 检查乘客 A 的换乘行程是否没有被标记为冲突
        self.ticket_a2.refresh_from_db()
        self.assertFalse(self.ticket_a2.is_conflict)
        self.assertFalse(self.ticket_a2.allow_reschedule)

        # 检查候补乘客 B 是否仍在队列中，并且乘车时间同步更新
        self.waiting_list_b.refresh_from_db()
        self.assertEqual(self.waiting_list_b.train.departure_time, '10:30')

    def test_train_delay_multiple_passengers(self):
        # 创建额外的乘客 C 和他们的航班
        passenger_c = Passenger.objects.create(name='Passenger C')
        ticket_c1 = Ticket.objects.create(passenger=passenger_c, train=self.train_k123, seat='3C')
        ticket_c2 = Ticket.objects.create(passenger=passenger_c, train=self.train_d456, seat='4D')

        # 模拟列车 K123 起飞时间推迟 1 小时
        response = self.client.post(reverse('delay_train'), {'train_id': self.train_k123.id, 'delay': 60})
        self.assertEqual(response.status_code, 200)

        # 检查乘客 A 和 C 的换乘行程是否被标记为冲突，并允许改签
        self.ticket_a2.refresh_from_db()
        ticket_c2.refresh_from_db()
        self.assertTrue(self.ticket_a2.is_conflict)
        self.assertTrue(self.ticket_a2.allow_reschedule)
        self.assertTrue(ticket_c2.is_conflict)
        self.assertTrue(ticket_c2.allow_reschedule)

        # 检查候补乘客 B 是否仍在队列中，并且乘车时间同步更新
        self.waiting_list_b.refresh_from_db()
        self.assertEqual(self.waiting_list_b.train.departure_time, '11:00')

        # 检查列车 D456 的相关换乘影响是否被重新计算
        self.assertTrue(self.train_d456.recalculate_transfer_impact())

class TrainChangeTests(TestCase):

    def setUp(self):
        # 创建乘客 A 和 B
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.passenger_b = Passenger.objects.create(name='Passenger B')

        # 创建列车 K123 和 D456
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin', departure_time='10:00')
        self.train_d456 = Train.objects.create(name='D456', route='Tianjin-Nanjing', departure_time='12:00')

        # 创建乘客 A 的航班
        self.ticket_a1 = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat='1A')
        self.ticket_a2 = Ticket.objects.create(passenger=self.passenger_a, train=self.train_d456, seat='2B')

        # 创建候补乘客 B 的排队信息
        self.waiting_list_b = WaitingList.objects.create(passenger=self.passenger_b, train=self.train_k123)


    def test_remove_stop_tianjin(self):
        # 创建停站信息
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='Tianjin')
        stop_shanghai = Stop.objects.create(train=self.train_k123, station='Shanghai')

        # 模拟删除天津停站
        response = self.client.post(reverse('remove_stop'), {'train_id': self.train_k123.id, 'station': 'Tianjin'})
        self.assertEqual(response.status_code, 200)

        # 检查已购“北京-天津”或“天津-上海”区间航班的乘客是否被通知允许退票或改签
        self.ticket_a1.refresh_from_db()


# 测试修改座位类型或数量
class SeatTypeAndQuantityTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', seat_number=10)

    def test_reduce_hard_sleeper(self):
        # 用例3.1：硬卧数量减少10个
        original_hard_sleeper = self.train_k123.seat_set.filter(seat_type='硬卧').count()
        self.train_k123.seat_set.filter(seat_type='硬卧').delete(10)
        updated_hard_sleeper = self.train_k123.seat_set.filter(seat_type='硬卧').count()
        self.assertEqual(updated_hard_sleeper, original_hard_sleeper - 10)

    def test_remove_business_class(self):
        # 用例3.2：商务座减少至0
        self.train_k123.seat_set.filter(seat_type='商务座').delete()
        self.assertEqual(self.train_k123.seat_set.filter(seat_type='商务座').count(), 0)

    def test_add_first_class(self):
        # 用例3.3：新增一等座
        original_seats = self.train_k123.seat_set.count()
        Seat.objects.create(train=self.train_k123, seat_type='一等座', seat_number=20)
        self.assertEqual(self.train_k123.seat_set.count(), original_seats + 1)

    def test_temp_add_hard_sleeper(self):
        # 用例3.4：临时新增硬卧
        original_hard_sleeper = self.train_k123.seat_set.filter(seat_type='硬卧').count()
        Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=40)
        self.assertEqual(self.train_k123.seat_set.filter(seat_type='硬卧').count(), original_hard_sleeper + 1)

# 测试修改票价
class FareModificationTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', price=500)

    def test_increase_fare(self):
        # 用例4.1：北京-上海票价上涨50元
        original_price = self.ticket_a.price
        self.train_k123.price = 550
        self.train_k123.save()
        self.assertEqual(self.ticket_a.price, original_price)
        new_ticket = Ticket.objects.create(passenger=Passenger.objects.create(name='Passenger B'), train=self.train_k123, seat_type='硬卧')
        self.assertEqual(new_ticket.price, 550)

    def test_partial_increase_fare(self):
        # 用例4.2：部分区间涨价
        stop_beijing = Stop.objects.create(train=self.train_k123, station='北京')
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='天津')
        stop_shanghai = Stop.objects.create(train=self.train_k123, station='上海')
        stop_beijing.price = 120
        stop_beijing.save()
        new_ticket = Ticket.objects.create(passenger=Passenger.objects.create(name='Passenger C'), train=self.train_k123, seat_type='硬卧', origin='北京', destination='天津')
        self.assertEqual(new_ticket.price, 120)

    def test_decrease_fare(self):
        # 用例4.3：全程降价
        original_price = self.ticket_a.price
        self.train_k123.price = 450
        self.train_k123.save()
        self.assertEqual(self.ticket_a.price, original_price)
        new_ticket = Ticket.objects.create(passenger=Passenger.objects.create(name='Passenger D'), train=self.train_k123, seat_type='硬卧')
        self.assertEqual(new_ticket.price, 450)

# 测试数据一致性复杂场景
class DataConsistencyComplexTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', price=500)

    def test_train_adjustment(self):
        # 列车K123的起飞时间提前1小时，新增停站“南京”，减少硬卧20个
        original_departure = self.train_k123.departure_time
        original_stops = self.train_k123.stop_set.count()
        original_hard_sleeper = self.train_k123.seat_set.filter(seat_type='硬卧').count()
        self.train_k123.departure_time = '09:00'
        self.train_k123.save()
        Stop.objects.create(train=self.train_k123, station='南京')
        self.train_k123.seat_set.filter(seat_type='硬卧').delete(20)
        self.assertNotEqual(self.train_k123.departure_time, original_departure)
        self.assertEqual(self.train_k123.stop_set.count(), original_stops + 1)
        self.assertEqual(self.train_k123.seat_set.filter(seat_type='硬卧').count(), original_hard_sleeper - 20)

# 测试补票区间选择
class TicketSupplementIntervalTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', origin='北京', destination='天津')

    def test_supplement_available(self):
        # 场景1：补票区间有余票
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.destination, '上海')

    def test_supplement_no_available(self):
        # 场景2：补票区间无余票
        self.train_k123.seat_set.filter(seat_type='硬卧', origin='天津', destination='上海').delete()
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 400)

    def test_supplement_tight_available(self):
        # 场景3：补票区间余票紧张
        self.train_k123.seat_set.filter(seat_type='硬卧', origin='天津', destination='上海').delete(9)
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 200)

# 测试座位安排与冲突
class SeatArrangementAndConflictTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.passenger_b = Passenger.objects.create(name='Passenger B')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.seat1 = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=1)
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat=self.seat1, origin='北京', destination='天津')

    def test_same_seat_supplement(self):
        # 场景1：同座位补票
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.destination, '上海')
        self.assertEqual(self.ticket_a.seat, self.seat1)

    def test_seat_conflict(self):
        # 场景2：座位冲突（原座位已分配给他人）
        self.ticket_b = Ticket.objects.create(passenger=self.passenger_b, train=self.train_k123, seat=self.seat1, origin='天津', destination='上海')
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 400)

    def test_change_seat_type(self):
        # 场景3：更换座位类型
        new_seat = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=2)
        self.ticket_a.change_seat_type(new_seat)
        self.assertEqual(self.ticket_a.seat, new_seat)

# 测试补票价格与票据
class TicketSupplementPriceAndReceiptTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬座', origin='北京', destination='天津', price=100)

    def test_dynamic_fare(self):
        # 场景1：动态票价
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='天津', price=120)
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.price, 100 + 120)

    def test_refund_price_difference(self):
        # 场景2：退补差价
        original_price = self.ticket_a.price
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='天津', price=80)
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.price, original_price + 80)

# 测试补票区间选择
class TicketSupplementIntervalTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', origin='北京', destination='天津')

    def test_supplement_available(self):
        # 场景1：补票区间有余票
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.destination, '上海')

    def test_supplement_no_available(self):
        # 场景2：补票区间无余票
        self.train_k123.seat_set.filter(seat_type='硬卧', origin='天津', destination='上海').delete()
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 400)

    def test_supplement_tight_available(self):
        # 场景3：补票区间余票紧张
        self.train_k123.seat_set.filter(seat_type='硬卧', origin='天津', destination='上海').delete(9)
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 200)

# 测试座位安排与冲突
class SeatArrangementAndConflictTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.passenger_b = Passenger.objects.create(name='Passenger B')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.seat1 = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=1)
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat=self.seat1, origin='北京', destination='天津')

    def test_same_seat_supplement(self):
        # 场景1：同座位补票
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.destination, '上海')
        self.assertEqual(self.ticket_a.seat, self.seat1)

    def test_seat_conflict(self):
        # 场景2：座位冲突（原座位已分配给他人）
        self.ticket_b = Ticket.objects.create(passenger=self.passenger_b, train=self.train_k123, seat=self.seat1, origin='天津', destination='上海')
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 400)

    def test_change_seat_type(self):
        # 场景3：更换座位类型
        new_seat = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=2)
        self.ticket_a.change_seat_type(new_seat)
        self.assertEqual(self.ticket_a.seat, new_seat)

# 测试补票价格与票据
class TicketSupplementPriceAndReceiptTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬座', origin='北京', destination='天津', price=100)

    def test_dynamic_fare(self):
        # 场景1：动态票价
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='天津', price=120)
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.price, 100 + 120)

    def test_refund_price_difference(self):
        # 场景2：退补差价
        original_price = self.ticket_a.price
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='天津', price=80)
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.price, original_price + 80)

# 测试列车大规模调整
class TrainLargeScaleAdjustmentTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', origin='北京', destination='天津')

    def test_train_adjustment(self):
        # 列车K123的起飞时间提前1小时，新增停站“南京”，减少硬卧20个
        original_departure = self.train_k123.departure_time
        original_stops = self.train_k123.stop_set.count()
        original_hard_sleeper = self.train_k123.seat_set.filter(seat_type='硬卧').count()
        self.train_k123.departure_time = '09:00'
        self.train_k123.save()
        Stop.objects.create(train=self.train_k123, station='南京')
        self.train_k123.seat_set.filter(seat_type='硬卧').delete(20)
        self.assertNotEqual(self.train_k123.departure_time, original_departure)
        self.assertEqual(self.train_k123.stop_set.count(), original_stops + 1)
        self.assertEqual(self.train_k123.seat_set.filter(seat_type='硬卧').count(), original_hard_sleeper - 20)

# 测试补票区间选择（新增）
class TicketSupplementIntervalAdditionalTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', origin='北京', destination='天津')

    def test_supplement_with_waiting_list(self):
        # 场景4：补票区间有余票，但候补队列中有乘客
        self.train_k123.seat_set.filter(seat_type='硬卧', origin='天津', destination='上海').delete(9)
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', origin='天津', destination='上海')
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 200)

    def test_supplement_with_no_seats_available(self):
        # 场景5：补票区间无余票，且候补队列已满
        self.train_k123.seat_set.filter(seat_type='硬卧', origin='天津', destination='上海').delete()
        for i in range(10):
            WaitingList.objects.create(passenger=Passenger.objects.create(name=f'Passenger {i}'), train=self.train_k123, seat_type='硬卧', origin='天津', destination='上海')
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 400)

# 测试座位安排与冲突（新增）
class SeatArrangementAndConflictAdditionalTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.passenger_b = Passenger.objects.create(name='Passenger B')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.seat1 = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=1)
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat=self.seat1, origin='北京', destination='天津')

    def test_seat_reassignment(self):
        # 场景4：座位重新分配
        new_seat = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=2)
        self.ticket_a.change_seat(new_seat)
        self.assertEqual(self.ticket_a.seat, new_seat)

    def test_seat_conflict_with_waiting_list(self):
        # 场景5：座位冲突，且候补队列中有乘客
        self.ticket_b = Ticket.objects.create(passenger=self.passenger_b, train=self.train_k123, seat=self.seat1, origin='天津', destination='上海')
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', origin='天津', destination='上海')
        response = self.client.post(reverse('supplement_seat'), {'ticket_id': self.ticket_a.id, 'new_destination': '上海'})
        self.assertEqual(response.status_code, 400)

# 测试补票价格与票据（新增）
class TicketSupplementPriceAndReceiptAdditionalTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Tianjin-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬座', origin='北京', destination='天津', price=100)

    def test_dynamic_fare_with_waiting_list(self):
        # 场景3：动态票价，且候补队列中有乘客
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='天津', price=120)
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬座', origin='天津', destination='上海')
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.price, 100 + 120)

    def test_refund_price_difference_with_waiting_list(self):
        # 场景4：退补差价，且候补队列中有乘客
        original_price = self.ticket_a.price
        stop_tianjin = Stop.objects.create(train=self.train_k123, station='天津', price=80)
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬座', origin='天津', destination='上海')
        self.ticket_a.supplement_seat(destination='上海')
        self.assertEqual(self.ticket_a.price, original_price + 80)

# 测试票价调整
class FareAdjustmentTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Shanghai', departure_time='10:00')
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧', price=500)

    def test_fare_increase_with_waiting_list(self):
        # 场景1：票价上涨，且候补队列中有乘客
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧')
        self.train_k123.price = 550
        self.train_k123.save()
        new_ticket = Ticket.objects.create(passenger=Passenger.objects.create(name='Passenger B'), train=self.train_k123, seat_type='硬卧')
        self.assertEqual(new_ticket.price, 550)

    def test_fare_decrease_with_waiting_list(self):
        # 场景2：票价下降，且候补队列中有乘客
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧')
        self.train_k123.price = 450
        self.train_k123.save()
        new_ticket = Ticket.objects.create(passenger=Passenger.objects.create(name='Passenger C'), train=self.train_k123, seat_type='硬卧')
        self.assertEqual(new_ticket.price, 450)

# 测试座位分配
class SeatAllocationTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Shanghai', departure_time='10:00')
        self.seat1 = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=1)
        self.ticket_a = Ticket.objects.create(passenger=self.passenger_a, train=self.train_k123, seat=self.seat1, origin='北京', destination='天津')

    def test_seat_allocation_with_waiting_list(self):
        # 场景3：座位分配，且候补队列中有乘客
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧')
        new_seat = Seat.objects.create(train=self.train_k123, seat_type='硬卧', seat_number=2)
        self.ticket_a.change_seat(new_seat)
        self.assertEqual(self.ticket_a.seat, new_seat)

    def test_seat_allocation_with_conflict(self):
        # 场景4：座位分配冲突，且候补队列中有乘客
        WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧')
        self.ticket_b = Ticket.objects.create(passenger=Passenger.objects.create(name='Passenger B'), train=self.train_k123, seat=self.seat1, origin='天津', destination='上海')
        response = self.client.post(reverse('change_seat'), {'ticket_id': self.ticket_a.id, 'new_seat_id': self.seat1.id})
        self.assertEqual(response.status_code, 400)

# 测试候补队列管理
class WaitingListManagementTests(TestCase):

    def setUp(self):
        self.passenger_a = Passenger.objects.create(name='Passenger A')
        self.train_k123 = Train.objects.create(name='K123', route='Beijing-Shanghai', departure_time='10:00')
        self.waiting_list_a = WaitingList.objects.create(passenger=self.passenger_a, train=self.train_k123, seat_type='硬卧')

    def test_waiting_list_priority(self):
        # 场景5：候补队列优先级管理
        self.passenger_b = Passenger.objects.create(name='Passenger B')
        self.waiting_list_b = WaitingList.objects.create(passenger=self.passenger_b, train=self.train_k123, seat_type='硬卧')
        self.assertEqual(self.waiting_list_a.priority, 1)
        self.assertEqual(self.waiting_list_b.priority, 2)

    def test_waiting_list_clear(self):
        # 场景6：候补队列清空
        self.train_k123.seat_set.filter(seat_type='硬卧').delete()
        response = self.client.post(reverse('clear_waiting_list'), {'train_id': self.train_k123.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WaitingList.objects.filter(train=self.train_k123).count(), 0)

    def test_waiting_list_notification(self):
        # 场景7：候补队列通知
        self.train_k123.seat_set.filter(seat_type='硬卧').delete()
        response = self.client.post(reverse('notify_waiting_list'), {'train_id': self.train_k123.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.waiting_list_a.notified)