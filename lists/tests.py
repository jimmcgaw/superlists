from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import home_page
from .models import Item

class ItemModelTest(TestCase):
  def test_saving_and_retrieving_items(self):
    first_item = Item()
    first_item.text = 'The first list item'
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.save()

    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'The first list item')
    self.assertEqual(second_saved_item.text, 'Item the second')


# Create your tests here.
class HomePageTest(TestCase):
  def test_root_url_resolves_to_home_page_view(self):
    found = resolve('/')
    self.assertEqual(found.func, home_page)

  def test_home_page_returns_correct_html(self):
    request = HttpRequest()
    response = home_page(request)
    expected_html = render_to_string('index.html', request=request)
    # response.content is in bytes, decode converts bytes to Python unicode string
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.content.decode()), len(expected_html))

  def test_home_page_can_save_post_request(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = 'A new list item'

    response = home_page(request)

    self.assertIn('A new list item', response.content.decode())

  def test_home_page_only_saves_items_when_necessary(self):
    request = HttpRequest()
    home_page(request)
    self.assertEqual(Item.objects.all().count(), 0)

  def test_home_page_only_saves_item_with_text(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = u''
    response = home_page(request)
    self.assertEqual(Item.objects.all().count(), 0)

  
