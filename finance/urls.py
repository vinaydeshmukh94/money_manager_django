from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path(
        "add_category/", views.add_category_subcategory, name="add_category_subcategory"
    ),
    path("add_transaction/", views.add_transaction, name="add_transaction"),
]
