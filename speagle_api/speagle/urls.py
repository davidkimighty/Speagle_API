from rest_framework import routers
from .api import SpeagleViewSet

router = routers.DefaultRouter()
router.register('api/speagle', SpeagleViewSet, 'speagle')

urlpatterns = router.urls
