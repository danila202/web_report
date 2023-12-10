from django.db import models


class Marking(models.Model):
    marking = models.CharField(max_length=50)


class Fence(models.Model):
    marking = models.CharField(max_length=50)
    grade = models.CharField(max_length=10)
    subclass = models.CharField(max_length=20)
    group = models.CharField(max_length=10)
    subgroup = models.CharField(max_length=20)
    typ = models.CharField(max_length=50)
    retention_capacity = models.CharField(max_length=5)
    impact_force = models.IntegerField(null=True)
    height = models.FloatField(null=True)
    step_rack = models.FloatField(null=True)
    manufacturer = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'ограждение'


class Material(models.Model):
    name = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    fences_and_elements = models.ManyToManyField(Fence, through='ElementMaterialFence',
                                                 related_name='fences_and_elements')

    class Meta:
        db_table = 'материал'


class Element(models.Model):
    name = models.CharField(max_length=50)
    marking = models.CharField(max_length=30)
    affiliation = models.CharField(max_length=25)
    profile = models.CharField(max_length=20)
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    thickness = models.IntegerField(null=True)
    length = models.IntegerField(null=True)
    materials_and_fences = models.ManyToManyField(Material, through='ElementMaterialFence',
                                                  related_name='elements_and_fences')

    class Meta:
        db_table = 'элемент'


class ElementMaterialFence(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    fence = models.ForeignKey(Fence, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    class Meta:
        db_table = 'МатОгражЭлем'


class Customer(models.Model):
    name = models.CharField(max_length=100)
    type_person = models.CharField(max_length=50)
    address = models.CharField(max_length=150)

    class Meta:
        db_table = 'заказчик'


class Application(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    receipt_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fence = models.ForeignKey(Fence, on_delete=models.CASCADE)

    class Meta:
        db_table = 'заявка'


class Protocol(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    data = models.DateField()
    performer = models.CharField(max_length=50)
    kind = models.CharField(max_length=25)
    fence = models.ForeignKey(Fence, on_delete=models.CASCADE)
    name_file = models.FileField(upload_to='pdf_report')

    class Meta:
        db_table = 'протокол'


class Transport(models.Model):
    kind = models.CharField(max_length=50)
    length = models.IntegerField()
    width = models.IntegerField()
    track = models.IntegerField()
    mass = models.IntegerField()
    load_po = models.FloatField()
    load_zo = models.FloatField()
    height = models.FloatField()

    class Meta:
        db_table = 'тс'


class Test(models.Model):
    data_start = models.DateField()
    data_end = models.DateField()
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    kind = models.CharField(max_length=50)
    speed_collision = models.IntegerField()
    angle_collision = models.IntegerField()
    parameter = models.ManyToManyField('Parameter', through='TestParameter', related_name='tests')

    class Meta:
        db_table = 'испытание'


class Parameter(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    unit_of_measurement = models.CharField(max_length=20)
    value_norm_from = models.FloatField()
    value_norm_before = models.FloatField()
    test = models.ManyToManyField('Test', through='TestParameter', related_name='parameters')

    class Meta:
        db_table = 'параметр'


class TestParameter(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    actual_value = models.FloatField(null=True)

    class Meta:
        db_table = 'ИспытаниеПараметр'

