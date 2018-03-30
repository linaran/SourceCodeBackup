from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from rest_framework import permissions, status, generics

from .models import Tweet
from .forms import CreateTweetForm, LoginForm, RegisterForm
from .serializers import TweetSerializer, UserSerializer
from .permissions import IsOwner, ReadOnly

activity_log_path = "rest_activity_log.txt"
browser_index = "HTTP_USER_AGENT"


# region Standard Web App
def register_login(request):
    form_login = LoginForm()
    form_register = RegisterForm()

    context = {
        'form_login': form_login,
        'form_register': form_register,
    }
    return render(request, 'faketweeter/register_login.html', context)


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('faketweeter:all_tweets'))
    else:
        raise Http404("This url accepts only posts.")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('faketweeter:all_tweets'))
        else:
            return HttpResponseRedirect(reverse('faketweeter:register_login'))
    else:
        raise Http404('This url accepts only posts.')


@login_required()
def all_tweets(request):
    form = CreateTweetForm()
    tweets = Tweet.objects.filter(
            user=request.user
    ).order_by('-date_published')[:20]
    return render(request, 'faketweeter/list_tweets.html', {'tweets': tweets, 'form': form})


@login_required()
def logout_user(request):
    logout(request)
    return redirect('faketweeter:register_login')


@login_required()
def tweet_detail(request, tweet_id, show_edit=False):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    if show_edit:
        form = CreateTweetForm(request.POST, instance=tweet)
    else:
        form = None

    context = {
        'tweet': tweet,
        'show_edit': show_edit,
        'form': form
    }
    return render(request, 'faketweeter/tweet_detail.html', context)


@login_required()
def create_tweet(request):
    if request.method == "POST":
        form = CreateTweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.date_published = timezone.now()
            tweet.user = request.user
            tweet.save()
            return HttpResponseRedirect(reverse('faketweeter:all_tweets'))
    return HttpResponseRedirect(reverse('faketweeter:all_tweets'))


@login_required()
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.user == tweet.user:
        if request.method == "POST":
            form = CreateTweetForm(request.POST, instance=tweet)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.date_published = timezone.now()
                tweet.user = request.user
                tweet.save()
                return HttpResponseRedirect(reverse('faketweeter:all_tweets'))
        else:
            return tweet_detail(request, tweet.id, show_edit=True)
    else:
        return HttpResponseForbidden()


@login_required()
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.user == tweet.user:
        tweet.delete()
        return HttpResponseRedirect(reverse('faketweeter:all_tweets'))
    else:
        return HttpResponseForbidden()


# endregion


def log_activity(path, browser):
    if browser is None:
        browser = "NOT_BROWSER"
    with open(activity_log_path, "a") as activity_file:
        activity_file.write(path + " " + str(str.split(browser)) + "\n")


class UserList(generics.ListCreateAPIView):
    """
    Pregled korisnika.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ReadOnly,)

    def finalize_response(self, request, response, *args, **kwargs):
        log_activity(self.request.path, self.request.META.get(browser_index))
        return super().finalize_response(request, response, *args, **kwargs)


class UserDetail(generics.RetrieveAPIView):
    """
    Detaljni pregled nekog korisnika.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ReadOnly,)



    def finalize_response(self, request, response, *args, **kwargs):
        log_activity(self.request.path, self.request.META.get(browser_index))
        return super().finalize_response(request, response, *args, **kwargs)


class UserTweetList(generics.ListAPIView):
    """
    Pregled tweetova nekog korisnika.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        tweets = Tweet.objects.filter(user_id=pk)
        if not tweets:
            raise Http404
        return tweets

    def finalize_response(self, request, response, *args, **kwargs):
        log_activity(self.request.path, self.request.META.get(browser_index))
        return super().finalize_response(request, response, *args, **kwargs)


class TweetList(generics.ListCreateAPIView):
    """
    Javni pregled i objava tweetova.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def finalize_response(self, request, response, *args, **kwargs):
        log_activity(self.request.path, self.request.META.get(browser_index))
        return super().finalize_response(request, response, *args, **kwargs)


class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Korisnik upravlja vlastitim tweetom.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def finalize_response(self, request, response, *args, **kwargs):
        log_activity(self.request.path, self.request.META.get(browser_index))
        return super().finalize_response(request, response, *args, **kwargs)
