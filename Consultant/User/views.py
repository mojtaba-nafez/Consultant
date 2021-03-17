from django.shortcuts import render
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
import coreapi

from .models import *


class TodoListViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        import re
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field(name='username', required=True, type='string'),
                coreapi.Field(name='email', required=True, type='string'),
                coreapi.Field(name='first_name', required=True, type='string'),
                coreapi.Field(name='last_name', required=True, type='string'),
                coreapi.Field(name='phone_number', required=True, type='string'),
                coreapi.Field(name='password', required=True, type='string'),
                coreapi.Field(name='password_repetition', required=True, type='string'),
            ]
            if re.search(r'consultant/', path) is not None:
                extra_fields += [
                    coreapi.Field(name='consultant_type', required=True, type='string'),
                ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class UserSignupAPI(APIView):
    schema = TodoListViewSchema()

    def post(self, request, format=None):
        try:
            serializer = serializers.UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return_data = serializers.UserConsultantSerializerReturnData(data=serializer.validated_data)
                return_data.is_valid(raise_exception=True)
                return Response(data=return_data.validated_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserConsultantLoginAPI(APIView):
    def post(self, request):
        try:
            serializer = serializers.UserConsultantLoginSerializer(data=request.data)
            if serializer.is_valid():
                # TODO: WRITE NATIVE QUERY HERE , USERNAME OR EMAIL
                user = list(UserProfile.objects.filter(username=serializer.validated_data['email_username']))
                if len(user) == 0:
                    user = UserProfile.objects.filter(email=serializer.validated_data['email_username'])
                if len(user) == 0:
                    return Response({'error': 'This user not found'}, status=status.HTTP_400_BAD_REQUEST)
                return_data = serializers.UserConsultantSerializerReturnData(user[0], many=False, partial=True)
                return Response(data=return_data.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConsultantSignupAPI(APIView):
    schema = TodoListViewSchema()
    def post(self, request, format=None):
        try:
            if request.data['consultant_type'] == 'Lawyer':
                serializer = serializers.LawyerSignupSerializer(data=request.data)
            else:
                return Response({'error': 'Type of consultant is not valid!!'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                return_data = serializers.UserConsultantSerializerReturnData(data=serializer.validated_data)
                return_data.is_valid(raise_exception=True)
                return Response(data=return_data.validated_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
