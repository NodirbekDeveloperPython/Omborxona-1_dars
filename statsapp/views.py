from django.shortcuts import render,redirect
from django.views import View
from userapp.models import *
from .models import *
# Create your views here.

class StatistikaView(View):
    def get(self,request):
        stats = Statistika.objects.filter(sotuvchi__user=request.user)
        qidiruv_sozi = request.GET.get('soz')
        if qidiruv_sozi is not None:
            stats = stats.filter(mahsulot__nom__contains=qidiruv_sozi)|Statistika.objects.filter(mahsulot__brend__contains=
            qidiruv_sozi)|Statistika.objects.filter(mahsulot__miqdor__contains=qidiruv_sozi)|Statistika.objects.filter(mahsulot__narx__contains=
            qidiruv_sozi)|Statistika.objects.filter(mahsulot__olchov__contains=qidiruv_sozi)
        data = {
            'statistikalar': stats,
            'mahsulotlar': Mahsulot.objects.all(),
            'mijozlar': Mijoz.objects.all(),
            'sotuvchilar': Sotuvchi.objects.all(),
        }
        return render(request,'stats.html', data)


    def post(self, request):
        Statistika.objects.create(
            mahsulot= Mahsulot.objects.get(id=request.POST.get('mahsulot')),
            mijoz=Mijoz.objects.get(id=request.POST.get('mijoz')),
            miqdor=request.POST.get('miqdor'),
            sana=request.POST.get('sana'),
            sotuvchi=Sotuvchi.objects.get(id=request.POST.get('sotuvchi')),
            jami=request.POST.get('summa'),
            tolandi=request.POST.get('tolandi'),
            nasiya=request.POST.get('nasiya'),
        )
        return redirect('/stats/')