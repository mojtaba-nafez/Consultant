# Generated by Django 2.2 on 2021-04-11 15:40

import User.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[User.models.validate_phone_number])),
                ('avatar', models.FileField(blank=True, null=True, upload_to='files/user_avatar', validators=[User.models.validate_avatar_extension])),
                ('user_type', models.CharField(choices=[('Lawyer', 'Lawyer'), ('normal_user', 'normal_user')], default='normal_user', max_length=32)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
         migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('private_profile', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'UserProfile',
            },
            bases=('User.baseuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ConsultantProfile',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('private_profile', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('certificate', models.FileField(blank=True, null=True, upload_to='files/lawyers/certificate')),
                ('my_secretaries', models.ManyToManyField(to='User.UserProfile')),
            ],
            options={
                'verbose_name_plural': 'ConsultantProfile',
            },
            bases=('User.baseuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
