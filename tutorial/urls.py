from django.urls import include, path
from django.contrib import admin
# from rest_framework import routers
from tutorial.quickstart import views
from tutorial.quickstart.router import SwitchDetailRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter
from tutorial.quickstart.views import FollowViewSet

switch_router = SwitchDetailRouter()
router = ExtendedDefaultRouter()
user_router = router.register(r'users', views.UserViewSet)

user_router.register('tweets', views.UserTweetViewSet, 'user-tweets', ['username'])
user_router.register('follows', views.UserFollowsViewSet, 'user-follows', ['username'])
user_router.register('followed', views.UserFollowedViewSet, 'user-followers', ['username'])

router.register(r'tweets', views.TweetViewSet)
switch_router.register(r'follow', FollowViewSet)
router.register(r'feed', views.FeedViewSet)


urlpatterns = [
    path('v1/', include(switch_router.urls)),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
