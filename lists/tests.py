from django.core.urlresolvers import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string


from lists.models import Item, List
from lists.views import home_page


class ListViewTest(TestCase):

    def test_list_view_displays_all_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        client = Client()
        # client.get('/lists/the-only-list-in-the-world/')
        response = client.get('/lists/the-only-list-in-the-world/')

        self.assertIn('itemey 1', response.content)
        self.assertIn('itemey 2', response.content)
        self.assertTemplateUsed(response, 'list.html')



class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content, expected_html)


    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertEqual(Item.objects.all().count(), 0)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        client = Client()
        response = client.post('/lists/new', 
                                data={'item_text': 'A new list item'})

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')

        # self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')



class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list = List()
        list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list
        second_item.save()

        saved_lists = List.objects.all()
        self.assertEqual(saved_lists.count(), 1)
        self.assertEqual(saved_lists[0], list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list)

        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list)


class ListViewTest(TestCase):

    def test_list_view_displays_all_items(self):
        list = List.objects.create()
        Item.objects.create(text='itemey 1', list=list)
        Item.objects.create(text='itemey 2', list=list)