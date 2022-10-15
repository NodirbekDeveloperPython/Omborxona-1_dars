from django.db import models
from asosiyapp.models import *
from userapp.models import *
# Create your models here.

class Statistika(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.SET_NULL, null=True)
    mijoz = models.ForeignKey(Mijoz, on_delete=models.SET_NULL, null=True)
    miqdor = models.PositiveSmallIntegerField(default=1)
    sana = models.DateField(auto_now=True)
    sotuvchi = models.ForeignKey(Sotuvchi, on_delete=models.SET_NULL, null=True)
    jami = models.PositiveSmallIntegerField(default=1)
    tolandi = models.PositiveSmallIntegerField()
    nasiya = models.PositiveSmallIntegerField()
    def __str__(self): return self.mijoz.ism
