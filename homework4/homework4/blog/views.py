from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from mimetypes import guess_type
from django.http import HttpResponse, Http404
from models import *
from forms import *
import os
from django.conf import settings
from itertools import chain

@transaction.atomic
def main(request):
	context={}
	if request.user.is_authenticated():
		users = User.objects.all().exclude(username = request.user)
	else:
		users = User.objects.all()

	posts = []
	follow_mark = 0
	follow_users=[]

	if request.user.is_authenticated:
		followers = Follower.objects.filter(user = request.user.id)
		if not followers:
			follow_mark=1
		for follower in followers:
			follow_users.append(follower.following)
	for follow_user in follow_users:
		posts.extend(Post.get_posts(follow_user))
		posts = sorted(posts, key=lambda instance: instance.time, reverse = True)
	context={'users':users, 'posts':posts, 'follow_mark':follow_mark, 'follow_users':follow_users}
	return render(request, 'blog/base.html', context)

@login_required
@transaction.atomic
def manage(request):
	context ={'posts':Post.get_posts(request.user).order_by("-time"),'form':PostForm()}
	return render(request,'blog/index.html',context)


@login_required
@transaction.atomic
def follow(request,username):
	user_click = User.objects.get(username = username)
	followers = Follower.objects.filter(user = request.user)
	followers_list=[]

	for follower in followers:
		followers_list.append(follower.following)

	if user_click in followers_list:
		Follower.objects.get(user = request.user, following = user_click).delete()
	else:
		new_follower = Follower(user = request.user, following = user_click)
		new_follower.save()
	return redirect(reverse('home'))

@transaction.atomic
def blogger_page(request, username):
	context={}
	users = User.objects.all()
	posts = []
	follow_mark = 0
	follow_user=User.objects.get(username = username)
	posts.extend(Post.get_posts(follow_user).order_by("-time"))
	context={'users':users, 'posts':posts, 'follow_mark':follow_mark, 'follow_users':follow_user}
	return render(request,'blog/base.html',context)

@login_required
@transaction.atomic
def add_post(request):

	new_post = Post(owner = request.user)
	form = PostForm(request.POST, request.FILES, instance = new_post)
	if not form.is_valid():
		context = {'form':form}
		return render(request,'blog/index.html',context)

	form.save()
	return redirect(reverse('manage'))

@login_required
@transaction.atomic
def delete_post(request,id):
	post = get_object_or_404(Post, owner = request.user, id = id)
	if post.picture:
		image_path = os.path.join(settings.MEDIA_ROOT, str(post.picture))
		os.unlink(image_path)
	post.delete()
	return redirect(reverse('manage'))

@transaction.atomic
def get_photo(request,id):
    post = get_object_or_404(Post, id=id)
    if not post.picture:
        raise Http404
    content_type = guess_type(post.picture.name)
    return HttpResponse(post.picture, mimetype=content_type)


@transaction.atomic
def register(request) :
	context = {}

	if request.method == "GET":
		context['form'] = RegistrationForm()
		return render(request,'blog/register.html',context)

	form = RegistrationForm(request.POST)
	context['form'] = form
	#Validation for the form
	if not form.is_valid():
		return render(request,'blog/register.html',context)

	new_user = User.objects.create_user(username = form.cleaned_data['username'],
										email = form.cleaned_data['email'],
										password = form.cleaned_data['password'],
										first_name = form.cleaned_data['first_name'],
										last_name = form.cleaned_data['last_name']
										)
	new_user.is_active = False
	new_user.save()

	token = default_token_generator.make_token(new_user)
	new_token = User_Token(user=new_user,token=token)
	new_token.save()

	email_body = "Welcome to Blog. Please click the link below to verify your email \
					address and complete the registration of your account: http://%s%s" % (request.get_host(), reverse('confirm', kwargs={'username' : str(new_user.username), 'token':str(token)}))
	
	send_mail(subject="Verify your email address",
				message = email_body,
				from_email = "qingqiaz@andrew.cmu.edu",
				recipient_list=[new_user.email])
	context ={'email': form.cleaned_data['email']}
	return render(request,'blog/need-confirmation.html', context)
	
	
@transaction.atomic
def register_confirm(request, username,token) :
	if request.method == "GET" :
		user_check = User.objects.get(username__exact = username)
		user_token = User_Token.objects.get(token=token)
		if user_check and user_token:
			user_check.is_active = True
			user_check.save()
			return render(request,'blog/confirmation.html')

    	else:
			Http404

def blogger_list(request):
	context={}
	if request.user.is_authenticated():
		users = User.objects.all().exclude(username = request.user)
	else:
		#get all the bloggers if the user doesn't login
		users = User.objects.all()

	posts = []
	follow_mark = 0
	follow_users=[]

	if request.user.is_authenticated:
		followers = Follower.objects.filter(user = request.user.id)
		if not followers:
			follow_mark=1
		for follower in followers:
			follow_users.append(follower.following)
	for follow_user in follow_users:
		posts.extend(Post.get_posts(follow_user).order_by("-time"))

	context={'users':users, 'posts':posts, 'follow_mark':follow_mark, 'follow_users':follow_users}
	return render(request, 'blog/blogger-list.html', context)


