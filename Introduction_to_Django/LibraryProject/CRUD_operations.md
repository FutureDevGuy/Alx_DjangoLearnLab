### Django Shell CRUD Operations

Here are the documented CRUD operations performed in the Django shell.

#### 1. Create Operation

Command:

from bookshelf.models import Book
book1 = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

Output:

<Book: 1984>

#### 2. Retrieve Operation

Command:

book = Book.objects.get(title="1984")
print(book)
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Year: {book.publication_year}")

Output:

1984
Title: 1984
Author: George Orwell
Year: 1949

#### 3. Update Operation

Command:

book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)

Output:

Nineteen Eighty-Four

#### 4. Delete Operation

Command:

book.delete()
print(Book.objects.all())

Output:

<QuerySet []>