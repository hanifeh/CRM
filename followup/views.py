from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from . import models, forms


class ViewCreateFollowUp(LoginRequiredMixin, CreateView):
    """
    create new Follow up
    """
    models = models.FollowUp
    form_class = forms.FollowUpCreateForm
    template_name = 'create-followup.html'

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw.update({'creator': self.request.user})
        organ = models.Organization.objects.get(slug=self.kwargs['slug'])
        kw.update({'organization': organ})
        return kw

    def form_invalid(self, form):
        super(ViewCreateFollowUp, self).form_invalid(form)
        return JsonResponse({'massages': "Title or body cannot be blank."}, status=400)

    def form_valid(self, form):
        try:
            form.instance.creator = self.request.user
            form.instance.organization = models.Organization.objects.get(slug=self.kwargs['slug'])
            super().form_valid(form)
        except:
            return JsonResponse({'massages': "Title must be unique."}, status=400)
        return JsonResponse({'massages': "Follow Up created successfully."}, status=201)

    def get_success_url(self):
        return reverse('organizations:detail-organization', kwargs={'slug': self.kwargs['slug']})


class ViewDetailFollowUp(LoginRequiredMixin, DetailView):
    """
    :return one Follow up
    """
    model = models.FollowUp
    template_name = 'detail-followup.html'

    def get_queryset(self):
        organization = models.FollowUp.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return organization
