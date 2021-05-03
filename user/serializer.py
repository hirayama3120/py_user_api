from rest_framework import serializers

from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'first_name',
            'last_name',
            'age',
            'mail_address',
            'delete_flag',
            'created_add',
            'updated_add'
        ]
        extra_kwargs = {
            'id': {
                'required': True,
            },
            'first_name': {
                'required': True,
                'allow_blank': False,
                'max_length': 32,
            },
            'last_name': {
                'required': True,
                'allow_blank': False,
                'max_length': 32,
            },
            'mail_address': {
                'required': True,
                'allow_blank': False,
            },
        }

