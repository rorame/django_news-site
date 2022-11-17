from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

# добавляем миксин, чтобы даже по ссылке неавторизованный пользователь не мог добавить новость
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm

# from .utils import MyMixin


# отправка писем
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                             'login@gmail.com',
                             ['test@mail.com'],
                             fail_silently=True)
            if mail:
                messages.success(request, 'The email has been sent!')
                return redirect('contact')
            else:
                messages.error(request, 'Error sending email')
        else:
            messages.error(request, 'Validation error')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Sign up is successful')
            return redirect('home')
        else:
            messages.error(request, 'Sign up fault')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request=request, user=user)
            return redirect('home')
    else:
         form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(ListView,
               # MyMixin
               ):
    model = News
    paginate_by = 2

    # если хотим занименить шаблон по умолчанию, на свой другой
    # template_name = 'news/home_news_list.html'
    # context_object_name = 'news'

    # только для статичных объектов
    # extra_context = {'title': 'Main'}

    # mixin_prop = 'hello world'

    # для динамичных данных
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main'
        # приводим к верхнему регистру фразу Hellow world через MyMixin
        # context['title'] = self.get_upper('Main')
        # context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        # загрузка связных данных не отложенно, а жадно
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    # не разрешаем показ пустых списков
    allow_empty = False
    paginate_by = 2

    # если хотим занименить шаблон по умолчанию, на свой другой
    # template_name = 'news/home_news_list.html'
    # context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    # template_name = 'news/home_news_detail.html.html'
    # pk_url_kwarg = 'news_id'
    # context_object_name = 'news_item'


# более общие наследуемые классы нужно размесить первее
class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # неавторизованных пользователей выкидывает на страницу регистрации
    login_url = '/admin/'
    # raise_exception = True

#     если хотим проигнорировать метод get_absolute_url в нашей модели
#     success_url = reverse_lazy('home')

# def index(request):
#     news = News.objects.all()
#     contex = {'news': news,
#               'title': 'News feed'}
#     return render(request, 'news/index_bootstrap.html', contex)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#
#     return render(request, 'news/category.html',
#                   {'news': news,
#                    'category': category}
#                   )


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html',
#                   {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # ** - распаковка словарей
#             # метод create для форм, которые не связаны с моделью
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html',
#                   {'form': form})
