from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Shop, Application, ViewApplication, Movement
# Подключение форм
from .forms import ShopForm, ApplicationForm, MovementForm,SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        return render(request, "index.html")            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Отчеты
@login_required
@group_required("Managers")
def report_index(request):
    try:
        start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
        finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0).strftime('%Y-%m-%d')         
        application = ViewApplication.objects.all().order_by('datea')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по дате
                start_date = request.POST.get("start_date")
                #print(start_date)
                finish_date = request.POST.get("finish_date")
                finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
                application = ViewApplication.objects.filter(datea__range=[start_date, finish_date]).order_by('datea')                
                finish_date = request.POST.get("finish_date")
        return render(request, "report/index.html", {"application": application, "start_date": start_date, "finish_date": finish_date,  })    
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def shop_index(request):
    try:
        shop = Shop.objects.all().order_by('shop_title')
        return render(request, "shop/index.html", {"shop": shop})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def shop_create(request):
    try:    
        if request.method == "POST":
            shop = Shop()
            shop.shop_title = request.POST.get("shop_title")
            shop.link = request.POST.get("link")
            shop.details = request.POST.get("details")                
            shopform = ShopForm(request.POST)
            if shopform.is_valid():
                shop.save()
                return HttpResponseRedirect(reverse('shop_index'))
            else:
                return render(request, 'shop/create.html', {'form': shopform})            
        else:        
            shopform = ShopForm()
            return render(request, "shop/create.html", {"form": shopform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def shop_edit(request, id):
    try:
        shop = Shop.objects.get(id=id) 
        if request.method == "POST":
            shop.shop_title = request.POST.get("shop_title")
            shop.link = request.POST.get("link")
            shop.details = request.POST.get("details")   
            shopform = ShopForm(request.POST)
            if shopform.is_valid():
                shop.save()
                return HttpResponseRedirect(reverse('shop_index'))
            else:
                print(0)
                return render(request, "shop/edit.html", {"form": shopform}) 
        else:
            # Загрузка начальных данных
            shopform = ShopForm(initial={'shop_title': shop.shop_title, 'link': shop.link, 'details': shop.details })
            return render(request, "shop/edit.html", {"form": shopform})
    except Shop.DoesNotExist:
        return HttpResponseNotFound("<h2>Shop not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def shop_delete(request, id):
    try:
        shop = Shop.objects.get(id=id)
        shop.delete()
        return HttpResponseRedirect(reverse('shop_index'))
    except Shop.DoesNotExist:
        return HttpResponseNotFound("<h2>Shop not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def shop_read(request, id):
    try:
        shop = Shop.objects.get(id=id) 
        return render(request, "shop/read.html", {"shop": shop})
    except Shop.DoesNotExist:
        return HttpResponseNotFound("<h2>Shop not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def application_index(request):
    try:
        application = ViewApplication.objects.all().order_by('datea')
        return render(request, "application/index.html", {"application": application})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список 
@login_required
def application_list(request):
    try:
        #print(request.user.id)
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        application = ViewApplication.objects.filter(user_id=request.user.id).order_by('-datea')
        return render(request, "application/list.html", {"application": application, 'first_name': first_name, 'last_name': last_name, 'email': email})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
#@group_required("Managers")
def application_create(request):
    try:
        if request.method == "POST":
            application = Application()
            application.user_id = request.user.id
            application.shop = Shop.objects.filter(id=request.POST.get("shop")).first()
            application.dates = request.POST.get("dates")
            application.track_number = request.POST.get("track_number")
            application.delivery_address = request.POST.get("delivery_address")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_list'))
            else:
                return render(request, "application/create.html", {"form": applicationform})
        else:        
            applicationform = ApplicationForm(initial={'dates': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "application/create.html", {"form": applicationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def application_edit(request, id):
    try:
        application = Application.objects.get(id=id) 
        if request.method == "POST":
            application.shop = Shop.objects.filter(id=request.POST.get("shop")).first()
            application.dates = request.POST.get("dates")
            application.track_number = request.POST.get("track_number")
            application.delivery_address = request.POST.get("delivery_address")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/edit.html", {"form": applicationform})
        else:
            # Загрузка начальных данных
            applicationform = ApplicationForm(initial={'shop': application.shop, 'dates': application.dates.strftime('%Y-%m-%d'), 'track_number': application.track_number, 'delivery_address': application.delivery_address, })
            return render(request, "application/edit.html", {"form": applicationform})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def application_delete(request, id):
    try:
        application = Application.objects.get(id=id)
        application.delete()
        return HttpResponseRedirect(reverse('application_index'))
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def application_read(request, id):
    try:
        application = ViewApplication.objects.get(id=id)
        movement = Movement.objects.filter(application_id=id).order_by('-datem')
        return render(request, "application/read.html", {"application": application, "movement": movement})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def movement_index(request, application_id):
    try:
        movement = Movement.objects.filter(application_id=application_id).order_by('-datem')
        app = Application.objects.get(id=application_id)
        #movement = Movement.objects.all().order_by('-orders', '-datem')
        return render(request, "movement/index.html", {"movement": movement, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def movement_create(request, application_id):
    try:
        app = Application.objects.get(id=application_id)
        if request.method == "POST":
            movement = Movement()
            movement.application_id = application_id
            movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/create.html", {"form": movementform})
        else:
            movementform = MovementForm(initial={ 'datem': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "movement/create.html", {"form": movementform, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def movement_edit(request, id, application_id):
    app = Application.objects.get(id=application_id)
    try:
        movement = Movement.objects.get(id=id) 
        if request.method == "POST":
            #movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/edit.html", {"form": movementform})
        else:
            # Загрузка начальных данных
            movementform = MovementForm(initial={'application': movement.application, 'datem': movement.datem.strftime('%Y-%m-%d'), 'status': movement.status, 'details': movement.details,  })
            return render(request, "movement/edit.html", {"form": movementform, "application_id": application_id, "app": app})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def movement_delete(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id)
        movement.delete()
        return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def movement_read(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id) 
        return render(request, "movement/read.html", {"movement": movement, "application_id": application_id})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")
