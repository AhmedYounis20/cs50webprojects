from django.urls import path
from django.views.generic.base import RedirectView
from . import views
app='enc'
urlpatterns = [
    path('' , RedirectView.as_view(url='wiki/')),
    path("wiki/", views.index, name="index"),
    path ('wiki/<str:ent_name>',views.view_entry,name='entry'),
    path('newPage',views.new_page,name='new_page'),
    path('random',views.random_paging,name='rand'),
    path('searchResult',views.search_section,),
    path('edit/<str:entry>',views.edited)
]
