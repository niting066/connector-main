from django.urls import path
from userdata import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('user/registration', views.user_data_save, name='signup'),
    path('upload', views.upload, name='upload'),
    path('profile/<str:pk>/', views.user_account, name='user_account'),
    path('setting', views.account_setting, name='setting'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('follow', views.follow, name='follow'),
    path('search', views.search_result, name='search'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
