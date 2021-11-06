from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("secret-spy", views.secretSpy, name="secretSpy"),
    path("secret-spy/scott-tanner", views.secretSpyOne, name="secretSpyOne"),
    path("secret-spy/hamilton-nash", views.secretSpyTwo, name="secretSpyTwo"),
    path("secret-spy/nancydrew", views.secretSpyThree, name="secretSpyThree"),
    path("secret-spy/nancy-drew", views.secretSpyThreeAlt, name="secretSpyThreeAlt"),
    path("secret-spy/alex-cross", views.secretSpyFour, name="secretSpyFour"),
    path("secret-spy/shnaswhr/result", views.secretSpyFinal, name="secretSpyFinal"),
    path("<str:name>", views.user, name="user"),
    path("<str:name>/access", views.access, name="access"),
]