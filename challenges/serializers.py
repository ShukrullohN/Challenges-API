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
        fields = ['id', 'name', 'image', 'goal', 'owner']




class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel
        fields = ['id', 'due_date', 'tasks']


class BulkUpdateListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        task_mapping = {tasks.id: tasks for tasks in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform updates
        ret = []
        for tasks_id, data in data_mapping.items():
            tasks = task_mapping.get(tasks_id, None)
            if task is not None:
                ret.append(self.child.update(tasks, data))

        return ret



class MyChallengeSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    daily_tasks = DailyTaskSerializer(many=True, read_only=True)

    class Meta:
        model = ChallengeModel
        fields = ['id', 'owner', 'name', 'goal', 'image',  'daily_tasks']

class ChallengeListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = ChallengeModel
        fields = ['id', 'owner', 'name', 'goal', 'image', 'status','created_at',]



class SecretKeySerializer(serializers.Serializer):
    secret_key = serializers.CharField()

class SecretPasswordSerializer(serializers.Serializer):
    secret_password = serializers.CharField()


class FillTaskSerializer(serializers.Serializer):
    tasks = serializers.CharField()

    def validate(self, data):
        challenge_id = self.context['view'].kwargs['pk']
        challenge = ChallengeModel.objects.get(id=challenge_id)
        return data


class JoinChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallengeModel
        fields = ['id', 'name', 'info']


class ChallengeSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = ChallengeModel
        fields  = '__all__'

    def validate(self, data):
        if data.get('status') and data.get('secret_password'):
            raise serializers.ValidationError('Public challenges should not have a secret password.')
        if not data.get('status') and not data.get('secret_password'):
            raise serializers.ValidationError('Private challenges must have a secret password.')
        return data


class UpdateChallengeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    info = serializers.CharField(write_only=True, required=True)
    goal = serializers.CharField(write_only=True, required=True)
    image = serializers.ImageField(write_only=True, required=True)
    mission = serializers.CharField(write_only=True, required=True)
    start_at = serializers.DateField(write_only=True, required=True)
    full_time = serializers.IntegerField(write_only=True, required=True)
    status = serializers.BooleanField(write_only=True, required=True)
    limited_time = serializers.IntegerField(write_only=True, required=True)

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
        instance.limited_time = validated_data.get('limited_time', instance.limited_time)

        instance.save()
        return instance


class UpdateTaskSerializer(serializers.ModelSerializer):
    tasks = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = TasksModel
        fields =['tasks']

    def update(self, instance, validated_data):
        instance.tasks = validated_data.get('tasks', instance.tasks)

        instance.save()
        return instance