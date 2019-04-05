from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import serializers

from .test_data import (
    valid_user, user_without_password, valid_user2, user_without_email)

from ..models import User
from ..serializers import LoginSerializer


class LoginSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**valid_user)
        self.serializer_class = LoginSerializer
        self.serializer = self.serializer_class(data=valid_user)

    def test_serializer_can_validate_an_unregisterd_user(self):
        serializer = self.serializer_class(data=valid_user2)
        is_valid_data = serializer.is_valid()

        self.assertFalse(is_valid_data)

        self.assertRaisesMessage(
            serializers.ValidationError,
            'User not found or account not active.', serializer.validate,
            valid_user2)

    def test_serializer_raises_an_exception_on_request_without_an_email(self):
        serializer = self.serializer_class(data=user_without_email)

        self.assertRaises(
            serializers.ValidationError, serializer.is_valid, 
            raise_exception=True)

        self.assertRaisesMessage(
            serializers.ValidationError,
            'An email address is required to log in.', serializer.validate,
            user_without_email)

    def test_serializer_raises_an_exception_on_request_without_password(self):
        serializer = self.serializer_class(data=user_without_password)

        self.assertRaises(
            serializers.ValidationError, 
            serializer.is_valid, raise_exception=True)

        self.assertRaisesMessage(
            serializers.ValidationError, 'A password is required to log in.',
            serializer.validate, user_without_password)
