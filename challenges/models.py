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
    is_different = models.BooleanField(default=True) # Kunlik vazifalarnimg bir xil yoki har xilligi. True - har xil
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    start_at = models.DateField()   
    full_time = models.IntegerField() # Challenjning umumiy vaqti yani davom etish muddati
    end_at = models.DateField(null=True, blank=True)
    limited_time = models.IntegerField() # Qancha vaqtdqa yangi vazifa berilishi.
    status = models.BooleanField(default=True, null=True, blank=True) # True - Public, False - Private
    secret_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.id

    class Meta:
        db_table = 'challenges'
        verbose_name = 'challenge'
        verbose_name_plural = 'challenges'


    @property
    def full_name(self):
        return self.name

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
    challenge = models.ForeignKey(ChallengeModel,related_name='daily_tasks', on_delete=models.CASCADE)
    due_date = models.DateField()
    tasks = models.TextField()

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Tasks'
        verbose_name_plural = 'Task'    

    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created
            # Calculate the due_date based on the limited_time of the challenge
            latest_task = TasksModel.objects.filter(challenge=self.challenge).order_by('-due_date').first()
            if latest_task:
                self.due_date = latest_task.due_date + timedelta(days=self.challenge.limited_time)
            else:
                self.due_date = self.challenge.start_at + timedelta(days=selfchallenge.limited_time)
        super(TasksModel, self).save(*args, **kwargs)



class MemberModel(models.Model):
    user = models.ForeignKey(UserModel,  on_delete=models.CASCADE)
    challenge = models.ForeignKey(ChallengeModel,  related_name='members',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('challenge', 'user')
        db_table = 'Members'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return f"{self.user.username} in {self.challenge.name}"
        