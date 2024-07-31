from rest_framework import serializers
from challenges.models import ChallengeModel

class UpdateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    info = serializers.TextField(write_only=True, required=True,max_digits=7,  decimal_places=2)
    missions = serializers.TextField(write_only=True, required=True)
    daily_missions = serializers.TextField(write_only=True, required=True)
    owner = serializers.CharField(write_only=True, required=True)
    start_at = serializers.DateField(write_only=True, required=True)
    full_time = serializers.IntegerField(write_only=True, required=True)
    limited_time = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = ChallengeModel
        fields ='__all__'


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.info = validated_data.get('info', instance.info)
        instance.missions = validated_data.get('missions', instance.missions)
        instance.daily_missions = validated_data.get('daily_missions', instance.daily_missions)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.start_at = validated_data.get('start_at', instance.start_at)
        instance.full_time = validated_data.get('full_time', instance.full_time)
        instance.limited_time = validated_data.get('limited_time', instance.limited_time)

        instance.save()
        return instance