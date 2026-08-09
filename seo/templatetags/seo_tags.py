
from django import template
from django.contrib.contenttypes.models import ContentType
register = template.Library()
@register.inclusion_tag('includes/render_meta.html', takes_context=True)
def render_seo(context, obj=None):
    from ..models import PageMeta
    request = context.get('request')
    meta = None
    if obj:
        ct = ContentType.objects.get_for_model(obj.__class__)
        meta = PageMeta.objects.filter(content_type=ct, object_id=obj.pk).first()
    elif request:
        meta = PageMeta.objects.filter(url_path=request.path).first()
        if not meta and request.path.endswith('/'):
            meta = PageMeta.objects.filter(url_path=request.path.rstrip('/')).first()
    return {'meta': meta, 'request': request}
