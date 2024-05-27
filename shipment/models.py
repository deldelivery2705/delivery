from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Интернет-магазин 
class Shop(models.Model):
    shop_title = models.CharField(_('shop_title'), max_length=256)
    link = models.URLField(max_length=256, blank=True, null=True)
    details = models.TextField(_('shop_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'shop'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['shop_title']),            
        ]
        # Сортировка по умолчанию
        ordering = ['shop_title']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{}".format(self.shop_title)
        # Override the save method of the model

# Заявка клиента
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='application_shop', on_delete=models.CASCADE)
    dates = models.DateTimeField(_('dates'))
    track_number = models.CharField(_('track_number'), unique=True, max_length=13)
    delivery_address = models.CharField(_('delivery_address'), max_length=192)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['user']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.user, self.track_number)

# Представление Заявкиклиента
class ViewApplication(models.Model):
    datea = models.DateTimeField(_('datea'))
    user_id = models.IntegerField(_('user_id'))
    username = models.CharField(_('username'), max_length=150)    
    first_name = models.CharField(_('first_name'), max_length=150)    
    last_name = models.CharField(_('last_name'), max_length=150)   
    email = models.CharField(_('email'), max_length=256)   
    shop_id = models.IntegerField(_('shop_id'))
    shop_title = models.CharField(_('shop_title'), max_length=256)
    link = models.URLField(max_length=256, blank=True, null=True)
    dates = models.DateTimeField(_('dates'))
    track_number = models.CharField(_('track_number'), unique=True, max_length=13)
    delivery_address = models.CharField(_('delivery_address'), max_length=192)
    final = models.CharField(_('final'), max_length=256)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']
        # Таблицу не надо не добавлять не удалять
        managed = False


# Рассмотрение заявки клиента
class Movement(models.Model):
    application = models.ForeignKey(Application, related_name='movement_application', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('datem'))
    status = models.CharField(_('movement_status'), max_length=128)
    details = models.TextField(_('movement_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'movement'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['datem']),
        ]
        # Сортировка по умолчанию
        ordering = ['datem']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datem.strftime('%d.%m.%Y'), self.application, self.status)
