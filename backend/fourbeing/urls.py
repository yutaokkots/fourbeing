from django.urls import path
from . import views

#from knox import views as knox_views
#from fourbeing.views import LoginView, CreateUserView, ManageUserView, LoginAPI


urlpatterns = [
    # api/fourbeing/
    path('fourbeing/', views.fourbeing_index, name="fourbeing_index" ),

    # api/fourbeing/create/
    path('fourbeing/create/', views.createpost, name="createpost" ),
    # api/fourbeing/:id/
    path('fourbeing/<int:post_id>/', views.post_detail, name='post_detail'),
    path('fourbeing/<int:post_id>/update/', views.post_update, name='post_detail'),
    path('fourbeing/<int:post_id>/delete/', views.post_delete, name='post_detail'),

    # api/fourbeing/
    path('fourbeing/test/', views.test, name='test'),

]