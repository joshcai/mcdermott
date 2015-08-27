from django.contrib.auth.models import User
from rest_framework import serializers

from models import McUser

class McUserSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = McUser
    fields = ('real_name', 'gender', 'birthday', 'class_year',  'utd_id', 'major', 'major2', 'minor', 
              'minor2', 'hometown', 'high_school', 'phone_number', 'id', 'pic')

class UserSerializer(serializers.ModelSerializer):
  profile = McUserSerializer(source='mcuser')

  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'email', 'profile')
