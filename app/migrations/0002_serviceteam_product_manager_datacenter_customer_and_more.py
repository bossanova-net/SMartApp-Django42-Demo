# Generated by Django 4.2.10 on 2024-02-22 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_team_name', models.CharField(max_length=255, verbose_name='Service Team Name ')),
                ('service_team_telephone', models.CharField(default='-', max_length=255, verbose_name='Service Team Telephone')),
                ('service_team_email', models.CharField(default='-', max_length=150, verbose_name='Service Team Email')),
                ('company', models.ForeignKey(default=1, help_text='Default=Yip - Yip In Tsoi', on_delete=django.db.models.deletion.CASCADE, to='app.company', verbose_name='Yip and SubContractor')),
            ],
            options={
                'ordering': ['service_team_name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='Product-Supporter Name')),
                ('product_telephone', models.CharField(default='-', max_length=255, verbose_name='Product-Supporter Telephone')),
                ('product_email', models.CharField(default='-', max_length=150, verbose_name='Product-Supporter Email')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update At')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='Remark')),
                ('customer_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_company', to='app.company', verbose_name='Customer-Company')),
                ('partner_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_company', to='app.company', verbose_name='Partner-Company')),
            ],
            options={
                'ordering': ['product_name'],
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_nickname', models.CharField(max_length=100, verbose_name='Nick Name')),
                ('is_site_manager', models.BooleanField(default=True, verbose_name='Is SiteManager')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['manager_nickname'],
            },
        ),
        migrations.CreateModel(
            name='DataCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datacenter_name', models.CharField(max_length=255, verbose_name='DataCenter Name')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Address')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update At')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
            options={
                'ordering': ['datacenter_name'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255, verbose_name='Customer Name')),
                ('customer_telephone', models.CharField(default='-', max_length=255, verbose_name='Customer Telephone')),
                ('customer_email', models.CharField(default='-', max_length=150, verbose_name='Customer Email')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update At')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='Remark')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company', verbose_name='Company')),
            ],
            options={
                'ordering': ['customer_name'],
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=255, verbose_name='Branch Name')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Address')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update At')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
            options={
                'ordering': ['branch_name'],
            },
        ),
        migrations.AddField(
            model_name='company',
            name='manager',
            field=models.ManyToManyField(blank=True, null=True, to='app.manager', verbose_name='Site-Manager'),
        ),
    ]
