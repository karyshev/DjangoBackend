import time
from django.test import TestCase
from django.contrib.auth.models import User
from tutorial.quickstart.models import Follow

# Create your tests here.
class UsersTestCase(TestCase):
    def test_simple(self):
        self.assertEqual(12 + 8, 20)

    def test_unknown_url(self):
        response = self.client.get('/incorrect/')
        self.assertEqual(response.status_code, 404)

    def test_list_without_user(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
        self.assertEqual(response.json(), {
                              "count": 0,
                              "next": None,
                              "previous": None,
                              "results": []
                        })

    def test_list_user_with_users(self):
        User.objects.create(username='Kelly')
        time.sleep(0.001)
        User.objects.create(username='Jhon')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        'url': 'http://testserver/v1/users/Jhon/',
                        'username': 'Jhon',
                        'first_name': '',
                        'last_name': '',
                        'email': ''
                    },
                    {
                        'url': 'http://testserver/v1/users/Kelly/',
                        'username': 'Kelly',
                        'first_name': '',
                        'last_name': '',
                        'email': ''
                    }
                ]
            }
        )

class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Kevin')
        self.user2 = User.objects.create(username='Tom')
        self.user3 = User.objects.create(username='Putin')
        Follow.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exist(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follow.objects.count(), 1)

    def test_new_follow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user3.username}/')
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(Follow.objects.count(), 2)
        self.assertIsNotNone(Follow.objects.get(
            follower=self.user1,
            follows=self.user3,
        ))

    def test_unfollow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)

    def test_follow_yourself_failed(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)

    def test_unfollow_not_exist_return_fail(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)

