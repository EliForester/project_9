from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^sign_out/$', views.sign_out, name='sign_out'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.edit_menu, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^menu/new/$', views.create_new_menu, name='menu_new'),
]
