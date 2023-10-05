from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
import os
import random

def get_random_image_from_folder(folder_path):
    images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return random.choice(images)

class RegisterSerializer(serializers.ModelSerializer):
    company_code = serializers.CharField(write_only=True)
    class Meta:
        model = AccountsUser
        fields = ['email', 'name', 'password',  'phone_number', 'profile_picture', 'role', 'company_code']

    def create(self, validated_data):
        company_code = validated_data.pop('company_code', None)
        hash_pass = make_password(validated_data.pop('password', None))
        image_name = get_random_image_from_folder('D:\Hackathons\Codeissance_team_bit_bucket\pics')
        profile_picture = validated_data.pop('profile_picture', os.path.join('profile_picture', image_name))

        # Fetch the Company instance using the provided company_code
        try:
            company = Company.objects.get(id=company_code)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"company_code": "Invalid company code provided."})

        # Create the AccountsUser instance and assign the Company instance to it
        user = AccountsUser.objects.create(password=hash_pass, company=company, profile_picture=profile_picture, **validated_data)

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
        fields = ['insight', 'rating', 'user_name']
    
    def create(self, validated_data):
        user_name = validated_data.pop('user_name', None)

        try:
            receiver = AccountsUser.objects.get(name=user_name)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"user_name": "Invalid user name provided."})

        feedback = Feedback.objects.create(receiver=receiver, **validated_data)

        return feedback
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountsUser
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['sender_name', 'insight', 'rating']
    
    def get_sender_name(self, obj):
        print(obj.sender)
        return obj.sender.name if obj.sender else None

class UserRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()

    class Meta:
        model = AccountsUser
        fields = ['name', 'average_rating']