

from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Menu, Item, Ingredient
from django.contrib.auth.models import User
from datetime import datetime
import pytz


class ProjectTestCase(TestCase):

    def setUp(self):
        expiration_date = datetime(2015,1,1, tzinfo=pytz.timezone('Asia/Tokyo'))
        self.test_menu = Menu.objects.create(season='aki',
                                             expiration_date=expiration_date)

        chef = User.objects.create(first_name='test_chef', last_name='chef_test')
        self.test_item = Item.objects.create(name='tonkatsu',
                                             description='fried pork',
                                             chef=chef,
                                             standard=True)

        self.ingredient1 = Ingredient.objects.create(name='pork')
        self.ingredient2 = Ingredient.objects.create(name='panko')

        self.test_item.ingredients.add(self.ingredient1)
        self.test_item.ingredients.add(self.ingredient2)
        self.test_item.save()

        self.test_menu.items.add(self.test_item)

    def test_db_results(self):
        menu_db_data = Menu.objects.count()
        item_db_data = Item.objects.count()
        ingredient_db_data = Ingredient.objects.count()
        self.assertEqual(menu_db_data, 1)
        self.assertEqual(item_db_data, 1)
        self.assertEqual(ingredient_db_data, 2)

    def test_menu_list_all(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertTemplateUsed('menu/list_all_current_menus.html')
        self.assertTrue(self.test_menu.season in
                        resp.content.decode('UTF-8').lower())

    def test_menu_detail(self):
        resp = self.client.get(reverse('menu_detail',
                                       args=[self.test_menu.pk]))
        self.assertTemplateUsed('menu/menu_detail.html')
        self.assertContains(resp, self.test_menu.season)
        self.assertTrue(self.test_item.name in
                        resp.content.decode('UTF-8').lower())

    def test_item_detail(self):
        pass

