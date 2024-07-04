from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView, UpdateView, DeleteView, CreateView
from .models import Cotegory, News, Comment
from .forms import ContactForm, CommentForm
from .custom import UserLoginTest, LoginRequiredMixin
from hitcount.views import HitCountDetailView, get_hitcount_model, HitCountMixin

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    comment = news.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()


    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        context['hit_counted'] = hit_count_response.hit_counted
        context['hit_message'] = hit_count_response.hit_message
        context['total_hits'] = hits
    context = {
        "news":news,
        "comment":comment,
        "comment_form":comment_form,
        'new_comment':new_comment
    }
    return render(request, 'news/single_page.html', context)




class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cotegorys'] = Cotegory.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_news'] = News.published.all().filter(cotegory__name='Mahalliy')[:5]
        context['xorij_xabarlari'] = News.published.all().filter(cotegory__name="Xorij").order_by('-publish_time')[:5]
        context['texnalogiya_xabarlari'] = News.published.all().filter(cotegory__name="Texnalogiya").order_by('-publish_time')[:5]
        context['sport_xabarlari'] = News.published.all().filter(cotegory__name="Sport").order_by('-publish_time')[:5]
        return context



class ContactView(LoginRequiredMixin,TemplateView):
    template_name = 'news/contact.html'
    
    def get(self, request, *args, **kwargs):
        form = ContactForm
        context = {
            'form':form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            form.save()
        
        context = {
            "form":form
        }
        return render(request, "news/contact.html", context)



class LocalPageView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = News.published.all().filter(cotegory__name='Mahalliy')
        return news
    


class SportPageview(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = News.published.all().filter(cotegory__name='Sport')
        return news
    


class ForingPageview(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'foring_news'

    def get_queryset(self):
        news = News.published.all().filter(cotegory__name='Xorij')
        return news
    


class TechnologyPageView(ListView):
    model = News
    template_name = 'news/texnalogiya.html'
    context_object_name = 'technalogy_news'

    def get_queryset(self):
        news = News.published.all().filter(cotegory__name='Texnalogiya')
        return news
    


class NewsUpdateView(UserLoginTest, UpdateView):
    template_name = 'news_edits/news_edit.html'
    model = News
    fields = ['title', 'body', 'image', 'cotegory']



class NewsDeleteView(UserLoginTest, DeleteView):
    model = News
    template_name = 'news_edits/news_delete.html'
    success_url = reverse_lazy('home')


class NewsCreateView(UserLoginTest, CreateView):
    model = News
    template_name = 'news_edits/news_create.html'
    fields = ('title','title_uz','title_en','title_ru','slug', 
              'body', 'body_uz', 'body_en', 'body_ru', 'image', 
              'cotegory', 'status')



