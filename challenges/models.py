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
    status = models.BooleanField(default=True) # True - Public, False - Private
    secret_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    secret_password = models.CharField(max_length=128, null=True, blank=True)

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

    def check_private(self):
        if self.status and self.secret_password:
            raise ValidationError('Public challenges should not have a secret password.')
        if not self.status and not self.secret_password:
            raise ValidationError('Private challenges must have a secret password.')


    def challenge_end_at(self):
        if not self.end_at:
            end_at = self.start_at + timedelta(days=self.full_time)
            self.end_at = end_at



    def check_time(self):
        if self.start_at and self.end_at:
            if self.start_at >= self.end_at:
                raise ValidationError("Start time must be before end time.")

    def clean(self):
        self.check_private()
        self.check_time()
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
        db_table = 'tasks'
        verbose_name = 'Tasks'
        verbose_name_plural = 'Task'    




class MemberModel(models.Model):
    user = models.ForeignKey(UserModel,  on_delete=models.CASCADE)
    challenge = models.ForeignKey(ChallengeModel,  related_name='members',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('challenge', 'user')
        db_table = 'members'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return f"{self.user.username} in {self.challenge.name}"
        