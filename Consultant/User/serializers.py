from abc import ABC

from rest_framework import serializers
from .models import *


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6, max_length=25)
    password_repetition = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6,
                                                max_length=25)
    private_profile = serializers.BooleanField(default=False, allow_null=False)

    def create(self, validated_data):
        del validated_data['password_repetition']
        return UserProfile.objects.create(**validated_data)

    def validate_password(self, password):
        """
        Check the password regex.
        """
        # TODO WRITE PASSWORD VALIDATION
        return password

    def validate(self, data):
        """
        Check the password regex.
        """
        if data["password_repetition"] != data["password"]:
            raise serializers.ValidationError("Repetition of password is not same with password!")
        return data

    def validate_phone_number(self, phone_number):
        """
        Check the phone_number regex.
        """
        import re
        if len(phone_number) != 11 or re.search(r"09[0-9]{9}", phone_number) is None:
            raise serializers.ValidationError("Format of phone_number is not true")
        return phone_number

class ConsultanSignupSerializer(UserSignupSerializer):
    consultant_types = (
        ('Lawyer', 'Lawyer')
    )
    consultant_type = serializers.ChoiceField(choices=consultant_types)

    def create(self, validated_data):
        del validated_data['password_repetition'], validated_data['consultant_type']
        return Lawyer.objects.create(**validated_data)

    class Meta:
        abstract = True

class LawyerSignupSerializer(ConsultanSignupSerializer):
    certificate = serializers.FileField(required=True, allow_null=False, allow_empty_file=False)

    def validate_certificate(self, certificate_file):
        # TODO CHECK CERTIFICATE EXTENSION
        return  certificate_file
