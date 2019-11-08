from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include('speagle.urls', namespace='speagle')),
]