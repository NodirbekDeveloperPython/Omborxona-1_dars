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
        products = Mahsulot.objects.filter(sotuvchi__user=request.user)
        qidiruv_sozi = request.GET.get('soz')
        if qidiruv_sozi is not None:
            products = products.filter(mahsulot__nom__contains=qidiruv_sozi) | products.filter(mahsulot__brend__contains=
            qidiruv_sozi) | products.filter(mahsulot__sotuvchi__contains=qidiruv_sozi)
        data = {
            'mahsulotlar': products
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
        mijozlar = Mijoz.objects.filter(sotuvchi__user=request.user)
        qidiruv_sozi = request.GET.get('soz')
        if qidiruv_sozi is not None:
            mijozlar = mijozlar.filter(mijoz__ism__contains=qidiruv_sozi) | mijozlar.filter(mijoz__nom__contains=
            qidiruv_sozi) | mijozlar.filter(mijoz__manzil__contains=qidiruv_sozi) | mijozlar.filter(mijoz__tel__contains=qidiruv_sozi)
        data = {
            'mijozlar': mijozlar
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


class ProductUpdateView(View):
    def get(self, request, son):
        hozirgi_ombor = Sotuvchi.objects.filter(user=request.user)
        product = Mahsulot.objects.get(id=son)
        if request.user.is_authenticated and product.sotuvchi in hozirgi_ombor:
            data = {
                'mahsulot': Mahsulot.objects.get(id=son)
            }
            return render(request, 'product_update.html', data)
        else:
            return redirect('/bolimlar/mahsulotlar/')

    def post(self,request,son):
        Mahsulot.objects.filter(id=son).update(
            nom = request.POST.get('name'),
            brend = request.POST.get('brand_name'),
            narx = request.POST.get('price'),
            miqdor = request.POST.get('miqdor'),
            olchov = request.POST.get('amout'),
        )
        return redirect('/bolimlar/mahsulotlar/')