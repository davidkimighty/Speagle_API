from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('speagle.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]