from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator

User = get_user_model()
hex_validator = RegexValidator(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='HEX #FFD700')

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created')
    class Meta:
        abstract = True
        ordering = ['-created_at']

class PageMeta(AuditModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    url_path = models.CharField(max_length=255, blank=True, db_index=True, verbose_name='URL', help_text='/')
    meta_title = models.CharField(max_length=70, verbose_name='Title')
    meta_description = models.TextField(max_length=160, verbose_name='Description')
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_title = models.CharField(max_length=120, blank=True)
    og_description = models.TextField(max_length=300, blank=True)
    og_image = models.ImageField(upload_to='seo/og/', blank=True, null=True)
    theme_color = models.CharField(max_length=7, default='#F1D07A', validators=[hex_validator])
    robots_noindex = models.BooleanField(default=False)
    class Meta:
        verbose_name='SEO'
        unique_together=('content_type','object_id')
    def __str__(self): return self.url_path or self.meta_title

class Chapter(AuditModel):
    name = models.CharField(max_length=100, verbose_name='Назва глави')
    slug = models.SlugField(unique=True, help_text='gold-mask')
    order = models.IntegerField(default=0)
    class Meta:
        verbose_name='Глава'
        verbose_name_plural='Глави'
        ordering=['order']
    def __str__(self): return self.name

class Boss(AuditModel):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='bosses')
    name = models.CharField(max_length=100, verbose_name='Бос')
    mode = models.CharField(max_length=50, default='Соло/Паті')
    diff = models.CharField(max_length=50, default='Середній/Високий')
    order = models.IntegerField(default=0)
    class Meta:
        verbose_name='Бос'
        verbose_name_plural='Боси'
        ordering=['order']
    def __str__(self): return f"{self.chapter.name} - {self.name}"

class LootItem(AuditModel):
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE, related_name='items')
    column_name = models.CharField(max_length=100, verbose_name='Колонка', help_text='Лицар 68-65')
    item_name = models.CharField(max_length=200, verbose_name='Предмет')
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    order = models.IntegerField(default=0)
    class Meta:
        verbose_name='Предмет'
        verbose_name_plural='Предмети'
        ordering=['order']
    def __str__(self): return self.item_name
