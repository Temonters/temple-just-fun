from django.shortcuts import render
from .models import Chapter

def home(request):
    chapters = Chapter.objects.prefetch_related('bosses__items').order_by('order')
    active_slug = request.GET.get('chapter')
    if active_slug:
        active = chapters.filter(slug=active_slug).first()
    else:
        active = chapters.first()
    return render(request, 'base.html', {
        'chapters': chapters,
        'active_chapter': active
    })