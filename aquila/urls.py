"""aquila URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from assign_rights.views import (AquilaLoginView, LoggedInView,
                                 RightsAssemblerView, RightsShellCreateView, RightsShellListView)
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', AquilaLoginView.as_view(template_name="users/login.html"), name="login"),
    path('api/rights-assemble/', RightsAssemblerView.as_view(), name='rights-assemble'),
    path('logout/', LogoutView.as_view(next_page="/login"), name="logout"),
    path('logged-in', LoggedInView.as_view(), name="logged-in"),
    path('rights/', RightsShellListView.as_view(), name='rights-list'),
    path('rights/create/', RightsShellCreateView.as_view(), name='rights-create')
]
