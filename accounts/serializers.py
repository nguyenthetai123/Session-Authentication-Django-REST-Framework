from rest_framework import serializers
from accounts.models import UserAccount

class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    comfirm_password= serializers.CharField(write_only=True)
    class Meta:
        model= UserAccount
        fields = ["email", "name", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm_Password doesn't match.")
        return attrs

    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
          raise serializers.ValidationError('user with this Email already exists.')
        return value

    def create(self, validated_data):
        user = UserAccount.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance