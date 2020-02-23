from django.urls import path
from .import views

urlpatterns = [
    path("", views.index),
    path("dashboard", views.dashboard),
    path("proc_reg", views.proc_reg),
    path("login", views.login),
    path("logout", views.logout),
    path("new", views.new),
    path("proc_job", views.proc_job),
    path("view/<int:id>", views.view),
    path("edit/<int:id>", views.edit),
    path("edit_proc", views.edit_proc),
    path("remove/<int:id>", views.remove),
]