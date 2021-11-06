from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


# Define the admin class
class BookInline(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # exclude = ['date_of_death']
    # Добавьте встроенный список перечня Book
    # в представление списка Author ,
    # используя тот же самый подход,
    # который мы применили для Book/BookInstance.
    inlines = [BookInline]
    extra = 0

# Register the admin class with the associated model


# Register the Admin classes for Book using the decorator

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'display_language')
    inlines = [BooksInstanceInline]

    extra = 0


# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    # Для представления списка BookInstance , добавьте код
    # для отображения книги, статуса, даты возврата, и id
    # (вместо значения по умолчанию возвращаемого  __str__() ).
    list_display = ('book', 'status', 'due_back', 'id')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
