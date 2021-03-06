# Generated by Django 2.1.7 on 2019-04-23 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_follows'),
        ('articles', '0003_auto_20190415_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.DecimalField(decimal_places=0, max_digits=5)),
                ('rated_on', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_ratings', to='articles.Article')),
                ('ratings_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='profiles.Profile')),
            ],
            options={
                'ordering': ['-ratings'],
            },
        ),
    ]
