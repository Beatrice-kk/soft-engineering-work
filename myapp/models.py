from django.db import models

class Seat(models.Model):
    s_id = models.CharField(max_length=255, primary_key=True)
    s_type = models.CharField(max_length=255, blank=True, null=True)
    s_price = models.DecimalField(max_digits=10, decimal_places=2)
    s_status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'seat'

class Stop(models.Model):
    stop_id = models.CharField(max_length=255, primary_key=True)
    stop_name = models.CharField(max_length=255, blank=True, null=True)
    stop_order = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'stop'

class WaitingList(models.Model):
    w_id = models.CharField(max_length=255, primary_key=True)
    w_p_id = models.CharField(max_length=255, blank=True, null=True)
    w_f_id = models.CharField(max_length=255, blank=True, null=True)
    w_date = models.DateField()
    w_time = models.TimeField()

    class Meta:
        managed = True
        db_table = 'waiting_list'

class Train(models.Model):
    f_id = models.CharField(max_length=255, primary_key=True)
    f_s_place = models.CharField(max_length=255, blank=True, null=True)
    f_e_place = models.CharField(max_length=255, blank=True, null=True)
    f_s_airfield = models.CharField(max_length=255, blank=True, null=True)
    f_e_airfield = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'train'


class Arrange(models.Model):
    a_id = models.CharField(max_length=255, primary_key=True)
    f = models.ForeignKey(Train, on_delete=models.CASCADE)
    a_date = models.DateField()
    a_s_time = models.TimeField()
    a_e_time = models.TimeField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        managed = True
        db_table = 'arrange'


class Passenger(models.Model):
    p_id = models.CharField(max_length=255, primary_key=True)
    p_name = models.CharField(max_length=255, blank=True, null=True)
    p_tel = models.CharField(max_length=255, blank=True, null=True)
    p_sex = models.CharField(max_length=255, blank=True, null=True)
    p_age = models.IntegerField(blank=True, null=True)
    p_card = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'passenger'

class Ticket(models.Model):
    a = models.ForeignKey(Arrange, on_delete=models.CASCADE)
    t_id = models.CharField(max_length=255, primary_key=True)
    t_seat = models.CharField(max_length=255, blank=True, null=True)
    t_available = models.CharField(max_length=255, blank=True, null=True)
    p_take = models.CharField(max_length=255, blank=True, null=True)
    p_pay = models.CharField(max_length=255, blank=True, null=True)
    t_paytime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'ticket'


class Relationships(models.Model):
    r_id = models.CharField(max_length=255, primary_key=True)
    p_main = models.CharField(max_length=255, blank=True, null=True)
    p_related = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'relationships'


class ManagerAccount(models.Model):
    m_id = models.CharField(max_length=255, primary_key=True)
    m_account = models.CharField(max_length=255, blank=True, null=True)
    m_password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'm_account'


class PassengerAccount(models.Model):
    p_id = models.CharField(max_length=255, primary_key=True)
    p_account = models.CharField(max_length=255, blank=True, null=True)
    p_password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'p_account'


class Stop(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=255)
    stop_order = models.IntegerField()  # 用于表示途径点的顺序

    class Meta:
        managed = True
        db_table = 'stop'

# Create your models here.

