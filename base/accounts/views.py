from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserCreationForm, UserLoginForm, editpro
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import busi_data, creator_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import business_profile_dataSerializers
from django.shortcuts import get_object_or_404
from .models import *
import requests
import base64
from datetime import datetime

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


def check_bizz(name, user__name):
    if business_profile_data.objects.filter(username=user__name):
        return True
    else:
        data = business_profile_data()
        data.username = user__name
        data.first_name = ''
        data.company_category = ''
        data.website = ''
        data.email = name
        data.number = '0'
        data.founded = '1996-12-26'
        data.field_of_interest = ''
        data.overview = ''
        data.location = ''
        data.address = ''
        data.company_size = '0'
        data.save()
        print('user created')
        return True


def check_creator(name, user__name):
    if creator_profile_data.objects.filter(username=user__name):
        return True
    else:
        data = creator_profile_data()
        data.username = user__name
        data.skills = ''
        data.artist_category = ''
        data.website = ''
        data.email = name
        data.number = '0'
        data.description = ''
        data.location = ''
        data.address = ''
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
            return render(request, 'accounts/creator.html', {})
        elif request.user.category == 'Business':
            # check_bizz(userme,user_name_)
            return render(request, 'accounts/business.html', {})
        else:
            # print('choose category')
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def change_password(request):
    userme = request.user
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
            form = editpro(request.POST or None, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/profile')
        else:
            form = editpro(instance=request.user)
            context = {'form': form}
            return render(request, 'accounts/edit_profile.html', context)

    else:
        return HttpResponseRedirect("/")


def edit_business(request):
    userme = request.user
    if userme.is_authenticated:
        cat = request.user.category
        if cat == 'Business':
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


def edit_creator(request):
    userme = request.user
    if userme.is_authenticated:
        cat = request.user.category
        if cat == 'Creator':
            if request.method == 'POST':
                poll = creator_profile_data.objects.get(username=request.user.username)
                form = creator_data(request.POST or None, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = creator_profile_data.objects.get(username=request.user.username)
                form = creator_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/creator_edit.html', context)
        else:
            HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def edit_me(request):
    userme = request.user
    if userme.is_authenticated:

        cat = request.user.category

        if cat == 'Creator':

            if request.method == 'POST':
                poll = creator_profile_data.objects.get(username=request.user)
                form = creator_data(request.POST or None, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = creator_profile_data.objects.get(username=request.user)
                form = creator_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/creator_edit.html', context)

        elif cat == 'Business':

            if request.method == 'POST':
                poll = business_profile_data.objects.get(username=request.user)
                form = busi_data(request.POST or None, instance=poll)
                if form.is_valid():
                    form.save()
                    return redirect('/profile')
            else:
                poll = business_profile_data.objects.get(username=request.user)
                form = busi_data(instance=poll)
                context = {'form': form}
                return render(request, 'accounts/business_edit.html', context)

        else:
            return HttpResponseRedirect("/")

    else:
        return HttpResponseRedirect("/")


class userlist(APIView):
    def get(self, request):
        list = MyUser.objects.all()
        serializer = business_profile_dataSerializers(list, many=True)
        return Response(serializer.data)

    def post(self):
        pass


import time


def timed_job():
    print('lmao')
    print(datetime.now())


from django.conf import settings


def connect(request):
    lmao = SocialAccount.objects.filter(user=request.user.id)
    data = user_connection_data.objects.get(username=request.user.id)
    connection_count = SocialAccount.objects.filter(user=request.user.id).count()
    selection_count = selected_connections.objects.filter(username=request.user.id).count()
    return render(request, 'accounts/lol.html', {'lmao': lmao, 'data': data, 'connection_count': connection_count, })


def long_live_facebook(existing_token):
    import facebook
    lol = existing_token
    graph = facebook.GraphAPI(lol)
    app_id = '1990551177704465'
    app_secret = '38942534de2eeb787551d1cf9d1d0dac'
    extended_token = graph.extend_access_token(app_id, app_secret)
    final = extended_token['access_token']
    return final


def facebookconfigure(requset):
    return HttpResponse('nothing here!')


def configure(request):
    account = []
    error_connected = ''
    pack_error = ''
    obj = SocialAccount.objects.filter(user=request.user.id)
    for x in range(len(obj)):
        account.append(obj[x])

    data = user_connection_data.objects.get(username=request.user.id)

    selected = selected_connections.objects.filter(dirtybit=request.user.dirtybit, selected=True)
    not_selected = selected_connections.objects.filter(dirtybit=request.user.dirtybit, selected=False)

    if 'facebook' in request.POST:
        print(request.POST['facebook'])
        object = request.POST['facebook']
        facetoken = get_object_or_404(SocialToken, id=request.POST['facebook'])
        all_account = get_object_or_404(SocialAccount, user=request.user, id=request.POST['facebook'])
        obj1 = requests.get("https://graph.facebook.com/me?fields=accounts&access_token=" + str(facetoken))
        par = obj1.json()
        accs = par['accounts']['data']
        return render(request, 'accounts/page-configrue.html', {'accs': accs, 'object': object})


    elif 'facebook-model' in request.POST:
        if data.total_seleceted_connections >= data.max_seleceted_connections:
            pack_error = 'Maximum Limit Reached, Upgrade your package!'
        else:
            obj = request.POST['facebook-model'].split(',,,,,')
            if not selected_connections.objects.filter(account_uid=obj[0]):
                print(obj[0])
                print(obj[1])
                print(obj[2])
                print(obj[3])
                obj_create = selected_connections()
                obj_create.username = MyUser.objects.get(id=request.user.id)
                obj_create.dirtybit = request.user.dirtybit
                obj_create.provider = 'facebook'
                obj_create.account_token = SocialToken.objects.get(id=obj[3])
                obj_create.access_token = obj[1]
                obj_create.long_token = long_live_facebook(obj[1])
                obj_create.extra_data = SocialAccount.objects.get(user=request.user.id, id=obj[3]).extra_data
                obj_create.access_expiry = SocialToken.objects.get(id=obj[3]).expires_at
                obj_create.account_name = obj[2]
                obj_create.account_uid = obj[0]
                obj_create.selected = True
                obj_create.save()
                data.total_seleceted_connections += 1
                data.save()
            else:
                error_connected = 'Account Already Connected !'

    elif 'google' in request.POST:
        if data.total_seleceted_connections >= data.max_seleceted_connections:
            pack_error = 'Maximum Limit Reached, Upgrade your package!'
        else:
            if SocialAccount.objects.filter(user=request.user.id, id=request.POST['google']).exists():
                if not selected_connections.objects.filter(
                        account_uid=SocialAccount.objects.get(user=request.user.id, id=request.POST['google']).uid):
                    obj_create = selected_connections()
                    obj_create.username = MyUser.objects.get(id=request.user.id)
                    obj_create.dirtybit = request.user.dirtybit
                    obj_create.provider = 'google'
                    obj_create.access_token = SocialToken.objects.get(id=request.POST['google']).token
                    obj_create.extra_data = SocialAccount.objects.get(user=request.user.id,
                                                                      id=request.POST['google']).extra_data
                    obj_create.access_expiry = SocialToken.objects.get(id=request.POST['google']).expires_at
                    obj_create.account_name = SocialAccount.objects.get(user=request.user.id,
                                                                        id=request.POST['google']).extra_data['email']
                    obj_create.account_uid = SocialAccount.objects.get(user=request.user.id,
                                                                       id=request.POST['google']).uid
                    obj_create.selected = True
                    obj_create.save()
                    obj_create.save()
                    data.total_seleceted_connections += 1
                    data.save()
                    # print(SocialAccount.objects.filter(user=request.user.id, id = request.POST['google']))
                    # print(SocialToken.objects.get(id = request.POST['google']).account)
                    # print(request.POST['google'])

                else:
                    error_connected = 'Account Already Connected !'
                    pass
            else:
                return redirect('/404')

    elif 'pinterest' in request.POST:
        if data.total_seleceted_connections >= data.max_seleceted_connections:
            pack_error = 'Maximum Limit Reached, Upgrade your package!'
        else:
            print(request.POST['pinterest'])

    elif 'linkedin' in request.POST:
        if data.total_seleceted_connections >= data.max_seleceted_connections:
            pack_error = 'Maximum Limit Reached, Upgrade your package!'
        else:
            if SocialAccount.objects.filter(user=request.user.id, id=request.POST['linkedin']).exists():
                if not selected_connections.objects.filter(
                        account_uid=SocialAccount.objects.get(user=request.user.id, id=request.POST['linkedin']).uid):

                    obj_create = selected_connections()
                    obj_create.username = MyUser.objects.get(id=request.user.id)
                    obj_create.dirtybit = request.user.dirtybit
                    obj_create.provider = 'linkedin'
                    obj_create.account_token = SocialToken.objects.get(id=request.POST['linkedin'])
                    obj_create.access_token = SocialToken.objects.get(id=request.POST['linkedin'])

                    obj_create.extra_data = SocialAccount.objects.get(user=request.user.id,
                                                                      id=request.POST['linkedin']).extra_data
                    obj_create.access_expiry = SocialToken.objects.get(id=request.POST['linkedin']).expires_at
                    obj_create.account_name = SocialAccount.objects.get(user=request.user.id,
                                                                        id=request.POST['linkedin']).extra_data[
                                                  'firstName']['localized']['en_US'] + ' ' + \
                                              SocialAccount.objects.get(user=request.user.id,
                                                                        id=request.POST['linkedin']).extra_data[
                                                  'lastName']['localized']['en_US']
                    obj_create.account_uid = SocialAccount.objects.get(user=request.user.id,
                                                                       id=request.POST['linkedin']).uid
                    obj_create.selected = True
                    obj_create.save()

                    data.total_seleceted_connections += 1
                    data.save()
                    # print(SocialAccount.objects.filter(user=request.user.id, id = request.POST['twitter']))
                    # print(SocialToken.objects.get(id = request.POST['twitter']).account)
                    # print(request.POST['twitter'])

                else:
                    error_connected = 'Account Already Connected !'
                    pass

    elif 'twitter' in request.POST:
        if data.total_seleceted_connections >= data.max_seleceted_connections:
            pack_error = 'Maximum Limit Reached, Upgrade your package!'
        else:
            if SocialAccount.objects.filter(user=request.user.id, id=request.POST['twitter']).exists():
                if not selected_connections.objects.filter(
                        account_uid=SocialAccount.objects.get(user=request.user.id, id=request.POST['twitter']).uid):

                    obj_create = selected_connections()
                    obj_create.username = MyUser.objects.get(id=request.user.id)
                    obj_create.dirtybit = request.user.dirtybit
                    obj_create.provider = 'twitter'
                    obj_create.account_token = SocialToken.objects.get(id=request.POST['twitter'])
                    obj_create.access_token = SocialToken.objects.get(id=request.POST['twitter'])

                    obj_create.access_token_secret = SocialToken.objects.get(id=request.POST['twitter']).token_secret

                    obj_create.extra_data = SocialAccount.objects.get(user=request.user.id,
                                                                      id=request.POST['twitter']).extra_data
                    obj_create.access_expiry = SocialToken.objects.get(id=request.POST['twitter']).expires_at
                    obj_create.account_name = SocialAccount.objects.get(user=request.user.id,
                                                                        id=request.POST['twitter']).extra_data['name']
                    obj_create.account_uid = SocialAccount.objects.get(user=request.user.id,
                                                                       id=request.POST['twitter']).uid
                    obj_create.selected = True
                    obj_create.save()

                    data.total_seleceted_connections += 1
                    data.save()
                    # print(SocialAccount.objects.filter(user=request.user.id, id = request.POST['twitter']))
                    # print(SocialToken.objects.get(id = request.POST['twitter']).account)
                    # print(request.POST['twitter'])

                else:
                    error_connected = 'Account Already Connected !'
                    pass
    elif 'facebook-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['facebook-remove']).extra_data['id']
        count_var1 = selected_connections.objects.filter(username=request.user.id, extra_data__icontains=var).count()
        var1 = selected_connections.objects.filter(username=request.user.id, extra_data__icontains=var).delete()
        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['facebook-remove']).delete()
        data.total_seleceted_connections -= count_var1
        data.save()
        return redirect('/configure')

    elif 'google-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['google-remove']).uid
        var1 = selected_connections.objects.filter(username=request.user.id, account_uid=var).delete()
        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['google-remove']).delete()
        data.total_seleceted_connections -= 1
        data.save()
        return redirect('/configure')

    elif 'twitter-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['twitter-remove']).uid
        var1 = selected_connections.objects.filter(username=request.user.id, account_uid=var).delete()
        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['twitter-remove']).delete()
        data.total_seleceted_connections -= 1
        data.save()
        return redirect('/configure')

    elif 'pinterest-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['pinterest-remove']).uid
        var1 = selected_connections.objects.filter(username=request.user.id, account_uid=var).delete()
        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['pinterest-remove']).delete()
        data.total_seleceted_connections -= 1
        data.save()
        return redirect('/configure')

    elif 'linkedin-remove' in request.POST:
        var = SocialAccount.objects.get(user=request.user.id, id=request.POST['linkedin-remove']).uid
        var1 = selected_connections.objects.filter(username=request.user.id, account_uid=var).delete()
        delete_me = SocialAccount.objects.get(user=request.user.id, id=request.POST['linkedin-remove']).delete()
        data.total_seleceted_connections -= 1
        data.save()
        return redirect('/configure')






    else:
        pass

    return render(request, 'accounts/configure.html', {'account': account, 'not_selected': not_selected,
                                                       'selected': selected, 'error_connected': error_connected,
                                                       'pack_error': pack_error, })


import calendar
from datetime import date


def schedule(request):
    obj = date.today()
    arr = []
    d = obj.strftime("%d")
    m = obj.strftime("%m")
    year = obj.strftime("%Y")
    obj1 = calendar.monthcalendar(int(year), int(m))
    month = calendar.month_name[int(m)]
    for x in range(1, 13):
        arr.append(calendar.month_name[x])

    if 'date_selected' in request.POST:
        print(request.POST['date_selected'])
        data = request.POST['date_selected']
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        return redirect('/configure/post/' + encodedStr)

    return render(request, 'accounts/schedule.html',
                  {'obj1': obj1, 'month': month, 'arr': arr, 'd': int(d), 'year': int(year), 'm': int(m)})


# from datetime import datetime, timedelta
import datetime


def time_machine(request, data):
    urlSafeEncodedBytes = base64.b64decode(data)
    date = str(urlSafeEncodedBytes, "utf-8")
    time_string = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    time_obj = datetime.datetime.now()
    hour = time_obj.hour
    minute = time_obj.minute
    second = time_obj.second

    now = datetime.datetime.now()
    now_plus_15 = now + datetime.timedelta(minutes=15)

    return render(request, 'accounts/datetime.html',
                  {'date': date, 'hour': now_plus_15.hour, 'minute': now_plus_15.minute, 'second': now_plus_15.second,
                   'time_string': time_string})


import random
import string


def randomString(stringLength=64):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def post_factory(request, data):
    urlSafeEncodedBytes = base64.b64decode(data)
    date = str(urlSafeEncodedBytes, "utf-8")
    selections = selected_connections.objects.filter(username=request.user.id)
    new_arr = []
    names_arr = []
    accs_provider = []
    if 'submit' in request.POST:

        for x in selections:
            try:
                if request.POST[str(x)]:
                    new_arr.append(request.POST[str(x)])
                    names_arr.append(x.account_name)
                    accs_provider.append(x.provider)

            except:
                pass
        print(names_arr)

        # data_accounts = accounts
        # encodedBytes = base64.b64encode(data_accounts.encode("utf-8"))
        # encodedAccounts = str(encodedBytes, "utf-8")

        data_message = request.POST['message']
        # encodedBytes = base64.b64encode(data_message.encode("utf-8"))
        # encodedMessage = str(encodedBytes, "utf-8")

        data_filename = request.POST['filename']
        # encodedBytes = base64.b64encode(data_filename.encode("utf-8"))
        # encodedFilename = str(encodedBytes, "utf-8")


        rand_user_string = randomString()
        obj = temp_data()
        obj.rand_save_string = rand_user_string
        obj.accs = new_arr
        obj.cont = data_message
        obj.img = data_filename
        obj.accs_name = names_arr
        obj.accs_provider = accs_provider
        obj.date = date
        obj.save()

        return redirect('/config-all-platforms/' + rand_user_string)

    return render(request, 'accounts/post_factory.html', {'date': date, 'selections': selections, })


def all_post_config(request, rand_user_string):
    url_post = '/config-all-platforms/' + rand_user_string

    model_data = get_object_or_404(temp_data, rand_save_string=rand_user_string)

    # urlSafeEncodedBytes = base64.b64decode(data)
    # date = str(urlSafeEncodedBytes, "utf-8")
    #
    # encodedAccountsurlSafeEncodedBytes = base64.b64decode(encodedAccounts)
    # accounts = str(encodedAccountsurlSafeEncodedBytes, "utf-8")

    arr = eval(model_data.accs)
    #
    # encodedMessageurlSafeEncodedBytes = base64.b64decode(encodedMessage)
    # message = str(encodedMessageurlSafeEncodedBytes, "utf-8")
    #
    # encodedFilenameurlSafeEncodedBytes = base64.b64decode(encodedFilename)
    # filename = str(encodedFilenameurlSafeEncodedBytes, "utf-8")

    date = model_data.date
    accounts = model_data.accs
    accs_name = model_data.accs_name
    message = model_data.cont
    filename = model_data.img
    accs_provider = model_data.accs_provider
    zipis = zip(eval(model_data.accs), eval(model_data.accs_name), eval(model_data.accs_provider))
    uuid_zip = []


    if request.method == 'POST':
        for x in arr:
            print(x, request.POST[x])

            obj = scheduler_model()
            obj.username = MyUser.objects.get(id = request.user.id)
            obj.dirtybit = MyUser.objects.get(id = request.user.id).dirtybit
            obj.provider = selected_connections.objects.get(account_uid = x)
            obj.content = request.POST[x]
            obj.save()
            print(str(obj.schedule_dirtybit))
            uuid_zip.append(str(obj.schedule_dirtybit))
            print(uuid_zip)
        model_data.uid_zip = uuid_zip
        model_data.save()

        return redirect('/select-time/post/'+rand_user_string)




    return render(request, 'accounts/all_post_config.html', {'date': date, 'accounts': accounts,
                                                             'message': message, 'filename': filename,
                                                             'arr': arr, 'url_post': url_post,'zipis':zipis})





def set_timer_post(request, rand_user_string):
    post_url = '/select-time/post/'+rand_user_string
    model_data = get_object_or_404(temp_data, rand_save_string=rand_user_string)
    date = model_data.date

    from datetime import datetime
    if str(datetime.now().day) == date.split('/')[0] and str(datetime.now().month) == date.split('/')[1]:
        return HttpResponse('today! i will figure it out ')
    else:
        for x in eval(model_data.uid_zip):
            print(x)
        else:
            pass

        if request.method == 'POST':
            if 'hour_is' in request.POST and 'min_is' in request.POST:
                print((request.POST['hour_is']), int(request.POST['min_is']))


        return render(request, 'accounts/set_time.html',{'post_url':post_url,'model_data':model_data,'date':date,'uid':eval(model_data.uid_zip)})





def schedule_for(request, month):
    obj = date.today()
    m = obj.strftime("%m")
    month_calc = calendar.month_name[int(m)]
    if month_calc == month:
        return redirect('/schrdule-this-month')
    else:
        return HttpResponse(month)
