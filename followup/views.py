from django.contrib.auth.mixins import LoginRequiredMixin
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

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.organization = models.Organization.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('organizations:detail-of-organization', kwargs={'slug': self.kwargs['slug']})


class ViewDetailFollowUp(LoginRequiredMixin, DetailView):
    """
    :return one Follow up
    """
    model = models.FollowUp
    template_name = 'detail-followup.html'

    def get_queryset(self):
        organization = models.FollowUp.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return organization
