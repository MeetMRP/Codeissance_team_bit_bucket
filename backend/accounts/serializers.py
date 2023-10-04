from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist

class RegisterSerializer(serializers.ModelSerializer):
    company_code = serializers.CharField(write_only=True)
    class Meta:
        model = AccountsUser
        fields = ['email', 'name', 'password',  'phone_number', 'profile_picture', 'role', 'company_code']

    def create(self, validated_data):
        company_code = validated_data.pop('company_code', None)
        hash_pass = make_password(validated_data.pop('password', None))

        # Fetch the Company instance using the provided company_code
        try:
            company = Company.objects.get(id=company_code)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"company_code": "Invalid company code provided."})

        # Create the AccountsUser instance and assign the Company instance to it
        user = AccountsUser.objects.create(password=hash_pass, company=company, **validated_data)

        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    user_id = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = AccountsUser
        fields = ['email', 'password', 'user_id']

    def validate(self, attrs):
        email = attrs.get('email', )
        password = attrs.get('password', )

        try:
            request_user = AccountsUser.objects.get(email=email)
        except Exception as e:
            raise AuthenticationFailed('Invalid credintials, try again')   
        
        if not check_password(password, request_user.password):
            raise AuthenticationFailed('Password invalid, try again')        
        
        return {
            'email': request_user.email,
            'user_id': request_user.id
        }
    
class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Feedback
        fields = ['insight', 'recommendation', 'user_name']
    
    def create(self, validated_data):
        user_name = validated_data.pop('user_name', None)

        try:
            receiver = AccountsUser.objects.get(name=user_name)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"user_name": "Invalid user name provided."})

        feedback = Feedback.objects.create(receiver=receiver, **validated_data)

        return feedback
 