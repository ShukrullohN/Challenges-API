from django.db import models
from users.models import UserModel
from datetime import date, timedelta

class ChallengeModel(models.Model):
    name = models.CharField(max_length=128)
    info = models.TextField()
    goal = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')
    mission = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    start_at = models.DateField()   
    full_time = models.IntegerField()
    end_at = models.DateField(null=True, blank=True)
    members_count = models.InegerField()
    status = models.BooleanField(default=True) # True - Public, False - Private
    secret_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def challenge_end_at(self):
        end_at = start_at + timedelta(days=full_time)
        self.end_at = end_at

    def get_members(self):
        data = ActiveUserModel.objects.filter(challenge = self.name)
        return data.user



    def check_star_at(self):
        return self.start_at > date.today()


class TasksModel(models.Model):
    limited_time = models.IntegerField()
    limited_tasks = models.TextField()

    limited_time = models.IntegerField()
    

class ActiveUserModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    challenge = models.ForeignKey(ChallengeModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} * {self.challenge.name}"

    
