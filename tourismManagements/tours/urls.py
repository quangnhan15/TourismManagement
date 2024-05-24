from django.urls import path, re_path, include
from . import views
# from .admin import admin_site
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tours', views.TourViewset)
router.register('tour_details', views.TourDetailViewset)
router.register(r'users', views.UserViewSet, basename='users')
router.register('comments', views.CommentViewSet, basename='comments')
#/tours/ Get
#/tours/ Post
#/tours/{tour_id}/ - Get xem chi tiet
#/tours/{tour_id}/ - Cap nhat
#/tours/{tour_id}/ - Xoa

urlpatterns = [
    path('', include(router.urls)),
    # path('', views.index, name="index"),
    # path('admin/', admin_site.urls)
]
