from django.urls import path
from hydroponicsapp import views

urlpatterns = [
    path("", views.login, name="Login"),
    path("Register", views.Register, name="Register"),
    path("ControlPanel", views.control_panel, name="ControlPanel"),
    path("Notifications", views.notification, name="Notifications"),
    path("History", views.history, name="History"),
    path("Logout", views.logout, name="Logout"),
    #path("edit/<str:id>", views.edit, name="edit"),
    path('delete/<str:id>', views.delete, name='delete'),
]
