from rest_framework import serializers
from .models import Person,Team
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username already exists")
        if data['email']:
            if User.objects.filter(username = data['email']).exists():
                raise serializers.ValidationError("Email already exists")
        return data
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_name'] # to get the dictionary of team_name

class PersonSerializer(serializers.ModelSerializer):
    team_info = serializers.SerializerMethodField() # variable for extra field
    class Meta:
        model = Person
        fields = '__all__'
        
    
    def get_team_info(self,obj):
        return "extra serializer field"
    
    def validate(self, data):
        spl_char = "!@#$%^&*()-_=+,:;<>?/|~"
        
        if any(c in spl_char for c in data['name']):
            SerializersError = serializers.ValidationError("Name should not contain special charecters")
            raise SerializersError
        if data['age']<18:
            SerializerError = serializers.ValidationError("Age should not be less than 18")
            raise SerializerError
        return data