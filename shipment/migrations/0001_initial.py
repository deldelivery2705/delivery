# Generated by Django 4.2.2 on 2024-05-23 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_title', models.CharField(max_length=256, verbose_name='shop_title')),
                ('link', models.URLField(blank=True, max_length=256, null=True)),
                ('details', models.TextField(verbose_name='news_details')),
            ],
            options={
                'db_table': 'shop',
                'ordering': ['shop_title'],
                'indexes': [models.Index(fields=['shop_title'], name='shop_shop_ti_a988b2_idx')],
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datea', models.DateTimeField(auto_now_add=True, verbose_name='datea')),
                ('dates', models.DateTimeField(verbose_name='dates')),
                ('track_number', models.CharField(max_length=13, unique=True, verbose_name='track_number')),
                ('delivery_address', models.CharField(max_length=192, verbose_name='delivery_address')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_shop', to='shipment.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'application',
                'ordering': ['datea'],
            },
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datem', models.DateTimeField(verbose_name='datem')),
                ('status', models.CharField(max_length=128, verbose_name='movement_status')),
                ('details', models.TextField(blank=True, null=True, verbose_name='movement_details')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movement_application', to='shipment.application')),
            ],
            options={
                'db_table': 'movement',
                'ordering': ['datem'],
                'indexes': [models.Index(fields=['application'], name='movement_applica_27871b_idx'), models.Index(fields=['datem'], name='movement_datem_8708fe_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='application',
            index=models.Index(fields=['datea'], name='application_datea_198fe9_idx'),
        ),
        migrations.AddIndex(
            model_name='application',
            index=models.Index(fields=['user'], name='application_user_id_ba75f5_idx'),
        ),
    ]
