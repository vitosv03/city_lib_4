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

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """    Функция просмотра для обновления определенного экземпляра BookInstance библиотекарем  """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если это запрос POST, обработайте данные формы
    if request.method == 'POST':

        # Создайте экземпляр формы и заполните его данными из запроса (привязки):
        form = RenewBookForm(request.POST)

        # Проверьте, действительна ли форма:
        if form.is_valid():
            # обрабатываем данные в form.cleaned_data по мере необходимости
            # (здесь мы просто записываем их в поле due_back модели)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # перенаправить на новый URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # Если это GET (или любой другой метод), создайте форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # значение поле дата по умолчанию = proposed_renewal_date
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(CreateView):
    # использует суффикс '_form'
    model = Author
    fields = '__all__'
    # значение поля по умолчанию
    initial = {'date_of_death': '12/10/2016', }


class AuthorUpdate(UpdateView):
    # использует суффикс '_form'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    # после удаления перейти на страницу просмотра всех книг
    # author_confirm_delete.html, где "_confirm_delete" это суффикс
    # его надо использовать или изменить, так как мы наследуем класс DeleteView
    # а этот класс ищет файлы по суффиксу
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    # использует суффикс '_form'
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    # использует суффикс '_form'
    model = Book
    fields = ['title', 'summary', 'isbn', 'genre', 'language']


class BookDelete(DeleteView):
    model = Book
    # после удаления перейти на страницу просмотра всех книг
    # book_confirm_delete.html, где "_confirm_delete" это суффикс
    # его надо использовать или изменить, так как мы наследуем класс DeleteView
    # а этот класс ищет файлы по суффиксу
    success_url = reverse_lazy('books')
