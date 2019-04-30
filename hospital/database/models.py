from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from uuid import uuid4


# Create your models here.

class User(AbstractUser):
    """用户"""
    real_name = models.CharField(max_length=20, verbose_name='真实姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    status = models.BooleanField(default=True, verbose_name='状态,默认启用')
    user_secret = models.UUIDField(default=uuid4(), verbose_name='用户jwt加密')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '用户'


# class ResourceMmanagement(models.Model):
#     """资源管理菜单"""
#     resource = models.CharField(max_length=20, verbose_name='资源名称')
#     resource_url = models.CharField()

class Role(Group):
    """角色"""
    status = models.BooleanField(default=True, verbose_name='状态，默认启用')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除，默认False')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        verbose_name = '角色'


class Department(models.Model):
    """科室"""
    department_name = models.CharField(max_length=20, verbose_name='科室名字')

    def __str__(self):
        return self.department_name

    class Meta:
        db_table = 'department'
        verbose_name = '科室'


class DoctorManage(User):
    """门诊医生信息"""
    id_number = models.CharField(max_length=18, verbose_name='身份证')

    phone = models.CharField(max_length=11, null=True, verbose_name='座机')
    sex = models.BooleanField(default=True, verbose_name='性别')
    birthday = models.DateField(verbose_name='出生年月')
    age = models.PositiveSmallIntegerField(verbose_name='年龄')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='科室管理')
    choice_education = ((1, '大专'), (2, '本科'), (3, '高中'), (4, '硕士'))
    education = models.CharField(choices=choice_education, null=True, verbose_name='学历')
    remark = models.CharField(max_length=100, null=True, verbose_name='备注')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除，默认False')

    def __str__(self):
        return self.real_name

    class Meta:
        db_table = 'doctormanage'
        verbose_name = '门诊医生信息'


class Registration(models.Model):
    """患者挂号信息"""
    name = models.CharField(max_length=20, verbose_name='患者姓名')
    id_number = models.CharField(max_length=18, verbose_name='患者身份证')
    cost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='挂号费')
    social_num = models.CharField(max_length=10, null=True, verbose_name='社保号')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_paying = models.BooleanField(default=True, verbose_name='是否自费')
    sex = models.BooleanField(default=1, verbose_name='性别')
    age = models.PositiveSmallIntegerField(null=True, verbose_name='年龄')
    occupation = models.CharField(max_length=20, null=True, verbose_name='职业')
    is_first = models.BooleanField(default=1, verbose_name='是否是初诊')
    regist_date = models.DateTimeField(auto_now_add=True, verbose_name='挂号时间')
    status_choice = ((1, '已住院'), (2, '已出院'), (3, '已结算'), (4, '未结算'), (5, '已挂号'), (6, '已退号'))
    status = models.CharField(choices=status_choice, verbose_name='患者挂号状态')
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, verbose_name='关联科室')
    doctor = models.ForeignKey(DoctorManage, on_delete=models.DO_NOTHING, verbose_name='关联医生')
    remark = models.CharField(max_length=100, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'registration'
        verbose_name = '病人挂号信息'


class Admission(models.Model):
    """住院办理"""
    nurse = models.CharField(max_length=20, verbose_name='护理')
    bed_id = models.CharField(max_length=10, verbose_name='床位号')
    pay_deposit = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='缴费押金')
    hospital_stays = models.DateTimeField(null=True, verbose_name='住院时间')
    # status_choice = ((1, '已住院'), (2, '已出院'), (3, '已结算'), (4, '未结算'))
    # status = models.CharField(choices=status_choice, verbose_name='患者住院状态')
    state_illness = models.TextField(verbose_name='病情')
    balance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='余额')
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, verbose_name='病人挂号')

    def __str__(self):
        return self.registration.name


class PayItems(models.Model):
    """项目收费"""
    item_name = models.CharField(max_length=50, verbose_name='项目名称')
    charge_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='收费金额')

    def __str__(self):
        return self.item_name

    class Meta:
        db_table = 'payitems'
        verbose_name = '项目收费'


class RegisterItems(models.Model):
    """收费项目登记"""
    item_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, verbose_name='关联患者挂号信息')
    pay_items = models.ForeignKey(PayItems, on_delete=models.CASCADE, verbose_name='关联收费项目')

    def __str__(self):
        return self.registration.name

    class Meta:
        db_table = 'registeritems'
        verbose_name = '收费项目登记'


class Drug(models.Model):
    """药品管理"""
    drug_number = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='药品编号')
    drug_image = models.ImageField(upload_to='drug_image/', verbose_name='药品图片')
    purcha_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='药品进价')
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='药品售价')
    drug_name = models.CharField(max_length=100, verbose_name='药品名称')
    drug_choice = ((1, '处方药'), (2, '中药'), (3, '西药'))
    drug_type = models.CharField(choices=drug_choice, default=1, verbose_name='药品类型')
    drug_descrip = models.CharField(max_length=50, null=True, verbose_name='药品简介')
    expire_date = models.PositiveSmallIntegerField(verbose_name='保质期')
    drug_describe = models.TextField(verbose_name='药品描述')
    manufacturer = models.CharField(max_length=50, null=True, verbose_name='生产厂商')
    use_instructions = models.CharField(max_length=50, verbose_name='服用说明')
    drug_remark = models.CharField(max_length=200, verbose_name='备注')
    drug_status_choice = ((1, '销售中'), (2, '已售空'))
    drug_status = models.CharField(choices=drug_status_choice, default=1, verbose_name='销售状态')
    surplus = models.IntegerField(verbose_name='剩余量')
    inventory = models.IntegerField(verbose_name='库存')

    def __str__(self):
        return self.drug_name

    class Meta:
        db_table = 'drug'
        verbose_name = '药品管理'


class Dispensing(models.Model):
    """发药管理"""
    responsible_name = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='负责人')
    drug_number = models.PositiveSmallIntegerField(verbose_name='发药数量')
    issued_number = models.PositiveSmallIntegerField(verbose_name='已发数量')
    not_issued_number = models.PositiveSmallIntegerField(verbose_name='未发数量')
    registration = models.ForeignKey(Registration, verbose_name='关联患者')

    def __str__(self):
        return self.registration.name

    class Meta:
        db_table = 'dispensing'
        verbose_name = '发药管理'
