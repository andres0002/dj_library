# django
from django.test import TestCase as dj_TestCase, Client
# third
# own
from apps.user.tests.factories import UserFactory

# Create your tests here.

# use Client HTTP.
class UserWithClientTestCase(dj_TestCase):
    def setUp(self):
        self.client = Client() # http.
        self.user = UserFactory.build()
    
    def test_login_user_fail(self):
        self.user.username = 'user'
        self.user.set_password('user')
        self.user.save()
        response = self.client.login(username='user',password='user1') # crea una session temporal mientras se execute las tests.
        # print(response)
        self.assertEqual(response, False)
    
    def test_login_user(self):
        self.user.username = 'user'
        self.user.set_password('user')
        self.user.save()
        # response = self.client.post(
        #     '/accounts/login/', # url -> path.
        #     { # data -> request.
        #         'username':'user',
        #         'password':'user'
        #     }
        # )
        # print(response.status_code)
        # print(response.content)
        # login -> el que trae integrado django por default -> solo devuelve true o false.
        response = self.client.login(username='user',password='user') # crea una session temporal mientras se execute las tests.
        # print(response)
        self.assertEqual(response, True)
    
    def test_user_list(self):
        # superuser login.
        self.user.username = 'superuser'
        self.user.is_superuser = True
        self.user.set_password('superuser')
        self.user.save()
        # get.
        self.client.login(username='superuser',password='superuser')
        response = self.client.get(
            '/user/users_table/', # url -> path.
            HTTP_X_REQUESTED_WITH='XMLHttpRequest' # que es un request por ajax.
        )
        # post.
        # response = self.client.post('url', {'data':'data'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest') # example.
        # print(response.json()) # show data.
        self.assertEqual(response.status_code, 200)

# command -> para execute tests -> 'python manage.py test'