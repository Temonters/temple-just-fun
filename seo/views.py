from django.shortcuts import render
from .models import Chapter

def home(request):
    try:
        chapters = Chapter.objects.all()
        active = chapters.first() if chapters.exists() else None
    except Exception as e:
        print(f"DB error: {e}")
        chapters = []
        active = None
    return render(request, 'base.html', {
        'chapters': chapters,
        'active_chapter': active
    })