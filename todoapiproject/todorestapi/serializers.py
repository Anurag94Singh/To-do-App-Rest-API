from rest_framework import serializers

from .models import Users,Tasks,UserTaskMapping,TaskMapping,Status

from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id','name')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TasksSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    createdby = UsersSerializer(read_only=True)
    class Meta:
        model = Tasks
        fields = '__all__'


class TaskMappingSerializer(serializers.ModelSerializer):
    student = UsersSerializer(read_only=True)
    task = TasksSerializer(read_only=True)
    class Meta:
        model = TaskMapping
        fields = '__all__'

# class StudentTasksSerializer(serializers.ModelSerializer):
#     # status = serializers.PrimaryKeyRelatedField(read_only=True)
#     # createdby = serializers.PrimaryKeyRelatedField(read_only=True)
#     users = UsersSerializer(read_only=True)
#     username = serializers.StringRelatedField(read_only=True)
#     taskid = serializers.SlugRelatedField(read_only=True, slug_field='taskid')
#     taskname = serializers.StringRelatedField(read_only=True)
#     userid = serializers.SlugRelatedField(read_only=True, slug_field='userid')
#     class Meta:
#         model = UserTaskMapping
#         fields = '__all__'
