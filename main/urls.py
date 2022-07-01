from django.urls import path
from . import views

urlpatterns = [
    path('', views.getIndex, name='Home'),
    path('post-detail/<int:post_id>', views.getPostDetail, name='Post Detail'),
    path('post-detail/<int:post_id>/like', views.PostLike, name='Post Like'),
    path('post-detail/<int:post_id>/like/users', views.PostLikeUsers, name='Post Like Users'),
    path('post-detail/<int:post_id>/disslike/users', views.PostDissLikeUsers, name='Post DissLike Users'),
    path('post-detail/<int:post_id>/disslike', views.PostDissLike, name='Post Disslike'),
    path('post-detail/<int:post_id>/comment', views.PostComment, name='Post Comment'),
    path('profile', views.getProfile, name='Profile'),
    path('profile/followers', views.getProfileFollowers, name='Profile Followers'),
    path('profile/followings', views.getProfileFollowings, name='Profile Followings'),
    path('user_search', views.UserSearch, name='UserSearch'),
    path('login', views.getLoginForm, name='Login'),
    path('register', views.getRegisterForm, name='Register'),
    path('logout', views.LogoutUser, name='Logout'),
    path('posting', views.getPostForm, name='Posting'),
    path('edit_profile', views.getEditProfile, name='EditProfile'),
    path('api_deneme', views.getApi, name='GetApi'),
    path('user/<str:user_name>', views.getAnotherUser, name='AnotherUser'),
    path('user/<str:user_name>/followers', views.getAnotherUserFollowers, name='AnotherUser Followers'),
    path('user/<str:user_name>/followings', views.getAnotherUserFollowings, name='AnotherUser Followings'),
    path('user/<str:user_name>/following', views.followingAnotherUser, name='AnotherUser Follow'),
    path('user/<str:user_name>/no_following', views.NofollowingAnotherUser, name='AnotherUser UnFollow'),
]
