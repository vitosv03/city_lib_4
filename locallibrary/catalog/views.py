from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # выполнение задания 2 из блока 5
    num_genres = Genre.objects.all().count()
    num_books_with_titles = Book.objects.filter(title__icontains='').count

    # Number of visits to this view,
    # as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    # Затем переменная num_visits передаётся в шаблон
    # через переменную контекста context.
    return render(
        request,
        'index.html',
        context={'num_books': num_books,
                 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors,
                 'num_genres': num_genres,
                 'num_books_with_titles': num_books_with_titles,
                 'num_visits': num_visits  # num_visits appended
                 },
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """    Generic class-based view listing books on loan to current user.    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    # слэш "\" значит перенос строки, чтоб нагляднее было, а то строка длинная
    def get_queryset(self):
        return BookInstance.objects. \
            filter(borrower=self.request.user). \
            filter(status__exact='o'). \
            order_by('due_back')


class LoanedBooksByAllListView(LoginRequiredMixin, generic.ListView):
    """    для СТАФФ список всек книг по задолжностям    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 5

    # слэш "\" значит перенос строки, чтоб нагляднее было, а то строка длинная
    def get_queryset(self):
        return BookInstance.objects. \
            filter(status__exact='o'). \
            order_by('due_back')

