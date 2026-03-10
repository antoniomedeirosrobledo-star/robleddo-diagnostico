from django.db import models
import uuid

class Report(models.Model):
    uid = models.CharField(max_length=12, unique=True, default='')
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)
