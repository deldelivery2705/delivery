from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput, CheckboxInput
from .models import Shop, Application, Movement
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

# Заявки
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_title', 'link', 'details')
        widgets = {
            'shop_title': TextInput(attrs={"size":"100"}),
            'link':  TextInput(attrs={"size":"100", "type":"url"}),            
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),            
        }    

# Заявки
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('shop', 'dates', 'track_number', 'delivery_address')
        widgets = {
            'shop': forms.Select(attrs={'class': 'chosen'}),
            #'dates': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'dates': DateTimeInput(format='%d.%m.%Y'), 
            'track_number': TextInput(attrs={"size":"100"}),
            'delivery_address': TextInput(attrs={"size":"100"}),
        }        
        labels = {
            'shop': _('shop_title'),            
        }

# Движение заявки
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('datem', 'status', 'details')
        widgets = {
            'datem': DateInput(attrs={"type":"date", "readonly":"readonly"}),
            'status': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),
        }

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
