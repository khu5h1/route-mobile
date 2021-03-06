# Generated by Django 3.0.5 on 2021-07-31 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('accounts', '0001_initial'),
        ('auth', '0013_auto_20210527_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularaccount',
            name='favourite_shops',
            field=models.ManyToManyField(blank=True, to='core.Shop'),
        ),
        migrations.AddField(
            model_name='regularaccount',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='regularaccount',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='billingaddress',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_user_address_check'),
        ),
    ]
