import unittest

from pyramid import testing

class PyramidDevViewTests(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()
		
	def tearDown(self):
		testing.tearDown()
		
	def test_home(self):
		from .views import PyramidDevViews
		
		request = testing.DummyRequest()
		inst = PyramidDevViews(request)
		response = inst.home()
		self.assertEqual('Home View', response['page_title'])
		
class PyramidDevFunctionalTests(unittest.TestCase):
	def setUp(self):
		from pyramiddev import main
		app = main({})
		from webtest import TestApp
		
		self.testapp = TestApp(app)
		
	def test_home(self):
		res = self.testapp.get('/', status=200)
		self.assertIn(b'PyramidDevViews - Home View', res.body)
		
