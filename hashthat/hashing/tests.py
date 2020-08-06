from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import Hash
import os
from django.core.exceptions import ValidationError
import time


class FunctionalTestCase(TestCase):

    def setUp(self) -> None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "venv\Scripts\geckodriver.exe")
        self.browser = webdriver.Firefox(executable_path=path)

    def test_there_is_homepage(self):
        self.browser.get('http://127.0.0.1:8000/')
        self.assertIn('Enter hash here', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        time.sleep(5)
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)


    def tearDown(self) -> None:
        self.browser.quit()





class UnitTestCase(TestCase):

    def test_home_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        form = HashForm(data={'text': 'hello'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        test_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", test_hash)

    def saveHash(self):
        hash_object = Hash()
        hash_object.text = 'hello'
        hash_object.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash_object.save()
        return hash_object

    def test_hash_object(self):
        hash_object = self.saveHash()
        pulled_hash = Hash.objects.get(hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(hash_object.text, pulled_hash.text)

    def test_viewing_hash(self):
        hash_object = self.saveHash()
        response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertContains(response,'hello')

    def test_bad_data(self):
        with self.assertRaises(ValidationError,):
            hash = Hash(hash="2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824sadas")
            hash.full_clean()

