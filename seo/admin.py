from django.contrib import admin
from django.utils.html import format_html
from.models import PageMeta, Chapter, Boss, LootItem

# === ТВОЇ НОВІ МОДЕЛІ ДЛЯ ХРАМУ ===

class LootItemInline(admin.TabularInline):
    model = LootItem
    extra = 1
    fields = ('column_name', 'item_name', 'icon', 'order')
    ordering = ('order',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)

@admin.register(Boss)
class BossAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter', 'mode', 'diff', 'order')
    list_filter = ('chapter',)
    ordering = ('order',)
    inlines = [LootItemInline]
    fields = ('chapter', 'name', 'mode', 'diff', 'order', 'created_by')
    readonly_fields = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# === ТВІЙ СТАРИЙ КОД З SEO - БЕЗ ЗМІН ===

class PageMetaInline(admin.StackedInline):
    """
    Inline для зручного редагування SEO прямо на сторінці основного об'єкта.
    Підключіть цей inline до будь-якого ModelAdmin: inlines = [PageMetaInline]
    """
    model = PageMeta
    extra = 0
    max_num = 1
    can_delete = True
    verbose_name = 'SEO та Open Graph'
    verbose_name_plural = 'SEO та Open Graph'

    fieldsets = (
        ('Основна сторінка', {
            'fields': ('url_path',),
            'description': 'Для статичних сторінок вкажіть URL. Для динамічних об\'єктів це поле залишається порожнім — прив\'язка йде автоматично.'
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'robots_noindex',
            ),
            'description': 'Базові мета-теги для Google та інших пошукових систем.'
        }),
        ('Open Graph (Facebook, Discord, Telegram)', {
            'fields': (
                'og_title',
                'og_description',
                'og_image',
                'theme_color',
            ),
            'classes': ('collapse',),
            'description': 'Налаштування для красивих прев\'ю при поширенні посилання у соцмережах. Блок можна згорнути.'
        }),
        ('Аудит', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by', 'content_type')

@admin.register(PageMeta)
class PageMetaAdmin(admin.ModelAdmin):
    """
    Окремий адмін-клас для прямого керування всіма SEO-записами.
    Аналог твого старого Django-адміністрування з скріна, тільки в стилі Храму.
    """
    list_display = ('meta_title', 'url_path', 'content_object_link', 'robots_noindex', 'created_by', 'updated_at', 'og_image_preview')
    list_filter = ('robots_noindex', 'created_at', 'content_type')
    search_fields = ('meta_title', 'meta_description', 'url_path', 'meta_keywords')
    readonly_fields = ('created_at', 'updated_at', 'og_image_preview', 'created_by')
    list_editable = ('robots_noindex',)
    save_on_top = True

    fieldsets = (
        ('Прив\'язка сторінки', {
            'fields': (
                ('content_type', 'object_id'),
                'url_path',
            ),
            'description': 'Вкажіть або URL, або прив\'язку до об\'єкта (Новина, Товар тощо). Не заповнюйте обидва одночасно.'
        }),
        ('SEO — для пошукових систем', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'robots_noindex',
            ),
        }),
        ('Open Graph — для соцмереж', {
            'fields': (
                'og_title',
                'og_description',
                'og_image',
                'og_image_preview',
                'theme_color',
            ),
            'classes': ('collapse',),
            'description': 'Ці поля відповідають за те, як виглядатиме посилання у Discord, Facebook, Telegram. Якщо OG Title/Description порожні — підтягнеться звичайний Title/Description.'
        }),
        ('Службова інформація', {
            'fields': (
                'created_by',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def content_object_link(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return obj.url_path or '—'
    content_object_link.short_description = 'Прив\'язаний об\'єкт'

    def og_image_preview(self, obj):
        if obj.og_image:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 8px; border: 1px solid #F1D07A;" />', obj.og_image.url)
        return 'Немає зображення'
    og_image_preview.short_description = 'Прев\'ю OG зображення'

    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, PageMeta) and not instance.created_by:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()