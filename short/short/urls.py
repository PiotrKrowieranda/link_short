"""
URL configuration for short project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from link.views import LoginFormView, LogoutView, Add_UserView, IndexView, LinkDetailsView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout-url"),
    path('add_user/', Add_UserView.as_view(), name="register"),
    path('', IndexView.as_view(), name='index'),
    path('my-links/<int:link_id>/', LinkDetailsView.as_view(), name='link-details'),
    path('<int:link_id>/', RedirectView.as_view(), name='redirect-view'),
]