from django.db import models

from client.models import AuditFields, CustomUser

# Create your models here.
class Notice(AuditFields):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="authored_notices"
    )
    file_attachment = models.FileField(
        upload_to="notices/attachments/", 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"{self.title}"