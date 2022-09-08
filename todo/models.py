from django.db import models

class User(models.Model):
  name = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name



class Todo(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.CharField(max_length=200)
  is_completed = models.BooleanField(default=False)
  
  def __str__(self):
    return self.text