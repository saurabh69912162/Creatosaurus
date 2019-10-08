from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, UserLoginForm , editpro
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import busi_data, creator_data
from .models import business_profile_data, creator_profile_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import business_profile_dataSerializers
from django.shortcuts import get_object_or_404
from .models import MyUser

User = get_user_model()

def register(request, *args, **kwargs):
    userme = request.user
    if userme.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, "accounts/register.html", context)


def login_view(request, *args, **kwargs):
    userme = request.user
    if userme.is_authenticated:
        return HttpResponseRedirect("/profile")
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            return HttpResponseRedirect("/profile")
        return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def check_bizz(name,user__name):
    if business_profile_data.objects.filter(username = user__name):
        return True
    else:
        data = business_profile_data()
        data.username = user__name
        data.first_name = ''
        data.company_category= ''
        data.website= ''
        data.email= name
        data.number= '0'
        data.founded= '1996-12-26'
        data.field_of_interest= ''
        data.overview= ''
        data.location= ''
        data.address= ''
        data.company_size= '0'
        data.save()
        print('user created')
        return True


def check_creator(name,user__name):
    if creator_profile_data.objects.filter(username = user__name):
        return True
    else:
        data = creator_profile_data()
        data.username = user__name
        data.skills = ''
        data.artist_category= ''
        data.website= ''
        data.email= name
        data.number= '0'
        data.description= ''
        data.location= ''
        data.address= ''
        data.gender = ''
        data.save()
        print('user created')
        return True





def profile(request):
    userme = request.user
    user_name_ = request.user.username
    if userme.is_authenticated:
        if request.user.category == 'Creator':
            # check_creator(userme, user_name_)
            return render(request,'accounts/creator.html',{})
        elif request.user.category == 'Business':
            # check_bizz(userme,user_name_)
            return render(request,'accounts/business.html',{})
        else:
            # print('choose category')
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")



def change_password(request):
    userme= request.user
    if userme.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/profile/')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {
            'form': form
        })
    else:
        return HttpResponseRedirect("/")

def edit_profile(request):
    userme = request.user
    if userme.is_authenticated:
        if request.method == 'POST':
            form = editpro(request.POST or None, instance= request.user)
            if form.is_valid():
                form.save()
                return redirect('/profile')
        else:
            form = editpro(instance=request.user)
            context = {'form':form}
            return render(request,'accounts/edit_profile.html',context)

    else:
        return HttpResponseRedirect("/")



def edit_business(request):
    userme = request.user
    if userme.is_authenticated :
        cat = request.user.category
        if cat =='Business':
            if request.method=='POST':
                poll = business_profile_data.objects.get(username = request.user.username)
                form = busi_data(request.POST or None,instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = business_profile_data.objects.get(username = request.user.username)
                form = busi_data(instance=poll)
                context = {'form':form}
                return render(request,'accounts/business_edit.html',context)
    else:
        return HttpResponseRedirect("/")



def edit_creator(request):
    userme = request.user
    if userme.is_authenticated :
        cat = request.user.category
        if cat == 'Creator':
            if request.method=='POST':
                poll = creator_profile_data.objects.get(username = request.user.username)
                form = creator_data(request.POST or None,instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = creator_profile_data.objects.get(username = request.user.username)
                form = creator_data(instance=poll)
                context = {'form':form}
                return render(request,'accounts/creator_edit.html',context)
        else:
            HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def edit_me(request):
    userme = request.user
    if userme.is_authenticated :

        cat = request.user.category

        if cat == 'Creator':

            if request.method=='POST':
                poll = creator_profile_data.objects.get(username = request.user.username)
                form = creator_data(request.POST or None,instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = creator_profile_data.objects.get(username = request.user.username)
                form = creator_data(instance=poll)
                context = {'form':form}
                return render(request,'accounts/creator_edit.html',context)

        elif cat == 'Business':

            if request.method == 'POST':
                poll = business_profile_data.objects.get(username=request.user.username)
                form = busi_data(request.POST or None, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = business_profile_data.objects.get(username=request.user.username)
                form = busi_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/business_edit.html', context)

        else:
            return HttpResponseRedirect("/")

    else:
        return HttpResponseRedirect("/")







class userlist(APIView):
    def get(self,request):
        list = MyUser.objects.all()
        serializer = business_profile_dataSerializers(list,many=True)
        return Response(serializer.data)

    def post(self):
        pass
