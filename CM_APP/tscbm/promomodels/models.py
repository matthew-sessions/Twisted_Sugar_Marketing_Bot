from django.db import models
import uuid

# Create your models here.
class DoorPromo(models.Model):
    psid = models.BigIntegerField(primary_key = True)
    qr_image_code = models.CharField(max_length=120)
    status = models.BooleanField(default=False)
    source = models.CharField(max_length=120)
    promo_id = models.CharField(max_length=50)
    name = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Orders(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    psid = models.BigIntegerField()
    order_amount = models.FloatField()
    promo_id = models.CharField(max_length=50)
    date_time = models.DateTimeField(auto_now_add=True)

    def update(self):
        data = DoorPromo.objects.get(psid=self.psid)
        data.status = True
        data.save()


