from rest_framework import routers

from user.api.v1.views import UserViewSet

router = routers.SimpleRouter()

router.register('registration', UserViewSet, basename='registration')

urlpatterns = router.urls
