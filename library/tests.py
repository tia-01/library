from django.test import TestCase
from .models import Book

class BookTestCase(TestCase):
    def test_create_book(self):
        book = Book.objects.create( title="Test Book",author="Author One", genre="science" )
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Author One")
        self.assertTrue(book.is_available)  

    def test_update_book(self):
        book = Book.objects.create(title="Initial Book",author="Author Two",genre="fiction")
        book.title = "Updated Book"
        book.is_available = False
        book.save()
        updated_book = Book.objects.get(pk=book.pk)
        self.assertEqual(updated_book.title, "Updated Book")
        self.assertFalse(updated_book.is_available)

    def test_delete_book(self):
        book = Book.objects.create( title="Delete Me", author="Author Three",genre="mystery"
        )
        book.delete()
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(title="Delete Me")