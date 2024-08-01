from django.db import models
from users.models import UserModel
from datetime import date, timedelta
import uuid

class ChallengeModel(models.Model):
    name = models.CharField(max_length=128)
    info = models.TextField()
    goal = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    mission = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    start_at = models.DateField()   
    full_time = models.IntegerField()
    end_at = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True) # True - Public, False - Private
    secret_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'challenges'
        verbose_name = 'challenge'
        verbose_name_plural = 'challenges'


    def challenge_end_at(self):
        if not self.end_at:
            end_at = self.start_at + timedelta(days=self.full_time)
            self.end_at = end_at


    def check_star_at(self):
        return self.start_at >= date.today()

    def clean(self):
        self.check_star_at()
        self.challenge_end_at()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(ChallengeModel, self).save(*args, **kwargs)


class TasksModel(models.Model):
    limited_time = models.IntegerField()
    limited_tasks = models.TextField()

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Tasks'
        verbose_name_plural = 'Task'    

class MemberModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    challenge = models.ForeignKey(ChallengeModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} * {self.challenge.name}"

    
    class Meta:
        db_table = 'Members'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'