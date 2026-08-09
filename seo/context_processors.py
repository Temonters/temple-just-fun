
def seo_meta(request):
    try:
        from .models import PageMeta
        meta = PageMeta.objects.filter(url_path=request.path).first()
        if not meta and request.path.endswith('/'):
            meta = PageMeta.objects.filter(url_path=request.path.rstrip('/')).first()
        return {'meta': meta}
    except:
        return {'meta': None}
