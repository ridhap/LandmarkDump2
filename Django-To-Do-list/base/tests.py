from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
# from todo_maker  import app 
class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.user={
            
            'username':'ridha',
            'password1':'ridha123',
            'password2':'ridha123',
        }
    
        self.user_short_password={
            'username':'ridha',
            'password1':'tes',
            'password2':'tes',
        }
        self.user_unmatching_password={

            'username':'ridha',
            'password1':'12345678',
            'password2':'12345678',
        }
        # self.login_url={
        #     'username':"",
        #     'password1':'password1',
        #     'password2':'password1',

        # }

        return super().setUp()



class RegisterTest(BaseTest):
   def test_can_view_page_correctly(self):
       response=self.client.get(self.register_url)
       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'base/register.html')

   def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

   def test_cant_register_user_withshortpassword(self):
        response=self.client.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,400)

   def test_cant_register_user_with_unmatching_passwords(self):
        response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
        self.assertEqual(response.status_code,400)

class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'base/login.html')
    
    def test_login_success(self):
        self.client.post(self.register_url,self.user,format='text/html')
        user=User.objects.filter(username=self.user['username']).first()
        user.is_active=True
        user.save()
        response= self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cantlogin_with_no_username(self):
        response= self.client.post(self.login_url,{'password':'pass12345','username':''},format='text/html')
        self.assertEqual(response.status_code,401)

    def test_cantlogin_with_no_password(self):
        response= self.client.post(self.login_url,{'username':'pass12345','password':''},format='text/html')
        self.assertEqual(response.status_code,401)

