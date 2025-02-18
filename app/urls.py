from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import DroneUserSignupView, DroneUserLoginView
from rest_framework.routers import DefaultRouter
from .views import ImageWithDetailsViewSet, GalleryViewSet

router = DefaultRouter()
router.register(r'images', ImageWithDetailsViewSet)
router.register(r'gallery', GalleryViewSet)

urlpatterns = [
    # Your other URL patterns
   
    path('signup/', DroneUserSignupView.as_view(), name='drone-user-signup'),
    path('login/', DroneUserLoginView.as_view(), name='drone-user-login'),
    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

