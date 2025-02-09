from django.urls import path
from .views import login_view, signup_view, home, dashboard_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name='logout'),
    path("signup/", signup_view, name="signup"),
    path("dashboard/", dashboard_view, name="dashboard")
]
