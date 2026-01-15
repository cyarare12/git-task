from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    def setUp(self):
        # Create a Note object for testing
        Note.objects.create(title='Test Note', content='This is a test note.')

    def test_note_has_title(self):
        # Test that a Note object has the expected title
        note = Note.objects.get(id=1)
        self.assertEqual(note.title, 'Test Note')

    def test_note_has_content(self):
        # Test that a Note object has the expected content
        note = Note.objects.get(id=1)
        self.assertEqual(note.content, 'This is a test note.')

    def test_note_str_method(self):
        # Test the __str__ method of the Note model
        note = Note.objects.get(id=1)
        self.assertEqual(str(note), 'Test Note')


class NoteViewTest(TestCase):
    def setUp(self):
        # Create a Note object for testing views
        Note.objects.create(title='Test Note', content='This is a test note.')

    def test_note_list_view(self):
        # Test the note-list view
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_note_detail_view(self):
        # Test the note-detail view
        note = Note.objects.get(id=1)
        response = self.client.get(reverse('note_detail', args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note.')

    def test_note_create_view_get(self):
        # Test the note-create view GET request
        response = self.client.get(reverse('note_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create New Note')

    def test_note_create_view_post(self):
        # Test the note-create view POST request
        response = self.client.post(reverse('note_create'), {
            'title': 'New Test Note',
            'content': 'Content for new test note.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Note.objects.count(), 2)  # Should now have 2 notes

    def test_note_update_view_get(self):
        # Test the note-update view GET request
        note = Note.objects.get(id=1)
        response = self.client.get(reverse('note_update', args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Note')

    def test_note_update_view_post(self):
        # Test the note-update view POST request
        note = Note.objects.get(id=1)
        response = self.client.post(reverse('note_update', args=[str(note.id)]), {
            'title': 'Updated Test Note',
            'content': 'Updated content for test note.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        note.refresh_from_db()
        self.assertEqual(note.title, 'Updated Test Note')

    def test_note_delete_view_get(self):
        # Test the note-delete view GET request
        note = Note.objects.get(id=1)
        response = self.client.get(reverse('note_delete', args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete Note')

    def test_note_delete_view_post(self):
        # Test the note-delete view POST request
        note = Note.objects.get(id=1)
        response = self.client.post(reverse('note_delete', args=[str(note.id)]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertEqual(Note.objects.count(), 0)  # Should now have 0 notes
