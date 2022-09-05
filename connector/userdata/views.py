from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from django.db.models import Q
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserData, UserPosting, FollowAccount


def handler404(request, exception):
    context = {}
    return render(request, "errors/404.html", context=context)


def handler500(request):
    context = {}
    return render(request, "errors/500.html", context=context)


def logout(request):
    auth.logout(request)
    return redirect('home')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        elif len(username) != 10:
            messages.info(request, 'Mobile number is not valid')
            return redirect('login')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'registration/login.html')


@login_required(login_url='login')
def home(request):
    global news_feed
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserData.objects.get(user=user_object)

    user_follow_list = []
    feed = []

    user_who_follow = FollowAccount.objects.filter(follower=request.user.username)

    for followers in user_who_follow:
        user_follow_list.append(followers.user)

    for usernames in user_follow_list:
        news_feed = UserPosting.objects.filter(user=usernames)
        feed.append(news_feed)

    news_feed = sorted(list(chain(*feed)), key=attrgetter('uploaded_at'), reverse=True)

    all_users = User.objects.all()
    user_following_all = []

    for usr in user_who_follow:
        user_list = User.objects.get(username=usr.user)
        user_following_all.append((user_list))

    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    suggesting_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(suggesting_list)

    username_profile = []
    username_profile_list = []

    for user in suggesting_list:
        username_profile.append(user.id)
    for ids in username_profile:
        profile_lists = UserData.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
    suggesting_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'post': news_feed,
                                          'suggest': suggesting_profile_list[:4]})


def user_data_save(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist, please try login with the email')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username is already taken, please use different one')
                return redirect('signup')
            elif len(username) != 10:
                messages.info(request, 'Mobile number is invalid')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()

                user_model = User.objects.get(username=username)
                new_user_data = UserData.objects.create(user=user_model, id_user=user_model.id)
                new_user_data.save()
                return redirect('home')
        else:
            messages.info(request, 'Passwords are different')
            return redirect('signup')
    else:
        return render(request, 'registration/signup.html')


@login_required(login_url='login')
def user_account(request, pk):
    user_obj = User.objects.get(username=pk)

    user_profile = UserData.objects.get(user=user_obj)
    pro = user_profile

    user_post = UserPosting.objects.filter(user=pk).order_by('-uploaded_at')
    post = user_post

    no_of_post = len(post)
    follower = request.user.username
    user = pk

    if FollowAccount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    no_of_followers = len(FollowAccount.objects.filter(user=pk))
    no_of_following = len(FollowAccount.objects.filter(follower=pk))

    context = {
        'user_obj': user_obj,
        'pro': pro,
        'post': post,
        'nop': no_of_post,
        'button_text': button_text,
        'no_of_followers': no_of_followers,
        'no_of_following': no_of_following,

    }

    return render(request, 'profile.html', context)


@login_required(login_url='login')
def account_setting(request):
    user_data_setting = UserData.objects.get(user=request.user)
    form = user_data_setting
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            bio = request.POST['bio']
            image = user_data_setting.profile_image
            location = request.POST['location']

            user_data_setting.bio = bio
            user_data_setting.profile_image = image
            user_data_setting.location = location
            user_data_setting.save()

        if request.FILES.get('image') != None:
            bio = request.POST['bio']
            image = request.FILES.get('image')
            location = request.POST['location']

            user_data_setting.bio = bio
            user_data_setting.profile_image = image
            user_data_setting.location = location
            user_data_setting.save()
        return redirect('setting')
    return render(request, 'account.html', {'form': form})


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            user = request.user.username
            image = request.FILES.get('post_image')
            caption = request.POST['caption']
            new_post = UserPosting.objects.create(user=user, image=image, caption=caption)
            new_post.save()

        if request.FILES.get('image') != None:
            user = request.user.username
            image = request.FILES.get('post_image')
            caption = request.POST['caption']
            new_post = UserPosting.objects.create(user=user, image=image, caption=caption)
            new_post.save()

        return redirect('home')
    else:
        return redirect('home')


@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowAccount.objects.filter(follower=follower, user=user):
            erase_follower = FollowAccount.objects.get(follower=follower, user=user)
            erase_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowAccount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)

    return None


def search_result(request):
    global username_profile_list
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserData.objects.get(user=user_object)

    if request.method == 'POST':
        qs = request.POST['qs']
        username_object = User.objects.filter(
            Q(username__icontains=qs) | Q(first_name__icontains=qs) | Q(email__icontains=qs))

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = UserData.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html',
                  {'user_profile': user_profile, 'username_profile_list': username_profile_list})
