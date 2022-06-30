from django.db import models
from django.db.models.aggregates import Max
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Model of each User

class client(AbstractUser):
    username = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    REQUIRED_FIELDS = ['password', 'name']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username}"


# Model of each Item
class item(models.Model):
    customer = models.ForeignKey(client, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=400)
    access_token = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.customer} "
