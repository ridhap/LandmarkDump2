from django.db import models
from datetime import datetime

# Create your models here.
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    task_accomplished = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now=datetime.now(), null=True)

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return "ID = {}, title = {}".format(self.description, self.title)
