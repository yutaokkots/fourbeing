from django.urls import path, include
from . import views

#from knox import views as knox_views
#from fourbeing.views import LoginView, CreateUserView, ManageUserView, LoginAPI

# import routers
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    # api/fourbeing/
    path('fourbeing/', views.index, name="index" ),
    path('fourbeing/create/', views.createpost, name="createpost" ),
    path('fourbeing/<int:post_id>/', views.post_detail, name='post_detail'),
    path('fourbeing/<int:post_id>/update/', views.post_update, name='post_update'),
    path('fourbeing/<int:post_id>/delete/', views.post_update, name='post_delete'),
    path('fourbeing/<int:post_id>/love/', views.post_love, name='post_love'),

    path('fourbeing/<int:post_id>/comments/', views.reply_index, name='reply_detail'),
    path('fourbeing/<int:post_id>/comments/create/', views.reply_create, name='reply_create'),
    #path('fourbeing/<int:post_id>/comments/<int:reply_id>/create/', views.reply_create, name='reply_create'),
    path('fourbeing/<int:post_id>/comments/<int:reply_id>/update/', views.reply_update, name='reply_update'),
    path('fourbeing/<int:post_id>/comments/<int:reply_id>/delete/', views.reply_update, name='reply_delete'),
    path('fourbeing/<int:post_id>/comments/<int:reply_id>/love/', views.reply_love, name='reply_love'),
    
    path('fourbeing/test/', views.test, name='test'),

]                   #/api/fourbeing/36/comments/4/update/