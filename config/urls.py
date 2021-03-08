from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from user.urls import router as user_router

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include(user_router.urls))
]
