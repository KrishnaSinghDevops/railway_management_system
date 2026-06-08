from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('django-admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('railway_app.urls')),
    path('', include('admin_panel.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)