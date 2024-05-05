from django.urls import path
from .views import *
from django.views.defaults import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('siginup/', SignUpView.as_view(), name='siginup'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

]