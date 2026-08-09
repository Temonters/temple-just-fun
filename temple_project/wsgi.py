from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temple_project.settings')
application = get_wsgi_application()

# Авто-міграція для Vercel /tmp
if os.getenv("VERCEL") == "1":
    try:
        from django.core.management import call_command
        call_command('migrate', '--run-syncdb', verbosity=0)
        print("✅ DB migrated to /tmp/db.sqlite3")
    except Exception as e:
        print(f"⚠️ Migrate error: {e}")