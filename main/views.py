from turtle import home, pos
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, JsonResponse

from main.models import Comment, Like, Post, DissLike
from main.models import PPImage
from main.models import Following
import json

def getIndex(request):
    if request.user.is_authenticated:
        following_users = Following.objects.filter(following_user_id=request.user.id)
        home_posts = []
        for user in following_users:
            posts = Post.objects.filter(user_id=user.followed_user_id.id)
            if posts:
                for post in posts:
                    pp_image = PPImage.objects.filter(user_id=post.user_id)
                    post_info = {
                        'posted_user': User.objects.filter(id=post.user_id.id)[0].username,
                        'imageURL': post.imageURL,
                        'id': post.id,
                        'profile_image': pp_image[0].imageURL
                    }
                    home_posts.append(post_info)
        return render(request, 'index.html', {
            'user': request.user,
            'posts': home_posts
        })
    else:
        return redirect('Login')

def getPostDetail(request, post_id):
    post = Post.objects.filter(id=post_id)
    user = User.objects.filter(username=post[0].user_id)
    pp_image_posted = PPImage.objects.filter(user_id=post[0].user_id)
    total_likes = Like.objects.filter(post_id=post_id).count()
    total_disslikes = DissLike.objects.filter(post_id=post_id).count()
    comments = Comment.objects.filter(post_id=post[0])
    comments_data = []
    for comment in comments:
        user = User.objects.filter(username=comment.user_id)
        pp_image = PPImage.objects.filter(user_id=comment.user_id)[0].imageURL.url
        comment_data = {
            'user_name': user[0].username,
            'profile_image': pp_image,
            'text': comment.content
        }
        comments_data.append(comment_data)
    return render(request, 'post_detail.html', {
        'post': post[0],
        'user': user[0],
        'profile_image_posted': pp_image_posted[0],
        'total_likes': total_likes,
        'total_disslikes': total_disslikes,
        'comments': comments_data
    })


def PostLike(request, post_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            post = Post.objects.filter(id=post_id)
            is_liked = Like.objects.filter(post_id=post[0], user_id=request.user)
            if is_liked:
                pass
            else:
                Like.objects.create(post_id=post[0], user_id=request.user)
            total_likes = Like.objects.filter(post_id=post_id).count()
            is_dissliked = DissLike.objects.filter(post_id=post[0], user_id=request.user)
            if is_dissliked:
                is_dissliked.delete()
            total_disslikes = DissLike.objects.filter(post_id=post_id).count()
            return JsonResponse({'context': {
                'total_likes': total_likes,
                'total_disslikes': total_disslikes
            }})
    else:
        return HttpResponseBadRequest('Invalid request')

def PostDissLike(request, post_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            post = Post.objects.filter(id=post_id)
            is_dissliked = DissLike.objects.filter(post_id=post[0], user_id=request.user)
            if is_dissliked:
                pass
            else:
                DissLike.objects.create(post_id=post[0], user_id=request.user)
            total_disslikes = DissLike.objects.filter(post_id=post_id).count()
            is_liked = Like.objects.filter(post_id=post[0], user_id=request.user)
            if is_liked:
                is_liked.delete()
            total_likes = Like.objects.filter(post_id=post_id).count()
            return JsonResponse({'context': {
                'total_disslikes': total_disslikes,
                'total_likes': total_likes
            }})
    else:
        return HttpResponseBadRequest('Invalid request')

def PostComment(request, post_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            comment_text = data.get('payload')
            post = Post.objects.filter(id=post_id)
            new_comment = Comment.objects.create(user_id=request.user, post_id=post[0], content=comment_text)
            pp_image = PPImage.objects.filter(user_id=request.user)
            return JsonResponse({
                'context': {
                    'profile_image': pp_image[0].imageURL.url,
                    'name': request.user.username,
                    'text': new_comment.content
                }
            })
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

def getProfile(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.filter(user_id= request.user.id)
        pp_image = PPImage.objects.filter(user_id=request.user.id)
        if pp_image:
            profile_image = pp_image[0]
        else:
            profile_image = {
                'imageURL': {
                    'url': 'deneme'
                }
            }
        followers_count = Following.objects.filter(followed_user_id=request.user.id).count()
        following_count = Following.objects.filter(following_user_id=request.user.id).count()
        return render(request, 'profile.html', {
            'user': user,
            'posts': posts,
            'profile_image': profile_image,
            'followers_count': followers_count,
            'following_count': following_count
        })
    else:
        return redirect('Login')

def getLoginForm(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)    # burada session ve cookie bilgileri olusturuluyor
            return redirect('Home')
        else:
            return render(request, 'login.html', {
                'error': 'Boyle Bir Kullanici Yok'
            })
    else:
        if request.user.is_authenticated:
            return redirect('Home')
        return render(request, 'login.html')

def getRegisterForm(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password= request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Bu Username Kullanılmaktadir'
            })
        elif User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Bu Email Kullanılmaktadir'
            })
        elif password != repassword:
            return render(request, 'register.html', {
                'error': 'Passwordler eslesmiyor'
            })
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
            user.save()
            return redirect('Login')

    else:
        if request.user.is_authenticated:
            return redirect('Home')
        else:
            return render(request, 'register.html')
    

def LogoutUser(request):
    logout(request)
    return redirect('Login')

def getPostForm(request):
    if request.method == 'POST':
        image = request.FILES['image']
        Post.objects.create(user_id=request.user, imageURL=image)
        return redirect('Profile')
    else:
        return render(request, 'Posting.html')

def getEditProfile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile_image = request.FILES['image']
            pp_image = PPImage.objects.filter(user_id=request.user)
            if pp_image:
                pp_image[0].imageURL = profile_image
                pp_image[0].save()
            else:
                PPImage.objects.create(user_id=request.user, imageURL=profile_image)
            user = User.objects.get(id=request.user.id)
            user.username = request.POST['username']
            user.save()
            return redirect('Profile')
        else:
            user = request.user
            return render(request, 'edit_profile.html', {
                    'user': user
                })
    else:
        return redirect('Login')
    

def getApi(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            return JsonResponse({'context': {
                'name': 'Salih',
                'lastname': 'Kalender'
            }})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

def getAnotherUser(request, user_name):
    if request.user.is_authenticated:
        user = User.objects.filter(username=user_name)
        if user[0]:
            if user[0].id == request.user.id:
                return redirect('Profile')
            else:
                posts = Post.objects.filter(user_id= user[0].id)
                pp_image = PPImage.objects.filter(user_id=user[0].id)
                followers_count = Following.objects.filter(followed_user_id=user[0].id).count()
                following_count = Following.objects.filter(following_user_id=user[0].id).count()
                is_following_this_user = Following.objects.filter(following_user_id=request.user.id, followed_user_id=user[0].id)
                is_following = False
                if is_following_this_user:
                    is_following = True  
                return render(request, 'another_user.html', {
                    'user': user[0],
                    'posts': posts,
                    'profile_image': pp_image[0],
                    'followers_count': followers_count,
                    'following_count': following_count,
                    'is_following': is_following
                })

        else:
            return render(request, 'another_user.html', {
                'error': 'BOYLE BIT KULLANICI YOK'
            })
    else:
        return redirect('Login')

def followingAnotherUser(request, user_name):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        user = User.objects.filter(username=user_name)
        user_id = user[0].id
        is_following = Following.objects.filter(followed_user_id=user_id, following_user_id=request.user.id)
        if is_following:
            return JsonResponse({'context': {
                'data': 'Zaten takip ediyorsun',
            }})
        else:
            Following.objects.create(followed_user_id=user[0], following_user_id=request.user)
            return JsonResponse({'context': {
                'count':  Following.objects.filter(followed_user_id=user_id).count()
            }})
    else:
        return HttpResponseBadRequest('Invalid request')

def NofollowingAnotherUser(request, user_name):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        user = User.objects.filter(username=user_name)
        user_id = user[0].id
        Following.objects.filter(followed_user_id=user_id, following_user_id=request.user.id).delete()
        return JsonResponse({'context': {
            'count': Following.objects.filter(followed_user_id=user_id).count(),
        }})
    else:
        return HttpResponseBadRequest('Invalid request')

def UserSearch(request):
    if request.user.is_authenticated:
        users = User.objects.filter().exclude(id=request.user.id)
        return render(request, 'user_search.html', {
            'users': users
        })
    else:
        return redirect('Login')

def PostLikeUsers(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=post_id)
        userLikes = Like.objects.filter(post_id=post[0])
        users = []
        for like in userLikes:
            user = User.objects.filter(username=like.user_id)
            data = {
                'username': user[0].username,
                'id': user[0].id
            }
            users.append(data)
        return render(request, 'user_search.html', {
            'users': users
        })
    else:
        return redirect('Login')

def PostDissLikeUsers(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=post_id)
        userDissLikes = DissLike.objects.filter(post_id=post[0])
        users = []
        for like in userDissLikes:
            user = User.objects.filter(username=like.user_id)
            data = {
                'username': user[0].username,
                'id': user[0].id
            }
            users.append(data)
        return render(request, 'user_search.html', {
            'users': users
        })
    else:
        return redirect('Login')

def getProfileFollowers(request):
    if request.user.is_authenticated:
        followers = Following.objects.filter(followed_user_id=request.user)
        users = []
        for follow in followers:
            user = User.objects.filter(username=follow.following_user_id)
            data = {
                'username': user[0].username,
                'id': user[0].id
            }
            users.append(data)
        return render(request, 'user_search.html', {
            'users': users
        })
    else:
        return redirect('Login')

def getProfileFollowings(request):
    if request.user.is_authenticated:
        followings = Following.objects.filter(following_user_id=request.user)
        users = []
        for follow in followings:
            user = User.objects.filter(username=follow.followed_user_id)
            data = {
                'username': user[0].username,
                'id': user[0].id
            }
            users.append(data)
        return render(request, 'user_search.html', {
            'users': users
        })
    else:
        return redirect('Login')

def getAnotherUserFollowers(request, user_name):
    if request.user.is_authenticated:
        selected_user = User.objects.filter(username=user_name)
        followers = Following.objects.filter(followed_user_id=selected_user[0])
        users = []
        for follow in followers:
            user = User.objects.filter(username=follow.following_user_id)
            data = {
                'username': user[0].username,
                'id': user[0].id
            }
            users.append(data)
        return render(request, 'user_search.html', {
            'users': users
        })
    else:
        return redirect('Login')


def getAnotherUserFollowings(request, user_name):
    if request.user.is_authenticated:
        selected_user = User.objects.filter(username=user_name)
        followings = Following.objects.filter(following_user_id=selected_user[0])
        users = []
        for follow in followings:
            user = User.objects.filter(username=follow.followed_user_id)
            data = {
                'username': user[0].username,
                'id': user[0].id
            }
            users.append(data)
        return render(request, 'user_search.html', {
            'users': users
        })
    else:
        return redirect('Login')
