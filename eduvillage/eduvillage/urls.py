from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ✅ correct app name
  

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
  # Serve media files (user uploaded files like avatars)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)