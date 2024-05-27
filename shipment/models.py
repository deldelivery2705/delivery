from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# ������ ���������� ���������� � ������, � �������� �� ���������.
# ��� �������� ���� � ��������� ����� ������.
# ������ ���� ������ ������������ ���� ������� � ���� ������.
# ������ ������ ��� ����� �������������� �� django.db.models.Model.
# ������� ������ ������������ ���� � ���� ������.
# Django ������������� ������������� ��������� API ��� ������� � ������

# choices (������ ������). �������� (��������, ������ ��� ������) 2-� ���������� ��������,
# ������������ �������� �������� ��� ����.
# ��� �����������, ������ ����� ���������� select ������ ������������ ���������� ����
# � ��������� �������� ���� ���������� ����������.

# ����������� ��� ���� (�����, label). ������ ����, ����� ForeignKey, ManyToManyField � OneToOneField,
# ������ ���������� ��������� �������������� ����������� ��������.
# ���� ��� �� �������, Django �������������� ������� ���, ��������� �������� ����, ������� ������������� �� ������.
# null - ���� True, Django �������� ������ �������� ��� NULL � ���� ������. �� ��������� - False.
# blank - ���� True, ���� �� ����������� � ����� ���� ������. �� ��������� - False.
# ��� �� �� �� ��� � null. null ��������� � ���� ������, blank - � �������� ������.
# ���� ���� �������� blank=True, ����� �������� �������� ������ ��������.
# ��� blank=False - ���� �����������.

# ��������-������� 
class Shop(models.Model):
    shop_title = models.CharField(_('shop_title'), max_length=256)
    link = models.URLField(max_length=256, blank=True, null=True)
    details = models.TextField(_('shop_details'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'shop'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['shop_title']),            
        ]
        # ���������� �� ���������
        ordering = ['shop_title']
    def __str__(self):
        # ����� �������� � ��� SELECT 
        return "{}".format(self.shop_title)
        # Override the save method of the model

# ������ �������
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='application_shop', on_delete=models.CASCADE)
    dates = models.DateTimeField(_('dates'))
    track_number = models.CharField(_('track_number'), unique=True, max_length=13)
    delivery_address = models.CharField(_('delivery_address'), max_length=192)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'application'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['user']),
        ]
        # ���������� �� ���������
        ordering = ['datea']
    def __str__(self):
        # ����� � ��� Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.user, self.track_number)

# ������������� �������������
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
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_application'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datea']),
        ]
        # ���������� �� ���������
        ordering = ['datea']
        # ������� �� ���� �� ��������� �� �������
        managed = False


# ������������ ������ �������
class Movement(models.Model):
    application = models.ForeignKey(Application, related_name='movement_application', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('datem'))
    status = models.CharField(_('movement_status'), max_length=128)
    details = models.TextField(_('movement_details'), blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'movement'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['datem']),
        ]
        # ���������� �� ���������
        ordering = ['datem']        
    def __str__(self):
        # ����� � ��� Select
        return "{} ({}): {}".format(self.datem.strftime('%d.%m.%Y'), self.application, self.status)
