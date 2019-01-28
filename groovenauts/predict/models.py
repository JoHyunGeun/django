from django.db import models
# Create your models here.
def upload_location(instance, filename):
    return filename

class Information(models.Model):

    sex = models.CharField(default='', max_length=6)
    picture = models.ImageField(upload_to=upload_location, default='default.jpeg', blank=True, null=True)

    def __str__(self):
        return self.picture
