from django.contrib import admin

from .models import  Shop, Application, Movement

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Shop)
admin.site.register(Application)
admin.site.register(Movement)
