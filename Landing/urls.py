
from django.urls import path
from .views import *

urlpatterns = [
    path("", render_all_users, name="home_page"),
    path("register/", register_user, name="register"),
    path("login/", user_login, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
    path("<id>/del_user/", delete_user_view, name="del_user"),
    path("<id>/edit", edit_user_view, name="edit_user")

]


