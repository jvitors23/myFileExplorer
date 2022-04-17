from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects"""

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'root_folder')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'first_name': {'required': True}
        }
        read_only_fields = ('id', 'root_folder')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['root_folder'] = user.root_folder.id
        token['username'] = user.username
        token['first_name'] = user.first_name
        return token
