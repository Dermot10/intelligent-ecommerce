from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'address', 'city', 'postal_code']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)

        # create customer profile linked a user
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        # update user data
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(
            instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        # update customer data
        for attr, value in validated_data.items():
            setattr(user_serializer, attr, value)
        instance.save()

        return instance
