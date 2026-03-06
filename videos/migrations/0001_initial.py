from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=280, unique=True)),
                ('description', models.TextField(blank=True)),
                ('video_file', models.FileField(upload_to='videos/')),
                ('thumbnail', models.ImageField(blank=True, upload_to='thumbnails/')),
                ('visibility', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='videos', to='categories.category')),
                ('primary_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_videos', to='categories.category')),
            ],
            options={
                'ordering': ['-is_featured', '-created_at'],
                'indexes': [models.Index(fields=['visibility', '-created_at'], name='videos_video_visibil_040ca2_idx')],
            },
        ),
    ]
