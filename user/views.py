from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404

from .models import Users
from .serializer import UsersSerializer

class UserListCreateAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        users = Users.objects.exclude(delete_flag=True)
        serializer = UsersSerializer(instance=users, many=True)
        if not serializer.is_valid:
            raise ValidationError(serializer.errors)

        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

class UserRetrieveUpdateDeleteAPIView(views.APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            user = Users.objects.get(id=pk, delete_flag=False)
        except Users.DoesNotExist:
            raise NotFound()

        serializer = UsersSerializer(instance=user)
        if not serializer.is_valid:
            raise ValidationError(serializer.errors)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        try:
            user = Users.objects.get(id=pk, delete_flag=False)
        except Users.DoesNotExist:
            raise NotFound()

        serializer = UsersSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        user = get_object_or_404(Users, pk=pk)
        user.delete_flag = True
        user.save()

        return Response(status.HTTP_204_NO_CONTENT)