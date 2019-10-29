from rest_framework import routers
from .speagle import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewset)