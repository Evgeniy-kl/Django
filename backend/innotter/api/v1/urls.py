from rest_framework import routers

from innotter.api.v1.views import TagViewSet, PageViewSet, PostViewSet

router = routers.SimpleRouter()

router.register('tag', TagViewSet, basename='tag')
router.register('page', PageViewSet, basename='page')
router.register('post', PostViewSet, basename='post')

urlpatterns = router.urls
