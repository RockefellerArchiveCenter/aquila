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
                                 GroupingDeleteView, GroupingDetailView,
                                 GroupingListView, GroupingUpdateView,
                                 RightsAssemblerView, RightsShellCreateView,
                                 RightsShellDeleteView, RightsShellDetailView,
                                 RightsShellListView, RightsShellUpdateView)
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rights-assemble/', RightsAssemblerView.as_view(), name='rights-assemble'),
    path('', GroupingListView.as_view(), name="groupings-list"),
    path('groupings/<int:pk>/', GroupingDetailView.as_view(), name="groupings-detail"),
    path('groupings/create/', GroupingCreateView.as_view(), name="groupings-create"),
    path('groupings/<int:pk>/update/', GroupingUpdateView.as_view(), name="groupings-update"),
    path('groupings/<int:pk>/delete/', GroupingDeleteView.as_view(), name="groupings-delete"),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('login/', AquilaLoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page="/login"), name="logout"),
    path('rights/', RightsShellListView.as_view(), name='rights-list'),
    path('rights/create/', RightsShellCreateView.as_view(), name='rights-create'),
    path('rights/<int:pk>/update/', RightsShellUpdateView.as_view(), name='rights-update'),
    path('rights/<int:pk>/delete/', RightsShellDeleteView.as_view(), name='rights-delete'),
    path('rights/<int:pk>/', RightsShellDetailView.as_view(), name='rights-detail'),
]
