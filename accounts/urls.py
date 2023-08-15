from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("activate/<uidb64>/<token>/",views.activate_view,name="activate"),
    path("",views.dashboard_view,name="dashboard"),
    path("dashboard/",views.dashboard_view,name="dashboard"),
    path("forgotPassword/",views.forgotPassword_view,name="forgotPassword"),
    path("resetPassword_validate//<uidb64>/<token>/",views.resetPassword_validate_view,name="resetPassword_validate"),
    path("resetpassword/",views.resetPassword_view,name="resetpassword")
]
