﻿# Generated by Django 4.2.2 on 2024-05-27 04:34
from pickle import FALSE, TRUE
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.db import migrations
# Подключаем модуль для работы с датой/веременем
from datetime import datetime, timedelta
# Подключаем модкль генерации случайных чисел
import random

# Получение случайного адреса (k - включает ли адрес квартиру)
def get_adres(k):
    ulica = ["ул. Абая", 
            "ул. Алиханова", 
            "ул. Архитектурная", 
            "ул. Баженова", 
            "ул. Байсеитовой", 
            "ул. Ботаническая", 
            "ул. Вавилова", 
            "ул. Воинов-интернационалистов", 
            "ул. Гастелло", 
            "ул. Гончарная", 
            "ул. Грибоедова", 
            "ул. Дружбы", 
            "ул. Ержанова",
            "ул. Ермекова",
            "ул. Жамбыла", 
            "ул. Заводская", 
            "ул. Защитная", 
            "ул. Ипподромная", 
            "ул. Караванная", 
            "ул. Карла Маркса", 
            "ул. Кирпичная", 
            "ул. Кооперации", 
            "ул. Космонавтов", 
            "ул. Курмангазы", 
            "ул. Луговая", 
            "ул. Луначарского", 
            "ул. Махметова", 
            "ул. Маяковского", 
            "ул. Металлистов", 
            "ул. Мира", 
            "ул. Некрасова", 
            "ул. Новоселов",
            "ул. Олимпийская", 
            "ул. Победы", 
            "ул. Привокзальная", 
            "ул. Рыскулова", 
            "ул. Садовая", 
            "ул. Сатпаева", 
            "ул. Степная", 
            "ул. Стремянная", 
            "ул. Таттимбета", 
            "ул. Университетская", 
            "ул. Фрунзе",
            "ул. Чехова", 
            "ул. Чайковского", 
            "ул. Шакирова", 
            "ул. Экибастузская", 
            "ул. Энтузиастов",
            "ул. Юбилейная",
            "ул. Южная"
        ]
    if (k==True):
        adres = random.choice(ulica) + ", " + str(random.randint(1, 200)) + "-" + str(random.randint(1, 200)) 
    else:
        adres = random.choice(ulica) + ", " + str(random.randint(1, 200)) 
    return adres

# Получение случайного Номера документа длиной k
def get_nomer(k):
    nomer = ""
    for i in range(k):
        nomer = nomer + str(random.randint(0, 9))
    return nomer

# Добавить магазин 
def insert_shop(apps, param_shop):   
    Shop = apps.get_model("shipment", "Shop")
    shop = Shop()
    shop.shop_title = param_shop[0]
    shop.link = param_shop[1]
    shop.details = param_shop[2]
    shop.save()
    return

# Добавить заявки клиента 
def insert_application(apps, param_application):   
    Application = apps.get_model("shipment", "Application")
    application = Application()
    application.datea = param_application[0]
    application.user_id = param_application[1]
    application.shop_id = param_application[2]
    application.dates = param_application[3]
    application.track_number = param_application[4]
    application.delivery_address = param_application[5]
    application.save()
    application.datea = param_application[0]
    application.save()
    # Добавить движение заявки
    parameters = [application.id, application.datea, "Заявка принята", "Заявка принята в обработку"]
    insert_movement(apps, parameters)
    parameters = [application.id, application.datea + timedelta(days=1) + timedelta(minutes=random.randint(1, 240)), "Товар в пути", "Товар в пути"]
    insert_movement(apps, parameters)
    # Вероятность в %
    r = random.randrange(1, 100)
    if r > 50:
        parameters = [application.id, application.datea + timedelta(days=14) + timedelta(minutes=random.randint(1, 240)), "Товар на складе", "Товар на складе"]
        insert_movement(apps, parameters)
        if r > 75:
            parameters = [application.id, application.datea + timedelta(days=15) + timedelta(minutes=random.randint(1, 240)), "Товар доставлен", "Товар доставлен"]
            insert_movement(apps, parameters)
    return

# Добавить движение заявки клиента 
def insert_movement(apps, param_movement):   
    Movement = apps.get_model("shipment", "Movement")
    movement = Movement()
    movement.application_id = param_movement[0]
    movement.datem = param_movement[1]
    movement.status = param_movement[2]
    movement.details = param_movement[3]
    movement.save()
    movement.datem = param_movement[1]
    movement.save()
    return

# Начальные данные 
def new_data(apps, schema_editor):
    try:
        # Суперпользователь id=1
        user = User.objects.create_superuser(username='root',
        email='delivery2705@mail.ru',
        first_name='Марат', 
        last_name='Баядилов',
        password='SsNn5678+-@')
        print("Суперпользователь создан")
    
        # Группа менеджеров
        managers = Group.objects.get_or_create(name = 'Managers')
        managers = Group.objects.get(name='Managers')
        print("Группа менеджеров создана")
    
        # Пользователь с ролью менеджера id=2
        user = User.objects.create_user(username='manager', password='Ss0066+-', email='manager@mail.ru', first_name='Алмат', last_name='Кужахметов')
        managers.user_set.add(user)
        print("Менеджер добавлен в группу менеджеров")

        # Простые пользователи (заявители) id3-27
        user = User.objects.create_user(username='user1', password='Uu0066+-', email='user1@mail.ru', first_name='Дина', last_name='Мусина', last_login=datetime.now())
        user = User.objects.create_user(username='user2', password='Uu0066+-', email='user2@mail.ru', first_name='Адия', last_name='Жунусова', last_login=datetime.now())
        user = User.objects.create_user(username='user3', password='Uu0066+-', email='user3@mail.ru', first_name='Айнура', last_name='Кенина', last_login=datetime.now())
        user = User.objects.create_user(username='user4', password='Uu0066+-', email='user4@mail.ru', first_name='Рустем', last_name='Какимов', last_login=datetime.now())
        user = User.objects.create_user(username='user5', password='Uu0066+-', email='user5@mail.ru', first_name='Алишер', last_name='Кабдуалиев', last_login=datetime.now())
        user = User.objects.create_user(username='user6', password='Uu0066+-', email='user6@mail.ru', first_name='Бауржан', last_name='Арыкбаев', last_login=datetime.now())
        user = User.objects.create_user(username='user7', password='Uu0066+-', email='user7@mail.ru', first_name='Алишер', last_name='Танатаров', last_login=datetime.now())
        user = User.objects.create_user(username='user8', password='Uu0066+-', email='user8@mail.ru', first_name='Мерует', last_name='Искакова', last_login=datetime.now())
        user = User.objects.create_user(username='user9', password='Uu0066+-', email='user9@mail.ru', first_name='Ольга', last_name='Муравьева', last_login=datetime.now())
        user = User.objects.create_user(username='user10', password='Uu0066+-', email='user10@mail.ru', first_name='Ақжарқын', last_name='Сансызбаева', last_login=datetime.now())
        user = User.objects.create_user(username='user11', password='Uu0066+-', email='user11@mail.ru', first_name='Арайлым', last_name='Алматова', last_login=datetime.now())
        user = User.objects.create_user(username='user12', password='Uu0066+-', email='user12@mail.ru', first_name='Айгерім', last_name='Дүйсенбиева', last_login=datetime.now())
        user = User.objects.create_user(username='user13', password='Uu0066+-', email='user13@mail.ru', first_name='Салтанат', last_name='Зиноллаева', last_login=datetime.now())
        user = User.objects.create_user(username='user14', password='Uu0066+-', email='user14@mail.ru', first_name='Сейтқасым', last_name='Болат', last_login=datetime.now())
        user = User.objects.create_user(username='user15', password='Uu0066+-', email='user15@mail.ru', first_name='Сара', last_name='Фазилова', last_login=datetime.now())
        user = User.objects.create_user(username='user16', password='Uu0066+-', email='user16@mail.ru', first_name='Бектас', last_name='Ерсейіт', last_login=datetime.now())
        user = User.objects.create_user(username='user17', password='Uu0066+-', email='user17@mail.ru', first_name='Диас', last_name='Мырзаш', last_login=datetime.now())
        user = User.objects.create_user(username='user18', password='Uu0066+-', email='user18@mail.ru', first_name='Нұржан', last_name='Жүрсінбек', last_login=datetime.now())
        user = User.objects.create_user(username='user19', password='Uu0066+-', email='user19@mail.ru', first_name='Дина', last_name='Жағыпар', last_login=datetime.now())
        user = User.objects.create_user(username='user20', password='Uu0066+-', email='user20@mail.ru', first_name='Жастілек', last_name='Жасталап', last_login=datetime.now())
        user = User.objects.create_user(username='user21', password='Uu0066+-', email='user21@mail.ru', first_name='Еркебұлан', last_name='Қадыхан', last_login=datetime.now())
        user = User.objects.create_user(username='user22', password='Uu0066+-', email='user22@mail.ru', first_name='Молдир', last_name='Бутабекова', last_login=datetime.now())
        user = User.objects.create_user(username='user23', password='Uu0066+-', email='user23@mail.ru', first_name='Аружан', last_name='Таурбекова', last_login=datetime.now())
        user = User.objects.create_user(username='user24', password='Uu0066+-', email='user24@mail.ru', first_name='Алтынай', last_name='Қожанова', last_login=datetime.now())
        user = User.objects.create_user(username='user25', password='Uu0066+-', email='user25@mail.ru', first_name='Эльнара', last_name='Иминова', last_login=datetime.now())
        print("Созданы простые пользователи")

        # Магазины
        parameters = ["eBay", "https://www.ebay.com/", "eBay Inc. — американская компания, предоставляющая услуги в областях интернет-аукционов (основное поле деятельности) и интернет-магазинов."]
        insert_shop(apps, parameters)
        parameters = ["Amazon", "https://www.amazon.com/", "Amazon — американская компания, крупнейшая в мире на рынках платформ электронной коммерции и публично-облачных вычислений по выручке и рыночной капитализации."]
        insert_shop(apps, parameters)
        parameters = ["Taobao", "https://taobao.com/", "Taobao.com — интернет-магазин, ориентированный на конечного потребителя. Сайт работает по системе C2C («потребитель для потребителя») — форма электронной торговли, которая заключается в продаже товаров и услуг между потребителями."]
        insert_shop(apps, parameters)
        parameters = ["AliExpress", "https://aliexpress.ru/", "AliExpress — глобальная виртуальная торговая площадка, предоставляющая возможность покупать товары производителей из КНР, а также России, Европы, Турции и других стран. Товары на площадке продаются в розницу и мелким оптом."]
        insert_shop(apps, parameters)
        parameters = ["Walmart", "https://www.walmart.com/", "Walmart, Inc. — американская компания, управляющая крупнейшей в мире сетью оптовой и розничной торговли, действующей под торговой маркой Walmart. "]
        insert_shop(apps, parameters)
        
        print("Созданы Магазины")

        # Заявки клиентов 
        #parameters = [datetime.now() - timedelta(days=50) + timedelta(minutes=random.randint(1, 240)), 3, 1, datetime.now(), "Трек", "Адрес"]
        #insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=49) + timedelta(minutes=random.randint(1, 240)), 3, 1, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=48) + timedelta(minutes=random.randint(1, 240)), 4, 2, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=47) + timedelta(minutes=random.randint(1, 240)), 5, 3, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=46) + timedelta(minutes=random.randint(1, 240)), 6, 4, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=45) + timedelta(minutes=random.randint(1, 240)), 7, 5, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=44) + timedelta(minutes=random.randint(1, 240)), 8, 1, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=43) + timedelta(minutes=random.randint(1, 240)), 9, 2, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=42) + timedelta(minutes=random.randint(1, 240)), 10, 3, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=41) + timedelta(minutes=random.randint(1, 240)), 11, 4, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=40) + timedelta(minutes=random.randint(1, 240)), 12, 5, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=39) + timedelta(minutes=random.randint(1, 240)), 13, 1, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=38) + timedelta(minutes=random.randint(1, 240)), 14, 2, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=37) + timedelta(minutes=random.randint(1, 240)), 15, 3, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=36) + timedelta(minutes=random.randint(1, 240)), 16, 4, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=35) + timedelta(minutes=random.randint(1, 240)), 17, 5, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=34) + timedelta(minutes=random.randint(1, 240)), 18, 1, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=33) + timedelta(minutes=random.randint(1, 240)), 19, 2, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=32) + timedelta(minutes=random.randint(1, 240)), 20, 3, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=31) + timedelta(minutes=random.randint(1, 240)), 21, 4, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=30) + timedelta(minutes=random.randint(1, 240)), 22, 5, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=29) + timedelta(minutes=random.randint(1, 240)), 23, 1, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=28) + timedelta(minutes=random.randint(1, 240)), 24, 2, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=27) + timedelta(minutes=random.randint(1, 240)), 25, 3, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=26) + timedelta(minutes=random.randint(1, 240)), 26, 4, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)
        parameters = [datetime.now() - timedelta(days=25) + timedelta(minutes=random.randint(1, 240)), 27, 5, datetime.now(), "KZ" + get_nomer(10), get_adres(True)]
        insert_application(apps, parameters)

        print("Созданы Заявки клиентов")

        

    except Exception as error:
        print(error)

class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0001_initial'),
    ]

    operations = [
                migrations.RunPython(new_data),
        # PostgreSQL
        migrations.RunSQL("""CREATE VIEW view_application AS
SELECT application.id, application.datea, application.user_id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, application.shop_id, shop.shop_title, shop.link, application.dates, application.track_number, application.delivery_address,
(SELECT  to_char(datem, 'DD.MM.YYYY HH24:MI:SS') || ' - ' || status FROM movement WHERE application_id = application.id ORDER BY datem DESC LIMIT 1) AS final
FROM application
LEFT JOIN auth_user ON application.user_id=auth_user.id
LEFT JOIN shop ON application.shop_id=shop.id"""),
#        # SQLite
#        migrations.RunSQL("""CREATE VIEW view_application AS
#SELECT application.id, application.datea, application.user_id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, application.shop_id, shop.shop_title, shop.link, application.dates, application.track_number, application.delivery_address,
#(SELECT strftime('%d.%m.%Y %H:%M:%S',datem) || ' - ' ||  status FROM movement WHERE application_id = application.id ORDER BY datem DESC LIMIT 1) AS final
#FROM application
#LEFT JOIN auth_user ON application.user_id=auth_user.id
#LEFT JOIN shop ON application.shop_id=shop.id"""),
    ]
