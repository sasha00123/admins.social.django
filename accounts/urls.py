from django.urls import path, include

from accounts.views import logout_view

views = [
    path('logout', logout_view, name='logout')
]

urlpatterns = [
    path('accounts/', include(views))
]
