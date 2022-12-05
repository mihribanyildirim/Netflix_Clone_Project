from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .forms import *
# Create your views here.
def userLogin(request):
    if request.method == 'POST':
        kullanici = request.POST['kullaniciadi']
        sifre = request.POST['sifre']
        
        user = authenticate(request, username = kullanici, password = sifre)
        
        if user is not None:
            login(request,user)
            messages.success(request, 'Başarıyla giriş yaptınız')
            return redirect('profiles')
        else:
            messages.error(request, 'Kullanıcı Adı ve ya şifre hatalı')
            return redirect('login')
    return render(request,'login.html')

def userRegister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        tel = request.POST['tel']
        tc = request.POST['tc']
        resim = request.FILES['resim']
        tarih = request.POST['date']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.warning(request, 'Bu Kullanıcı Adı Zaten Kullanılıyor')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.warning(request, 'Bu Email Zaten Kullanılıyor')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, email=email, password=password1)
                Profil.objects.create(
                    user = user,
                    name = username,
                    email = email,
                    tel = tel,
                    tc = tc,
                    image = resim,
                    date = tarih,
               )
                user.save()
                messages.success(request, 'Başarıyla Kayıt Oldunuz')
                return redirect('login')
    return render(request,'register.html')

def userLogout(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız')
    return redirect ('login')

def userProfil(request):
    profile = request.user.profil
    context = {
        'profile': profile
    }
    return render(request, 'hesap.html', context)

def userDelete(request):
    userProfil = request.user.profil
    user = request.user
    userProfil.delete()
    user.delete()
    messages.success(request, 'Kullanıcı başarıyla silindi')
    return redirect('login')

def profilCreate(request):
    form = ProfilForm()
    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit = False)
            form.owner = request.user.profil
            form.save()
            messages.success(request, 'Profil oluşturuldu')
            return redirect('profiles')
    context = {
        'form':form,
    }
    return render(request, 'profil-create.html', context)
    