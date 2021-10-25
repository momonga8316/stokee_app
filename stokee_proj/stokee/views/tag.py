from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from stokee.models import Tag

class TagListView(ListView):
    queryset = Tag.objects.annotate(num_posts=Count('post'))
        
class TagPostView(ListView):
    model = Tag
    template_name = 'stokee/tag_detail.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
