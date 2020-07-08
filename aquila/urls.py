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
from assign_rights.views import (AquilaLoginView, GroupingCreateView,
                                 GroupingDetailView, GroupingListView,
                                 GroupingUpdateView, LoggedInView,
                                 RightsAssemblerView)
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rights-assemble/', RightsAssemblerView.as_view(), name='rights-assemble'),
    path('groupings/', GroupingListView.as_view(), name="groupings-list"),
    path('groupings/<int:pk>/', GroupingDetailView.as_view(), name="groupings-detail"),
    path('groupings/create/', GroupingCreateView.as_view(), name="groupings-create"),
    path('groupings/<int:pk>/edit/', GroupingUpdateView.as_view(), name="groupings-update"),
    path('login/', AquilaLoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page="/login"), name="logout"),
    path('logged-in/', LoggedInView.as_view(), name="logged-in")
]
