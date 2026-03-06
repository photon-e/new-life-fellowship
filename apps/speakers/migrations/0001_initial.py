from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('slug', models.SlugField(max_length=160, unique=True)),
                ('photo', models.ImageField(blank=True, upload_to='speakers/')),
                ('bio', models.TextField(blank=True)),
            ],
            options={'ordering': ['name']},
        ),
    ]
