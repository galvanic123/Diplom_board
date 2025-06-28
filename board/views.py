from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Advertisement, Category, Comment
from .forms import AdvertisementForm, CommentForm


class AdListView(ListView):
    model = Advertisement
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset.order_by('-created_at')


class AdDetailView(DetailView):
    model = Advertisement
    template_name = 'board/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/ad_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/ad_edit.html'

    def form_valid(self, form):
        messages.success(self.request, 'Объявление успешно обновлено!')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('ad_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Advertisement
    template_name = 'board/ad_delete.html'
    success_url = reverse_lazy('ad_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('ad_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


def add_comment(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ad = ad
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
    return redirect('ad_detail', pk=ad.pk)