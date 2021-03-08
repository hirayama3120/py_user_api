import django_filters
from rest_framework import viewsets, filters

from .models import Users
from .serializer import UsersSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer