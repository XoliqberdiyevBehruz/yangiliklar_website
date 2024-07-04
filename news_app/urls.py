from django.urls import path
from .views import  news_detail, ContactView, HomePageView, TechnologyPageView, LocalPageView, SportPageview, ForingPageview, NewsUpdateView, NewsDeleteView, NewsCreateView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('xorij-xabarlari/', ForingPageview.as_view(), name='xorij'),
    path('sport-xabarlari/', SportPageview.as_view(), name='sport'),
    path('texnalogiya-xabarlari/', TechnologyPageView.as_view(), name='texnalogiya'),
    path('mahalliy-xabarlar/', LocalPageView.as_view(), name='mahalliy'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('<slug:news>/', news_detail, name='detail_page'),
    path('<slug>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),


]