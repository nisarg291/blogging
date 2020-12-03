#from django.shortcuts import render,redirect
#from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
#we use this form which are provided by django so we do not need to validation manually
#we can create python class togenerate html form and some class are provided by django here UserCreaitionForm class for form
#message.debug,message.info,message.success,message.warning,message.error


# Create your views here.
import json
from ast import literal_eval
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Profile
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
# we use this decorator so we use profile url if and only if we have logged in.
# if we do not use decorator then we can accest profile page with manully write profile url in ulr bar without logged in
@login_required
def followers(request):
    userid=request.user.id
    print(userid)
    userFriends=literal_eval(request.user.profile.friends)
    Friends = []
    if str(request.user.profile.friends) != "-":
        Fri = literal_eval(request.user.profile.friends)
        print(type(Fri))
        for item in Fri.items():
            Friends.append(item)
    else:
        Fri = {}
    return render(request,'users/followers.html',{'id':userid,'Friends':Friends})
def following(request):
    userid=request.user.id
    print(userid)
    userFriends=literal_eval(request.user.profile.friends)
    Friends = []
    if str(request.user.profile.friends) != "-":
        Fri = literal_eval(request.user.profile.friends)
        print(type(Fri))
        for item in Fri.items():
            Friends.append(item)
    else:
        Fri = {}
    return render(request,'users/following.html',{'id':userid,'Friends':Friends})
def accept(request,id):
    Cuser=request.user;
    friends=literal_eval(Cuser.profile.friends)
    print(friends)
    friends[str(id)]['followers']="true";
    Cuser.profile.friends=friends
    Cuser.profile.save()
    users=User.objects.all()
    flag1="true"
    flag="false"
    for user in users:
        if user.id==id:
            getProfile=Profile.objects.get(user=id)
            userexist = False;
            flag = 'false';
            flag1='true';
            if str(getProfile.friends) != '-':
                ll5 = eval(getProfile.friends)
                try:
                    if ll5[str(Cuser.id)]['id']==str(Cuser.id):
                        print('user is exist')
                        ll5[str(Cuser.id)]['following'] = "true"
                        userexist=True;
                        getProfile.friends = ll5;
                        getProfile.save()

                except:
                    if userexist==False:
                        ll5[str(Cuser.id)]={'id':str(Cuser.id),'name':str(Cuser.username),'image':str(Cuser.profile.image),'followers':'fl','following':flag1};
                        getProfile.friends = ll5;
                        getProfile.save()
            else:
                l2 = {}
                l2[str(Cuser.id)] = {'id': str(Cuser.id), 'name': str(Cuser.username), 'image': str(Cuser.profile.image),'followers':'fl','following':flag1};
            # l1.append({'id':str(Cuser.id),'name':str(Cuser.username),'image':str(Cuser.profile.image),'flag':flag})
            # getprofile.friends=l1;
                getProfile.friends = l2;
            # getprofile.friends=getprofile.friends.append({'id':str(Cuser.id),'name':Cuser.username,'image':str(Cuser.profile.image),'flag':flag})
                getProfile.save()
    # Friends = []
    # if str(Cuser.profile.friends) != "-":
    #     Fri = literal_eval(Cuser.profile.friends)
    #     print(type(Fri))
    #     for item in Fri.items():
    #         Friends.append(item)
    # else:
    #     Fri = {}
    # context = {'Friends':Friends}
    return redirect('blog-home')
def friend(request,id):
    Cuser=request.user;
    users=User.objects.all()
    getProfile="";
    userId=0;
    context={}
    userexist = False;
    for user in users:
        if user.id==id:
            getprofile=Profile.objects.get(user=user.id)
            print(getprofile)
            # userId=user.id;
            flag='false';
            if str(getprofile.friends)!='-':
                ll5=eval(getprofile.friends)
                print(ll5)
                # context = {
                #     'id': user.id,
                #     'username': user.username,
                #     'email': user.email,
                #     'mobile_no': user.profile.mobile_no,
                #     'clg_name': user.profile.clg_name,
                #     'degree': user.profile.degree,
                #     'skill': user.profile.skill,
                #     'jobs': user.profile.jobs,
                #     'image': user.profile.image,
                #     'friends': user.profile.friends,
                #     'msg': "request is send",
                # }
                try:
                    if ll5[str(Cuser.id)]['id'] == str(Cuser.id):
                        ll5[str(Cuser.id)]['followers']="false"
                        userexist = True;
                        print("user is exist")
                        getprofile.friends = ll5;
                        getprofile.save()
                        context = {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'mobile_no': user.profile.mobile_no,
                            'clg_name': user.profile.clg_name,
                            'degree': user.profile.degree,
                            'skill': user.profile.skill,
                            'jobs': user.profile.jobs,
                            'image': user.profile.image,
                            'friends': user.profile.friends,
                            'msg': "request send",
                        }
                        break;
                except:
                    if userexist==False:
                        ll5[str(Cuser.id)]={'id':str(Cuser.id),'name':Cuser.username,'image':str(Cuser.profile.image),'followers':flag,'following':flag};
                         # list1={'id':str(Cuser.id),'name':Cuser.username,'image':str(Cuser.profile.image),'flag':flag};
                        #ll5.append({'id':str(Cuser.id),'name':Cuser.username,'image':str(Cuser.profile.image),'followers':flag,'follwing':flag});
                        #ll5.append({'id':str(Cuser.id),'name':Cuser.username,'image':str(Cuser.profile.image),'followers':flag,'follwing':flag})
                        getprofile.friends=ll5;
                        getprofile.save()
                        context = {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'mobile_no': user.profile.mobile_no,
                            'clg_name': user.profile.clg_name,
                            'degree': user.profile.degree,
                            'skill': user.profile.skill,
                            'jobs': user.profile.jobs,
                            'image': user.profile.image,
                            'friends': user.profile.friends,
                            'msg': "request send",
                        }
                        break;
            else:
            #l1=[];
                l2={}
                l2[str(Cuser.id)]={'id':str(Cuser.id),'name':str(Cuser.username),'image':str(Cuser.profile.image),'followers':flag,'following':flag};
                #l1.append({'id':str(Cuser.id),'name':str(Cuser.username),'image':str(Cuser.profile.image),'flag':flag})
                #getprofile.friends=l1;
                getprofile.friends = l2;
                # getprofile.friends=getprofile.friends.append({'id':str(Cuser.id),'name':Cuser.username,'image':str(Cuser.profile.image),'flag':flag})
                getprofile.save()
                context = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'mobile_no': user.profile.mobile_no,
                'clg_name': user.profile.clg_name,
                'degree': user.profile.degree,
                'skill': user.profile.skill,
                'jobs': user.profile.jobs,
                'image': user.profile.image,
                'friends': user.profile.friends,
                'msg': "request send",
                }
                break;
                # getprofile.friends=str(getprofile.friends)
            # Profile.objects.get(user=user.id).update(friends=friendList)
            # Profile.update_db_field(Profile,user.id,list1)
            # print(getprofile.friends)
    return render(request,'users/profile1.html',context);

def profile1(request,id):
    print("profile")
    user1=id
    Cuserid=request.user.id;
    CuserName=request.user.username;
    CuserProfile=request.user.profile.image;
    Cuserfriends=request.user.profile.friends;
    #print(user1)
    users=User.objects.all()
    u_form=[]
    p_form=[]
    context={}
    for user in users:
        if user.id==user1:
            try:
                if literal_eval(user.profile.friends)[str(Cuserid)]['followers']=="true":
                    context={
                    'Cuserid':Cuserid,
                    'CuserName':CuserName,
                    'CuserProfile':CuserProfile,
                    'id':user.id,
                    'username':user.username,
                    'email':user.email,
                    'mobile_no':user.profile.mobile_no,
                    'clg_name':user.profile.clg_name,
                    'degree':user.profile.degree,
                    'skill':user.profile.skill,
                    'jobs':user.profile.jobs,
                    'image':user.profile.image,
                    'msg':"you are following",
                    }
                elif literal_eval(request.user.profile.friends)[str(id)]['following'] == "true":
                    context = {
                            'Cuserid': Cuserid,
                            'CuserName': CuserName,
                            'CuserProfile': CuserProfile,
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'mobile_no': user.profile.mobile_no,
                            'clg_name': user.profile.clg_name,
                            'degree': user.profile.degree,
                            'skill': user.profile.skill,
                            'jobs': user.profile.jobs,
                            'image': user.profile.image,
                            'msg': "you are following",
                    }
                elif (literal_eval(user.profile.friends)[str(Cuserid)]['followers']=="false"):
                    context = {
                    'Cuserid': Cuserid,
                    'CuserName': CuserName,
                    'CuserProfile': CuserProfile,
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'mobile_no': user.profile.mobile_no,
                    'clg_name': user.profile.clg_name,
                    'degree': user.profile.degree,
                    'skill': user.profile.skill,
                    'jobs': user.profile.jobs,
                    'image': user.profile.image,
                    'msg': "request send",
                    }
                else:
                    context = {
                        'Cuserid': Cuserid,
                        'CuserName': CuserName,
                        'CuserProfile': CuserProfile,
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'mobile_no': user.profile.mobile_no,
                        'clg_name': user.profile.clg_name,
                        'degree': user.profile.degree,
                        'skill': user.profile.skill,
                        'jobs': user.profile.jobs,
                        'image': user.profile.image,
                        'msg': "follow",
                    }
            except:
                context = {
                'Cuserid': Cuserid,
                'CuserName': CuserName,
                'CuserProfile': CuserProfile,
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'mobile_no': user.profile.mobile_no,
                'clg_name': user.profile.clg_name,
                'degree': user.profile.degree,
                'skill': user.profile.skill,
                'jobs': user.profile.jobs,
                'image': user.profile.image,
                'msg': "follow",
                }
            break;
    return render(request, 'users/profile1.html', context)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        #which is uploaded bu user from his/her p.c.'s location
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    Cuser=request.user;
    Friends = []
    if str(Cuser.profile.friends) != "-":
        Fri = literal_eval(Cuser.profile.friends)
        print(type(Fri))
        for item in Fri.items():
            Friends.append(item)
    else:
        Fri = {}

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'Friends':Friends

    }
    return render(request, 'users/profile.html', context)


def edit(request):
    Cuser=request.user;
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        #which is uploaded bu user from his/her p.c.'s location
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/edit.html', context)