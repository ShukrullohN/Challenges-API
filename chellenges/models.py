from django.db import models
from shared.models import BaseModel
from users.models import UserModel

class ChallengeModel(BaseModel):
    name = models.CharField(max_length=128)
    info = models.TextField()
    missions = models.TextField()
    daily_missions = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=CASCADE)
    start_at = models.DateField()
    full_time = models.IntegerField()
    end_at = models.DateField(null=True, blank=True)
    limited_time = models.IntegerField()

    def __str__(self):
        return self.name
    
    def challenge_end_at(self):
        start_at

class ActiveUserModel(BaseModel):
    users = models.ForeignKey(UserModel, on_delete=CASCADE)
    challenges = models.ForeignKey(ChallengeModel, on_delete=CASCADE)
