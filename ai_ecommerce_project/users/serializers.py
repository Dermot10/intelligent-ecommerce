from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password during user creation
        user = User.objects.create_user(**validated_data)
        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Accept nested user data

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'address', 'city', 'postal_code']

    def create(self, validated_data):
        # Extract user data and delegate user creation to UserSerializer
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()  # Create the User

        # Create the Customer profile linked to the User
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        # Update user data using UserSerializer
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(
            instance=instance.user, data=user_data, partial=True
        )
        if user_serializer.is_valid():
            user_serializer.save()

        # Update customer-specific fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
