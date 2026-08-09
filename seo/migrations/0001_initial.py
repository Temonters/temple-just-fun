
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]
    operations = [
        migrations.CreateModel(
            name='PageMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name="ID об'єкта")),
                ('url_path', models.CharField(blank=True, db_index=True, help_text="Наприклад: /about/ або /news/. Залиште порожнім, якщо прив'язуєте до об'єкта", max_length=255, verbose_name='URL сторінки')),
                ('meta_title', models.CharField(help_text='Рекомендовано до 60-70 символів. Відображається у вкладці браузера та пошуку Google', max_length=70, verbose_name='Meta Title')),
                ('meta_description', models.TextField(help_text='Рекомендовано до 160 символів. Короткий опис для пошукових систем', max_length=160, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(blank=True, help_text='Перерахуйте через кому, наприклад: pw, perfect world, just fun', max_length=255, verbose_name='Ключові слова (Keywords)')),
                ('og_title', models.CharField(blank=True, help_text='Якщо порожньо — буде використано звичайний Meta Title', max_length=120, verbose_name='OG Title')),
                ('og_description', models.TextField(blank=True, help_text='Якщо порожньо — буде використано звичайний Meta Description', max_length=300, verbose_name='OG Description')),
                ('og_image', models.ImageField(blank=True, help_text='Рекомендований розмір 1200x630px. Для Facebook, Discord, Telegram', null=True, upload_to='seo/og_images/', verbose_name='OG Зображення')),
                ('theme_color', models.CharField(default='#FFD700', help_text='HEX-код для підсвічування у Discord, мобільних браузерах. За замовчуванням #FFD700 (золотий)', max_length=7, validators=[django.core.validators.RegexValidator(message='Введіть коректний HEX-код кольору, наприклад #FFD700', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')], verbose_name='Колір теми (Theme Color)')),
                ('robots_noindex', models.BooleanField(default=False, help_text='Якщо увімкнено — сторінка не буде індексуватись Google (додасться meta robots=noindex)', verbose_name='Приховати від пошуку (noindex)')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Тип контенту')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Автор створення')),
            ],
            options={
                'verbose_name': 'SEO Метадані',
                'verbose_name_plural': 'SEO Метадані',
            },
        ),
        migrations.AddIndex(
            model_name='pagemeta',
            index=models.Index(fields=['url_path'], name='seo_pagemet_url_pat_4c8ddc_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='pagemeta',
            unique_together={('content_type', 'object_id')},
        ),
    ]
