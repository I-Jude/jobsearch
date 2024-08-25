
from django.contrib import admin
from django.urls import path , include
from jobsearch import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login_1, name='login_1'),
    path('jobsearch/', include('jobsearch.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
