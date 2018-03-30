from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'faketweeter'
urlpatterns = [
    url(r'^all_tweets/$', views.all_tweets, name='all_tweets'),
    url(r'^register_login/$', views.register_login, name='register_login'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^create_tweet/$', views.create_tweet, name='create_tweet'),
    url(r'^(?P<tweet_id>[0-9]+)$', views.tweet_detail, name='tweet_detail'),
    url(r'^(?P<tweet_id>[0-9]+)/edit', views.edit_tweet, name='edit_tweet'),
    url(r'^(?P<tweet_id>[0-9]+)/delete$', views.delete_tweet, name='delete_tweet'),
]

api = r'^api/'
urlpatterns += [
    url(api + r'users/(?P<pk>[0-9]+)/tweets', views.UserTweetList.as_view()),
    url(api + r'users/(?P<pk>[0-9]+)', views.UserDetail.as_view()),
    url(api + r'users/$', views.UserList.as_view(), name='list_users'),
    url(api + r'tweets/(?P<pk>[0-9]+)', views.TweetDetail.as_view()),
    url(api + r'tweets/$', views.TweetList.as_view(), name='list_tweets'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
