from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import NoteForm
from .models import Note


class NoteListView(ListView):
    """
    Display a list of all notes, ordered by title.
    """
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    ordering = ['title']


class NoteDetailView(DetailView):
    """
    Display the details of a specific note.
    """
    model = Note
    template_name = 'notes/note_detail.html'


class NoteCreateView(SuccessMessageMixin, CreateView):
    """
    Handle the creation of a new note.
    If the form is valid, save the note and redirect to the note detail.
    Otherwise, render the form with errors.
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_message = 'Note created successfully.'

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})


class NoteUpdateView(SuccessMessageMixin, UpdateView):
    """
    Handle the update of an existing note.
    If the form is valid, save the changes and redirect to the note detail.
    Otherwise, render the form with errors.
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_message = 'Note updated successfully.'

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})


class NoteDeleteView(SuccessMessageMixin, DeleteView):
    """
    Handle the deletion of a note.
    Confirm deletion on POST request, then redirect to the note list.
    """
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')
    success_message = 'Note deleted successfully.'