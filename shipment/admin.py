from django.contrib import admin

from .models import  Shop, Application, Movement

# ���������� ������ �� ������� �������� ���������� ��������������
admin.site.register(Shop)
admin.site.register(Application)
admin.site.register(Movement)
