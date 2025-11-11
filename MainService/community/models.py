from django.db import models

# Create your models here.

class Community(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    private = models.BooleanField()
    members = models.IntegerField()
    publish_date = models.DateField()
    creator_id = models.TextField()

    def __str__(self):
        return self.id

class UsersAllowed(models.Model):
    user_id = models.TextField(primary_key=True)
    community_id = models.TextField()

    def __str__(self):
        return self.user_id