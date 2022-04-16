from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.index,name="login"),
    path("home",views.home,name="home"),
    path("logout",LogoutView.as_view(),name="logout"),
    path("<int:pk>/update",views.DataUpdateView.as_view(),name="update"),
    path("<int:pk>/edit",views.edit.as_view(),name="edit"),
    path("export",views.export,name="export"),
    path("export_filter",views.export_filtered,name="export-filter"),
    path("filter",views.filter,name="filter"),
    path("<int:pk>/cancel",views.cancel.as_view(),name="cancel"),
    path("", include('pwa.urls')),
]