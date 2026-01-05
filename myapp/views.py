from datetime import datetime, timedelta
from django.utils import timezone  # 导入Django的timezone模块来处理时区
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
import json
from django.db.models import Max
from django.db import transaction
import os
from myapp.models import ManagerAccount, PassengerAccount, Passenger, Relationships, Ticket, Train, Arrange, Stop


def login(request):
    username = request.GET.get('name')
    password = request.GET.get('pass')
    # print(username)
    # print(password)
    passenger = PassengerAccount.objects.filter(p_account=username)
    manager = ManagerAccount.objects.filter(m_account=username)
    if passenger.count() != 0 and passenger[0].p_password == password:
        res = 1
        p_id = passenger[0].p_id
        response = {'res': res, 'p_id': p_id, 'username': username}
    elif manager.count() != 0 and manager[0].m_password == password:
        res = 2
        m_id = manager[0].m_id
        response = {'res': res, 'p_id': m_id, 'username': username}
    else:
        res = 0
        response = {'res': res}
    return JsonResponse(response)


def register(request):
    data = json.loads(request.body)
    account = data['account']
    card = data['card']
    if PassengerAccount.objects.filter(p_account=account).count() != 0:
        response = {'res': 1}
        return JsonResponse(response)
    elif Passenger.objects.filter(p_card=card).count() != 0:
        response = {'res': 2}
        return JsonResponse(response)
    else:
        if data['sex'] == '1':
            sex = 'Male'
        else:
            sex = 'Female'
        max_id = Passenger.objects.aggregate(Max('p_id'))['p_id__max']
        if max_id:
            max_number = int(max_id[1:]) + 1
        else:
            max_number = 1
        new_p_id = f'P{max_number:04}'
        passenger = Passenger(
            p_id = new_p_id,
            p_name=data['name'],
            p_tel=data['phone'],
            p_sex=sex,
            p_age=data['age'],
            p_card=data['card']
        )
        passenger.save()
        passenger_account = PassengerAccount.objects.create(
            p_id=new_p_id,
            p_account=data['account'],
            p_password=data['pass']
        )
        passenger_account.save()
        response = {'res': 3}
        return JsonResponse(response)


def get_profile(request):
    # 直接从GET请求的查询参数中获取p_id作为字符串
    p_id = request.GET.get('p_id')
    # 验证p_id是否提供
    if not p_id:
        return JsonResponse({'status': 'error', 'message': 'Missing p_id'}, status=400)

    try:
        # 尝试获取乘客信息
        passenger = Passenger.objects.get(pk=p_id)
        user_info = {
            'p_name': passenger.p_name,
            'p_sex': passenger.p_sex,
            'p_age': passenger.p_age,
            'p_tel': passenger.p_tel,
            'p_card': passenger.p_card,
        }
        return JsonResponse({'status': 'success', 'user_info': user_info})
    except Passenger.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Passenger not found'}, status=404)
    except Exception as e:
        # 处理其他可能的异常
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def change_password(request):
    p_id = request.GET.get('p_id')
    old_password = request.GET.get('upassword')
    new_password = request.GET.get('newpassword')
    if not p_id:
        return JsonResponse({'status': 'error', 'message': 'Missing p_id'}, status=400)

    try:
        account = PassengerAccount.objects.get(p_id=p_id)
        if account.p_password == old_password:
            account.p_password = new_password  # Ensure this password is hashed in a real-world scenario
            account.save()
            return JsonResponse({'status': 'success', 'message': '密码修改成功'})
        else:
            return JsonResponse({'status': 'error', 'message': '旧密码输入有误'})
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '未发现账户'}, status=404)
    
from django.http import JsonResponse
from .models import Passenger


# def change_profile(request):
#     # 从GET请求的查询字符串中获取数据
#     p_id = request.GET.get('p_id')
#     new_data = {
#         'p_name': request.GET.get('p_name'),
#         'p_sex': request.GET.get('p_sex'),
#         'p_age': request.GET.get('p_age'),
#         'p_tel': request.GET.get('p_tel'),
#         'p_card': request.GET.get('p_card'),
#     }

#     try:
#         passenger = Passenger.objects.get(pk=p_id)
#         # Update passenger's information here only if the new value is not None or empty string
#         for key, value in new_data.items():
#             if value:  # Check if the new value is not None or empty
#                 setattr(passenger, key, value)  # Update attributes if they exist and value is not None or empty
#         passenger.save()
#         return JsonResponse({'status': 'success', 'message': '个人资料修改成功'})
#     except Passenger.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': '未发现账户'}, status=404)
def change_profile(request):
    # 1. 获取 p_id
    p_id = request.GET.get('p_id')
    
    # 2. 定义需要更新的字段映射
    new_data = {
        'p_name': request.GET.get('p_name'),
        'p_sex': request.GET.get('p_sex'),
        'p_age': request.GET.get('p_age'),
        'p_tel': request.GET.get('p_tel'),
        'p_card': request.GET.get('p_card'),
    }

    try:
        passenger = Passenger.objects.get(pk=p_id)
        
        # 3. 遍历更新字段
        for key, value in new_data.items():
            if value:  # 只有当传入值不为空时才处理
                
                # --- 核心修复点：针对年龄字段进行数字校验 ---
                if key == 'p_age':
                    try:
                        value = int(value) # 强制转换，失败会抛出 ValueError
                    except ValueError:
                        # 如果转换失败，返回测试脚本预期的 400 错误
                        return JsonResponse({
                            'status': 'error', 
                            'message': '无效的输入数据'
                        }, status=400)
                
                setattr(passenger, key, value)
        
        passenger.save()
        return JsonResponse({'status': 'success', 'message': '个人资料修改成功'})

    except Passenger.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '未发现账户'}, status=404)


def get_relation(request):
    p_id = request.GET.get('p_id')
    if not p_id:
        return JsonResponse({'status': 'error', 'message': 'Missing p_id'}, status=400)

    try:
        relations = Relationships.objects.filter(p_main=p_id)
        relation_info = []

        for relation in relations:
            # 获取关联人的详细信息
            passenger = Passenger.objects.get(p_id=relation.p_related)
            relation_info.append({
                'name': passenger.p_name,  # 假设 p_account 字段存储了关联人的姓名
                'phone': passenger.p_tel,  # 假设 p_tel 字段存储了关联人的电话
                'card': passenger.p_card  # 假设 p_card 字段存储了关联人的身份证号
            })

        return JsonResponse({'status': 'success', 'data': {'relation': relation_info}})
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Passenger not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def add_relation(request):
    p_main = request.GET.get('p_main')
    p_related_name = request.GET.get('p_name')

    try:
        # 在Passenger表中查找p_name对应的p_id
        related_passenger = Passenger.objects.get(p_name=p_related_name)
        if(p_main==related_passenger.p_id): return JsonResponse({'status': 'error', 'message': '关联人与用户重复'})
        # 在Relationships表中创建新的关联关系
        new_relation, created = Relationships.objects.get_or_create(
        p_main=p_main,
        p_related=related_passenger.p_id # 使用查找到的p_id
        )
        # 如果已经存在相同的关系，则不做更改
        if not created:
            return JsonResponse({'status': 'info', 'message': '关系已存在'})

        return JsonResponse({'status': 'success', 'message': '关联人添加成功'})
    except Passenger.DoesNotExist:
        # 如果找不到指定p_name的Passenger
        return JsonResponse({'status': 'error', 'message': '找不到指定的关联人'})
    except Relationships.DoesNotExist:
        # 如果Relationships中找不到关系，这通常不会发生，因为我们用的是get_or_create
        return JsonResponse({'status': 'error', 'message': '创建关系失败'})
    except Exception as e:
        # 捕获其他所有异常
        return JsonResponse({'status': 'error', 'message': str(e)})


def del_relation(request):
    p_main = request.GET.get('p_main')
    p_related_card = request.GET.get('card')
    print(p_main, p_related_card)
    try:
        related_passenger = Passenger.objects.get(p_card=p_related_card)
        relation = Relationships.objects.get(p_main=p_main, p_related=related_passenger.p_id)
        print(relation.p_main, relation.p_related)
        relation.delete()  # 删除这个关系
        return JsonResponse({'status': 'success', 'message': '关联人删除成功'})
    except Passenger.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '找不到指定的关联人'}, status=404)
    except Relationships.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '找不到指定的关系'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


from django.http import JsonResponse
from .models import Ticket, Arrange, Train
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Ticket, Arrange, Train
from django.db.models import Q, Count


def getp_ticket(request):
    # 获取前端发送的参数
    page_num = request.GET.get('pageNum', 1)
    page_size = request.GET.get('pageSize', 10)
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    date = request.GET.get('date', '')  # YYYY-MM-DD format
    date = date[:10] if date else ''  # 取前10个字符即可得到 'YYYY-MM-DD'
    seat = request.GET.get('seat', '')
    if date:  # 确保date不为空
        date_obj = datetime.strptime(date[:10], "%Y-%m-%d")  # 将字符串转换为datetime对象
        date_obj += timedelta(days=1)  # 在日期上加一天
        date = date_obj.strftime("%Y-%m-%d")  # 将datetime对象转换回字符串
    print(date)

    # 构建筛选条件
    ticket_filters = Q(t_available='未支付')  # 确保只选择可用的票
    arrange_filters = Q()

    if start:
        ticket_filters &= Q(a__f_id__f_s_place=start)
    if end:
        ticket_filters &= Q(a__f_id__f_e_place=end)
    if date:
        arrange_filters &= Q(a_date=date)
    if seat:
        seat_numbers = [str(i) + seat for i in range(1, 11)]
        ticket_filters &= Q(t_seat__in=seat_numbers)

    # 获取所有Ticket数据并应用筛选条件
    tickets = Ticket.objects.filter(ticket_filters).filter(a__in=Arrange.objects.filter(arrange_filters))

    # 创建空列表来存放最后的数据
    ticket_list = []

    for ticket in tickets:
        arrange = ticket.a  # 直接使用外键访问
        train = arrange.f  # 通过Arrange访问Train

        ticket_list.append({
            '航班编号': ticket.t_id,
            '起始地': train.f_s_place if train else '',
            '目的地': train.f_e_place if train else '',
            '起始机场': train.f_s_airfield if train else '',
            '目的机场': train.f_e_airfield if train else '',
            '起飞时间': arrange.a_s_time if arrange else '',
            '到达时间': arrange.a_e_time if arrange else '',
            '航班价格': arrange.price,
            '座位号': ticket.t_seat,
            '状态': ticket.t_available,
            '日期': arrange.a_date if arrange else '',
        })

    # 分页处理
    paginator = Paginator(ticket_list, int(page_size))
    page = paginator.get_page(int(page_num))

    # 构造返回结果
    data = {
        'tickets': list(page.object_list),
        'total': paginator.count
    }
    return JsonResponse(data)


def get_passenger(request):
    p_id = request.GET.get('p_id')
    try:
        # 获取本人的信息
        passenger = Passenger.objects.get(p_id=p_id)
        # 获取关联人的信息
        relations = Relationships.objects.filter(p_main=passenger.p_id)
        related_passengers = Passenger.objects.filter(p_id__in=[rel.p_related for rel in relations])

        # 构造返回数据
        passenger_list = [
                             {
                                 '姓名': passenger.p_name,
                                 '身份证号': passenger.p_card,
                                 '用户编号':passenger.p_id
                             }
                         ] + [
                             {
                                 '姓名': rp.p_name,
                                 '身份证号': rp.p_card,
                                 '用户编号': rp.p_id
                             } for rp in related_passengers
                         ]

        return JsonResponse({'passengers': passenger_list})
    except Passenger.DoesNotExist:
        return JsonResponse({'passengers': [], 'message': 'No passenger found'}, status=404)


from django.http import JsonResponse
from .models import Ticket


def book_ticket(request):
    if request.method == "GET":
        p_ids_str = request.GET.get('p_ids', '')
        a_id = request.GET.get('a_id')
        p_main = request.GET.get('p_main')

        # 处理乘客ID列表（支持单个ID或逗号分隔的多个ID）
        if ',' in p_ids_str:
            p_ids = p_ids_str.split(',')
        else:
            p_ids = [p_ids_str] if p_ids_str else []

        print(f"a_id: {a_id}")
        print(f"p_ids: {p_ids}")
        print(f"p_main: {p_main}")

        if not a_id or not p_ids:
            return JsonResponse({'message': 'Missing required parameters'}, status=400)

        try:
            # 查找可用的Ticket（状态为'Yes'表示可用）
            available_tickets = Ticket.objects.filter(a_id=a_id, t_available='Yes')

            # 检查是否有足够的可用票
            if available_tickets.count() < len(p_ids):
                return JsonResponse({'message': 'Not enough available tickets'}, status=400)

            booked_count = 0
            for p_id in p_ids:
                # 检查该乘客是否已经预订了这个航班
                if available_tickets.filter(p_take=p_id).exists():
                    return JsonResponse({'message': 'Passenger already booked this flight'}, status=400)

                # 获取一张可用票
                ticket = available_tickets[booked_count]
                ticket.p_take = p_id
                ticket.t_available = 'No'
                ticket.p_pay = p_main
                ticket.save()
                booked_count += 1

            return JsonResponse({'message': 'Ticket booked successfully'})

        except Exception as e:
            print(f"Booking error: {e}")
            return JsonResponse({'message': 'Booking failed'}, status=500)


def booked_tickets(request):
    p_id = request.GET.get('p_id', '')
    print(p_id)
    if not p_id:
        return JsonResponse({'message': 'No p_id provided'}, status=400)
    try:
        passenger = Passenger.objects.get(p_id=p_id)
    except Passenger.DoesNotExist:
        return JsonResponse({'message': 'Passenger not found'}, status=404)
    tickets = Ticket.objects.filter(p_pay=passenger.p_id, t_available="No")

    ticket_list = []
    for ticket in tickets:
        arrange = Arrange.objects.filter(a_id=ticket.a_id).first()
        train = Train.objects.filter(f_id=arrange.f_id).first() if arrange else None
        passenger = Passenger.objects.get(p_id=ticket.p_take)

        ticket_list.append({
            '航班编号': ticket.t_id,
            '起始地': train.f_s_place if train else '',
            '目的地': train.f_e_place if train else '',
            '起始机场': train.f_s_airfield if train else '',
            '目的机场': train.f_e_airfield if train else '',
            '日期': arrange.a_date if arrange else '',
            '起飞时间': arrange.a_s_time if arrange else '',
            '到达时间': arrange.a_e_time if arrange else '',
            '航班价格': ticket.p_pay,
            '座位号': ticket.t_seat,
            '乘客姓名': passenger.p_name,
            '状态': ticket.t_available,
        })

    # 返回JSON数据
    return JsonResponse({'tickets': ticket_list})


def purchase_ticket(request):
    t_id = request.GET.get('t_id')  # 从POST请求获取t_id
    if not t_id:
        return JsonResponse({'message': 'No t_id provided'}, status=400)

    try:
        # 查找对应的Ticket对象
        ticket = Ticket.objects.get(t_id=t_id)
        # 更新Ticket的支付时间为当前时间，状态为'已支付'
        ticket.t_paytime = timezone.now()+ timedelta(hours=8)
        ticket.t_available = "已支付"
        ticket.save()  # 保存更改

        return JsonResponse({'message': 'Ticket purchased successfully'})

    except Ticket.DoesNotExist:
        # 如果找不到Ticket，返回错误信息
        return JsonResponse({'message': 'Ticket not found'}, status=404)

def cancel_ticket(request):
    t_id = request.GET.get('t_id')  # 从POST请求获取t_id
    if not t_id:
        return JsonResponse({'message': 'No t_id provided'}, status=400)

    try:
        # 查找对应的Ticket对象
        ticket = Ticket.objects.get(t_id=t_id)
        ticket.p_take = "No"
        ticket.p_pay = "No"
        ticket.t_available = "Yes"
        ticket.save()  # 保存更改

        return JsonResponse({'message': 'Ticket purchased successfully'})

    except Ticket.DoesNotExist:
        # 如果找不到Ticket，返回错误信息
        return JsonResponse({'message': 'Ticket not found'}, status=404)


def order_tickets(request):
    p_id = request.GET.get('p_id', '')
    print(p_id)
    if not p_id:
        return JsonResponse({'message': 'No p_id provided'}, status=400)
    try:
        passenger = Passenger.objects.get(p_id=p_id)
    except Passenger.DoesNotExist:
        return JsonResponse({'message': 'Passenger not found'}, status=404)
    tickets = Ticket.objects.filter(p_pay=passenger.p_id, t_available="已支付")

    ticket_list = []
    for ticket in tickets:
        arrange = Arrange.objects.filter(a_id=ticket.a_id).first()
        train = Train.objects.filter(f_id=arrange.f_id).first() if arrange else None
        passenger = Passenger.objects.get(p_id=ticket.p_take)

        ticket_list.append({
            '航班编号': ticket.t_id,
            '起始地': train.f_s_place if train else '',
            '目的地': train.f_e_place if train else '',
            '起始机场': train.f_s_airfield if train else '',
            '目的机场': train.f_e_airfield if train else '',
            '日期': arrange.a_date if arrange else '',
            '起飞时间': arrange.a_s_time if arrange else '',
            '到达时间': arrange.a_e_time if arrange else '',
            '航班价格': arrange.price,
            '座位号': ticket.t_seat,
            '乘客姓名': passenger.p_name,
            '状态': ticket.t_available,
            '支付时间':ticket.t_paytime.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({'tickets': ticket_list})


def mget_ticket(request):
    # 1. 获取前端发送的分页和筛选参数
    page_num = request.GET.get('pageNum', 1)
    page_size = request.GET.get('pageSize', 10)
    start_place = request.GET.get('start', '')
    end_place = request.GET.get('end', '')
    date_val = request.GET.get('date', '')

    # 2. 构建针对 Arrange (航线表) 的筛选条件
    # 注意：f__f_s_place 是通过 Arrange 中的外键 f 关联到 Train 表的字段
    arrange_filters = Q()
    if start_place:
        arrange_filters &= Q(f__f_s_place__icontains=start_place)
    if end_place:
        arrange_filters &= Q(f__f_e_place__icontains=end_place)
    if date_val:
        arrange_filters &= Q(a_date=date_val)

    # 3. 执行查询并优化性能 (使用 select_related 减少 SQL 查询次数)
    arranges = Arrange.objects.filter(arrange_filters).select_related('f').order_by('a_date', 'a_s_time')

    # 4. 构造数据列表
    ticket_list = []
    for arrange in arranges:
        # 在 Ticket 表中统计该航线的售票情况
        # 统计“已售”：通常指状态不是“未支付”或“已退票”的
        sold_count = Ticket.objects.filter(a=arrange).exclude(t_available='Yes').count()
        # 统计“剩余”：状态为“未支付”（即可售状态）
        available_count = Ticket.objects.filter(a=arrange, t_available='Yes').count()

        # 获取关联的航线信息
        train = arrange.f

        ticket_list.append({
            "航班编号": arrange.a_id,      # 对应前端的 a_id
            '航线编号': train.f_id,        # 对应前端的 f_id
            '起始地': train.f_s_place,
            '目的地': train.f_e_place,
            '起始机场': train.f_s_airfield,
            '目的机场': train.f_e_airfield,
            '起飞时间': arrange.a_s_time.strftime("%H:%M:%S") if arrange.a_s_time else "",
            '到达时间': arrange.a_e_time.strftime("%H:%M:%S") if arrange.a_e_time else "",
            '航班价格': str(arrange.price), # Decimal类型转为字符串，防止JSON序列化失败
            '日期': arrange.a_date.strftime("%Y-%m-%d") if arrange.a_date else "",
            '已售': sold_count,
            '剩余': available_count
        })

    # 5. 分页处理
    try:
        paginator = Paginator(ticket_list, int(page_size))
        page = paginator.get_page(int(page_num))
        
        data = {
            'tickets': list(page.object_list),
            'total': paginator.count
        }
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse(data)


def change_arrange(request):
    # 从请求中获取参数
    a_id = request.GET.get('a_id')
    start_time = request.GET.get('startTime')
    end_time = request.GET.get('endTime')
    price = request.GET.get('price')
    print(a_id)
    print(start_time)
    print(end_time)
    print(price)
    # 找到并更新Arrange实例
    arrange = get_object_or_404(Arrange, a_id=a_id)
    arrange.a_s_time = start_time
    arrange.a_e_time = end_time
    arrange.price = price
    arrange.save()
    # 返回成功响应
    return JsonResponse({'status': 'success', 'message': 'Arrange and related tickets updated'})


def del_arrange(request):
    # 获取a_id参数
    a_id = request.GET.get('a_id')
    print(a_id)

    # 找到并删除所有相关的Ticket
    tickets = Ticket.objects.filter(a_id=a_id)
    tickets.delete()  # 删除所有相关的票

    # 根据a_id找到Arrange实例并删除
    arrange = get_object_or_404(Arrange, a_id=a_id)
    arrange.delete()

    # 返回成功响应
    return JsonResponse({'status': 'success', 'message': 'Arrange and related tickets deleted successfully'})


def get_train(request):
    # 从请求中获取参数
    start_place = request.GET.get('start', '')  # 获取起始地参数
    end_place = request.GET.get('end', '')  # 获取目的地参数
    page_num = request.GET.get('pageNum', 1)  # 获取页码，默认为第一页
    page_size = request.GET.get('pageSize', 10)  # 获取每页大小，默认为10

    # 构建查询的过滤条件
    query = {}
    if start_place:
        query['f_s_place'] = start_place
    if end_place:
        query['f_e_place'] = end_place

    # 根据提供的起始地和目的地查找符合条件的Train
    trains = Train.objects.filter(**query)

    # 分页处理
    paginator = Paginator(trains, page_size)  # 创建分页对象
    page_obj = paginator.get_page(page_num)  # 获取指定页的数据

    # 创建并填充返回的航班信息列表
    train_list = []
    for train in page_obj:
        train_info = {
            '航线编号': train.f_id,
            '起始地': train.f_s_place,
            '目的地': train.f_e_place,
            '起始机场': train.f_s_airfield,
            '目的机场': train.f_e_airfield
        }
        train_list.append(train_info)

    # 返回响应，包括分页后的数据和总页数
    return JsonResponse({
        'train_list': train_list,
        'total': paginator.count  # 总数据数
    })


def mget_train(request):
    # 从请求中获取参数
    start_place = request.GET.get('start', '')  # 获取起始地参数
    end_place = request.GET.get('end', '')  # 获取目的地参数

    # 构建查询的过滤条件
    query = {}
    if start_place:
        query['f_s_place'] = start_place
    if end_place:
        query['f_e_place'] = end_place

    # 根据提供的起始地和目的地查找符合条件的Train
    trains = Train.objects.filter(**query)


    # 创建并填充返回的航班信息列表
    train_list = []
    for train in trains:
        train_info = {
            '航线编号': train.f_id,
            '起始地': train.f_s_place,
            '目的地': train.f_e_place,
            '起始机场': train.f_s_airfield,
            '目的机场': train.f_e_airfield
        }
        train_list.append(train_info)

    # 返回响应，包括分页后的数据和总页数
    return JsonResponse({
        'train_list': train_list,
    })


def save_arrange(request):
    # 1. 获取参数
    a_id = request.GET.get('a_id', '')
    f_id = request.GET.get('f_id', '')
    date_str = request.GET.get('date', '')
    start_time_str = request.GET.get('start', '')
    end_time_str = request.GET.get('end', '')
    price = request.GET.get('price', '')

    if not all([a_id, f_id, date_str, start_time_str, end_time_str, price]):
        return JsonResponse({'status': 'error', 'message': '字段不完整'})

    # 2. 查重 (解决 Duplicate entry 错误)
    if Arrange.objects.filter(a_id=a_id).exists():
        return JsonResponse({'status': 'error', 'message': f'编号 {a_id} 已存在'})

    # 3. 解析日期时间
    try:
        date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str[11:16], "%H:%M").time()
        end_time = datetime.strptime(end_time_str[11:16], "%H:%M").time()
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': '时间解析失败'})

    # 4. 数据库事务操作
    try:
        with transaction.atomic():
            # A. 创建航线
            arrange = Arrange.objects.create(
                a_id=a_id,
                f_id=f_id,
                a_date=date,
                a_s_time=start_time,
                a_e_time=end_time,
                price=price
            )

            # B. 批量生成机票
            tickets_list = []
            current_now = timezone.now() # 获取当前时间作为默认支付时间占位
            
            for i in range(1, 11): 
                ticket_id = f"T-{a_id}-{i:02d}"
                seat_name = f"{i}A"
                
                tickets_list.append(Ticket(
                    t_id=ticket_id,
                    a_id=a_id,
                    t_seat=seat_name,
                    t_available='Yes',
                    p_take='No',
                    p_pay='No',
                    # 【核心修复】解决 t_paytime cannot be null 报错
                    # 给一个当前时间作为初始值
                    t_paytime=current_now 
                ))
            
            Ticket.objects.bulk_create(tickets_list)

        return JsonResponse({'status': 'success', 'message': '航班及机票成功存入数据库！'})

    except Exception as e:
        # 打印详细报错到控制台，方便调试
        print(f"DEBUG ERROR: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f'数据库创建失败: {str(e)}'})

def change_train(request):
    f_id = request.GET.get('f_id')
    startField = request.GET.get('startField')
    endField = request.GET.get('endField')

    # 使用get()获取单个Train对象
    try:
        train = Train.objects.get(f_id=f_id)  # 确保f_id是唯一的
        train.f_s_airfield = startField
        train.f_e_airfield = endField
        train.save()  # 保存更改
        return JsonResponse({'status': 'success', 'message': 'Train updated successfully'})
    except Train.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Train not found'}, status=404)
    except Exception as e:
        # 适当地处理其他可能的异常，如多个返回对象、数据库错误等。
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def del_train(request):
    # 获取前端通过参数传递的f_id
    f_id = request.GET.get('f_id')
    print(f_id)
    # 查找并删除对应的Arrange对象
    try:
        train = Train.objects.get(f_id=f_id)  # 获取单个Arrange对象
        train.delete()  # 删除对象
        return JsonResponse({'status': 'success', 'message': 'Arrange deleted successfully'})
    except Train.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Arrange not found'}, status=404)
    except Exception as e:
        # 处理其他可能的异常
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def save_train(request):
    # 从GET请求中获取参数
    f_id = request.GET.get('f_id')
    startPlace = request.GET.get('startPlace')
    endPlace = request.GET.get('endPlace')
    startField = request.GET.get('startField')
    endField = request.GET.get('endField')

    # 创建并保存新的航线对象
    try:
        train = Train.objects.create(
            f_id=f_id,
            f_s_place=startPlace,
            f_e_place=endPlace,
            f_s_airfield=startField,
            f_e_airfield=endField
        )
        return JsonResponse({'status': 'success', 'message': 'Train created successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_ticket(request):
    # 获取前端发送的参数
    page_num = request.GET.get('pageNum', 1)
    page_size = request.GET.get('pageSize', 10)
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    date = request.GET.get('date', '').strip()  # YYYY-MM-DD format
    available = request.GET.get('status', '').strip()

    # 构建筛选条件
    ticket_filters = Q()
    if available:  # 如果提供了available，则加入筛选条件
        ticket_filters &= Q(t_available=available)
    if start:
        ticket_filters &= Q(a__f__f_s_place=start)
    if end:
        ticket_filters &= Q(a__f__f_e_place=end)
    if date:
        ticket_filters &= Q(a__a_date=date)

    # 应用筛选条件到Ticket模型
    tickets = Ticket.objects.filter(ticket_filters)

    # 创建空列表来存放最后的数据
    ticket_list = []
    for ticket in tickets:
        arrange = ticket.a
        train = arrange.f

        ticket_list.append({
            "航线编号": arrange.a_id,
            '航班编号': train.f_id,
            '航班编号': ticket.t_id,
            '起始地': train.f_s_place,
            '目的地': train.f_e_place,
            '起始机场': train.f_s_airfield,
            '目的机场': train.f_e_airfield,
            '起飞时间': arrange.a_s_time,
            '到达时间': arrange.a_e_time,
            '航班价格': arrange.price,
            '日期': arrange.a_date,
            '座位号': ticket.t_seat,
            '状态': ticket.t_available,
        })

    # 分页处理
    paginator = Paginator(ticket_list, int(page_size))
    page = paginator.get_page(int(page_num))

    # 构造返回结果
    data = {
        'tickets': list(page.object_list),
        'total': paginator.count
    }
    return JsonResponse(data)


def get_ticket_more(request):
    t_id = request.GET.get('t_id', None)
    # 初始化返回数据
    response_data = {
        'p_name': '',
        'p_account': '',
        't_paytime': ''
    }
    try:
        ticket = Ticket.objects.get(t_id=t_id)
        # 检查ptake是否为空
        if ticket.p_take:  # p_take不为空
            passenger = Passenger.objects.get(p_id=ticket.p_take)
            response_data['p_name'] = passenger.p_name or ""  # 假设p_name是乘客姓名
            try:
                passenger_account = PassengerAccount.objects.get(p_id=passenger.p_id)
                response_data['p_account'] = passenger_account.p_account or ""
            except PassengerAccount.DoesNotExist:
                pass
            if ticket.t_paytime:  # t_paytime不为空
                response_data['t_paytime'] = ticket.t_paytime

        return JsonResponse(response_data)

    except Ticket.DoesNotExist or Passenger.DoesNotExist:
        return JsonResponse({'error': 'Ticket or Passenger does not exist'}, status=404)


def del_ticket(request):
    t_id = request.GET.get('t_id', '')

    if not t_id:
        return JsonResponse({'error': 'No t_ids provided'}, status=400)

    try:
        ticket = Ticket.objects.get(t_id=t_id)
        ticket.delete()

        return JsonResponse({'success': 'Tickets deleted'})

    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'One or more Tickets do not exist'}, status=404)


def del_ticket_batch(request):
    t_ids = request.GET.get('t_ids', '').split(',')

    if not t_ids:
        return JsonResponse({'error': 'No t_ids provided'}, status=400)

    try:
        # 找到所有对应的Tickets并删除
        for t_id in t_ids:
            ticket = Ticket.objects.get(t_id=t_id)
            ticket.delete()

        return JsonResponse({'success': 'Tickets deleted'})

    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'One or more Tickets do not exist'}, status=404)


def mget_passenger(request):
    # 从请求中获取参数
    page_num = request.GET.get('pageNum', 1)
    page_size = request.GET.get('pageSize', 10)
    name = request.GET.get('name', '')
    phone = request.GET.get('phone', '')

    # 获取所有乘客数据，并根据name和phone进行过滤
    passengers = Passenger.objects.all()
    if name:
        passengers = passengers.filter(p_name__icontains=name)
    if phone:
        passengers = passengers.filter(p_tel__contains=phone)

    # 分页处理
    paginator = Paginator(passengers, page_size)
    page = paginator.get_page(page_num)

    # 构建响应数据，确保每个对象都被序列化为字典
    response_data = {
        # 使用values方法将模型实例序列化为字典
        'passengers': list(page.object_list.values('p_id', 'p_name', 'p_tel', 'p_sex', 'p_age', 'p_card')),
        'total': paginator.count  # 总记录数
    }
    return JsonResponse(response_data)


def del_passenger(request):
    p_id = request.GET.get('p_id', '')

    if not p_id:
        return JsonResponse({'error': 'No t_ids provided'}, status=400)

    try:
        passenger = Passenger.objects.get(p_id=p_id)
        passenger.delete()

        return JsonResponse({'success': 'Passenger deleted'})

    except Passenger.DoesNotExist:
        return JsonResponse({'error': 'One or more Passenger do not exist'}, status=404)


def del_passenger_batch(request):
    p_ids = request.GET.get('p_ids', '').split(',')

    if not p_ids:
        return JsonResponse({'error': 'No p_ids provided'}, status=400)

    try:
        # 找到所有对应的Tickets并删除
        for p_id in p_ids:
            passenger = Passenger.objects.get(p_id=p_id)
            passenger.delete()

        return JsonResponse({'success': 'Passenger deleted'})

    except Passenger.DoesNotExist:
        return JsonResponse({'error': 'One or more Passenger do not exist'}, status=404)


def get_account(request):
    # 从请求中获取参数
    username = request.GET.get('username', '')

    if username:
        accounts = PassengerAccount.objects.filter(p_account=username)
    else:
        accounts = PassengerAccount.objects.all()
    accounts_data = list(accounts.values('p_id', 'p_account', 'p_password'))

    return JsonResponse({'accounts': accounts_data})


def reset_account(request):
    # 从请求中获取参数
    p_id = request.GET.get('p_id', '')
    # 查找指定的账户
    try:
        account = PassengerAccount.objects.get(p_id=p_id)
        # 重置密码, 这里为示例设置一个默认值，实际应用中可能需要更安全的处理
        account.p_password = '123456'
        account.save()
        return JsonResponse({'success': 'Password reset successfully'})
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'error': 'Account does not exist'}, status=404)


def del_account(request):
    # 从GET请求中获取参数
    p_id = request.GET.get('p_id', '')
    try:
        account = PassengerAccount.objects.get(p_id=p_id)
        account.delete()
        return JsonResponse({'success': 'Account deleted successfully'})
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'error': 'Account does not exist'}, status=404)


def del_account_batch(request):
    # 从GET请求中获取参数
    p_ids = request.GET.get('p_ids', '')
    p_id_list = p_ids.split(',') if p_ids else []

    if p_id_list:
        # 找到并删除所有匹配的PassengerAccount对象
        for p_id in p_id_list:
            try:
                account = PassengerAccount.objects.get(p_id=p_id)
                account.delete()
            except PassengerAccount.DoesNotExist:
                # 如果PassengerAccount不存在，可以选择记录日志或忽略
                pass

        return JsonResponse({'success': 'Selected accounts deleted'})
    else:
        return JsonResponse({'error': 'No p_ids provided'}, status=400)


def getSchedule(request):
    type = request.GET.get('type', '')
    p_id = request.GET.get('p_id', '')
    if type == '2':
        arranges = Arrange.objects.all()
        dict = {}
        for arrange in arranges:
            date = arrange.a_date.strftime('%Y-%m-%d')
            if date in dict:
                dict[date]+=1
            else:
                dict[date]=1
        for item in dict:
            dict[item] = "航班次数：" + str(dict[item])
        result = [
            {
                "scheduleDay": day,
                "content": content
            } for day, content in dict.items()
        ]
        return JsonResponse({'res': result})
    else:
        tickets = Ticket.objects.filter(p_pay=p_id,t_available='已支付')
        arrangelist = set()
        for ticket in tickets:
            arrangelist.add(ticket.a_id)
        print(arrangelist)
        dict = {}
        for a_id in arrangelist:
            arrange = Arrange.objects.get(a_id=a_id)
            date = arrange.a_date.strftime('%Y-%m-%d')
            if date in dict:
                dict[date] += 1
            else:
                dict[date] = 1
        for item in dict:
            dict[item] = "航班次数：" + str(dict[item])
        result = [
            {
                "scheduleDay": day,
                "content": content
            } for day, content in dict.items()
        ]
        return JsonResponse({'res': result})


def add_stop(request):
    train_id = request.POST.get('train_id')
    stop_name = request.POST.get('stop_name')
    stop_order = request.POST.get('stop_order')

    try:
        train = Train.objects.get(f_id=train_id)
        # 检查是否已经存在相同的途径点
        if Stop.objects.filter(train=train, stop_name=stop_name).exists():
            return JsonResponse({'status': 'info', 'message': 'Stop already exists'})

        Stop.objects.create(train=train, stop_name=stop_name, stop_order=stop_order)
        return JsonResponse({'status': 'success', 'message': 'Stop added successfully'})
    except Train.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Train not found'}, status=404)


def get_stops(request):
    train_id = request.GET.get('train_id')

    try:
        train = Train.objects.get(f_id=train_id)
        stops = Stop.objects.filter(train=train).order_by('stop_order')
        stop_list = [{'stop_name': stop.stop_name, 'stop_order': stop.stop_order} for stop in stops]
        return JsonResponse({'status': 'success', 'data': stop_list})
    except Train.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Train not found'}, status=404)


def del_stop(request):
    stop_id = request.POST.get('stop_id')

    try:
        stop = Stop.objects.get(id=stop_id)
        stop.delete()
        return JsonResponse({'status': 'success', 'message': 'Stop deleted successfully'})
    except Stop.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Stop not found'}, status=404)




