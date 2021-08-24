from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.
class Files(models.Model):
    BIOACTIVE = 'BI'
    CHEMICAL = 'CH'
    SAMPLEINFO = 'SP'
    NUTRITION = 'NU'
    PHYSICAL = 'PH'
    META_DATA = 'MD'
    TYPE_FILE = [
        (BIOACTIVE, 'Bioactive'),
        (CHEMICAL, 'Chemical'),
        (SAMPLEINFO, 'Sampleinfo'),
        (NUTRITION, 'Nutrition'),
        (PHYSICAL, 'Physical'),
        (META_DATA, 'Meta Data'),
    ]
    type_file = models.CharField(
        max_length=2,
        choices=TYPE_FILE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='rice/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
