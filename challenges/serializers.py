from rest_framework import serializers
from challenges.models import ChallengeModel, TasksModel, MemberModel
from users.models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [ 'id', 'username']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = MemberModel
        fields = ['id',  'user']


class ChallengeDetailSerializers(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = MemberSerializer(read_only=True)

    class Meta:
        model = ChallengeModel
        fields = ['id', 'name', 'image', 'goal', 'owner', 'members']

class ChallengeListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = ChallengeModel
        fields = ['id', 'owner', 'name', 'goal', 'image']


class JoinChallengeSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True)

    class Meta:
        model = ChallengeModel
        fields = ['id', 'name', 'info', 'members']


class ChallengeSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = ChallengeModel
        fields  = '__all__'

class UpdateChallengeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    info = serializers.CharField(write_only=True, required=True)
    goal = serializers.CharField(write_only=True, required=True)
    image = serializers.ImageField(write_only=True, required=True)
    mission = serializers.CharField(write_only=True, required=True)
    start_at = serializers.DateField(write_only=True, required=True)
    full_time = serializers.IntegerField(write_only=True, required=True)
    status = serializers.BooleanField(write_only=True, required=True)
    #limited_tasks = serializers.CharField(write_only=True, required=True)
    #limited_time = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = ChallengeModel
        fields ='__all__'


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.info = validated_data.get('info', instance.info)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.mission = validated_data.get('mission', instance.mission)
        instance.start_at = validated_data.get('start_at', instance.start_at)
        instance.full_time = validated_data.get('full_time', instance.full_time)
        instance.status = validated_data.get('status', instance.status)
        #instance.limited_tasks = validated_data.get('limited_tasks', instance.limited_tasks)
        #instance.limited_time = validated_data.get('limited_time', instance.limited_time)

        instance.save()
        return instance