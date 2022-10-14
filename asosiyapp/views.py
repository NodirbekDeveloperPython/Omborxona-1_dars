from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from userapp.models import *
# Create your views here.


class BolimlarView(View):
    def get(self, request):
        return render(request, 'bulimlar.html')

class MahsulotlarView(View):
    def get(self, request):
        data = {
            'mahsulotlar': Mahsulot.objects.filter(sotuvchi__user=request.user)
        }
        return render(request, 'products.html', data)

    def post(self, request):
        s = Sotuvchi.objects.filter(user=request.user)[0]
        Mahsulot.objects.create(
                nom = request.POST.get('pr_name'),
                brend = request.POST.get('pr_brand'),
                miqdor = request.POST.get('pr_amount'),
                narx = request.POST.get('pr_price'),
                olchov = request.POST.get('olchov'),
                # kelgan_sana = request.POST.get(''),
                sotuvchi = s,
            )

        return redirect('/bolimlar/mahsulotlar/')


class ProductDeleteView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            hozirgi_sotuvchi = Sotuvchi.objects.filter(user=request.user)[0]
            m = Mahsulot.objects.get(id=pk)
            if m.sotuvchi == hozirgi_sotuvchi and request.user.is_staff:
                m.delete()
            return redirect('mahsulotlar')
        return redirect('login')


class MijozlarView(View):
    def get(self, request):
        data = {
            'mijozlar': Mijoz.objects.filter(sotuvchi__user=request.user)
        }
        return render(request, 'clients.html',data)

    def post(self, request):
        s = Sotuvchi.objects.filter(user=request.user)[0]
        Mijoz.objects.create(
            ism = request.POST.get('client_name'),
            nom = request.POST.get('client_shop'),
            manzil = request.POST.get('client_address'),
            tel = request.POST.get('client_phone'),
            qarz = request.POST.get('client_qarz'),
            sotuvchi = s,
        )
        return redirect('/bolimlar/clientlar/')

class ClientDeleteView(View):
    def get(self,request, son):
        if request.user.is_authenticated:
            hozirgi_sotuvchi = Sotuvchi.objects.filter(user=request.user)[0]
            client = Mijoz.objects.get(id=son)
            if request.user.is_staff and client.sotuvchi == hozirgi_sotuvchi:
                client.delete()
            return redirect('mijozlar')
        return redirect('login')


class ClientUpdateView(View):
    def get(self, request,son):

        data = {
            'client': Mijoz.objects.get(id=son)
        }
        return render(request, 'client_update.html',data)

    def post(self, request, son):
        if request.user.is_authenticated:
            hozirgi_sotuvchi = Sotuvchi.objects.filter(user=request.user)[0]
            if request.user.is_staff and Mijoz.objects.get(id=son).sotuvchi == hozirgi_sotuvchi:
                Mijoz.objects.filter(id=son).update(
                    ism = request.POST.get('client_name'),
                    nom = request.POST.get('client_shop'),
                    manzil = request.POST.get('client_address'),
                    tel = request.POST.get('client_phone'),
                    qarz = request.POST.get('client_qarz'),
                    sotuvchi = hozirgi_sotuvchi,
                )
        return redirect('mijozlar')