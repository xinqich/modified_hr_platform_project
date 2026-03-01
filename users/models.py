from django.db import models
from django.contrib.auth.models import Permission, AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('view_all_resumes', 'Can view all resumes'),
            ('edit_all_resumes', 'Can edit all resumes')
        ]