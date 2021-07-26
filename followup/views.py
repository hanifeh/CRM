from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView
from . import models, forms


class ViewDetailFollowUp(LoginRequiredMixin, DetailView):
    """
    :return one Follow up
    """
    model = models.FollowUp
    template_name = 'detail-followup.html'

    def get_queryset(self):
        organization = models.FollowUp.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return organization


class ViewCreateFollowUp(LoginRequiredMixin, CreateView):
    """
    create new Follow up
    """
    models = models.FollowUp
    form_class = forms.FollowUpCreateForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw.update({'creator': self.request.user})
        return kw

    def form_invalid(self, form):
        return JsonResponse({'massages': "Title or body cannot be blank."}, status=400)

    def form_valid(self, form):
        try:
            form.instance.creator = self.request.user
            self.object = form.save()
        except:
            return JsonResponse({'massages': "Title must be unique."}, status=400)
        return JsonResponse({'massages': "Follow Up created successfully."}, status=201)