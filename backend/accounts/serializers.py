from accounts.models import MyUser
from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate

# Class for admin to update user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id', 'username', 'password', 'email', 'fullname', 'is_active', 'date_joined', 'is_admin', 'is_author')
        read_only_fields = ('date_joined', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Class for admin to get user info
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id', 'username', 'email', 'fullname', 'is_active', 'date_joined', 'is_admin', 'is_author')
        read_only_fields = ('date_joined',  'id')
        extra_kwargs = {'password': {'write_only': True}}


# Serializer for authenticated user
class AuthenticatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'fullname', 'date_joined')
        read_only_fields = ('date_joined', 'id')

# Serializer for set password
class ChangePasswordUserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)

    class Meta:
        fields = ('password')
        extra_kwargs = {'password': {'write_only': True}}

# serializer for login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        user = None
        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None
        if email is not None and password is not None:
            user = self._validate_email(email, password)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

