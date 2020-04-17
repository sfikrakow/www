from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.first_name + ' ' + self.last_name
