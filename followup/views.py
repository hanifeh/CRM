from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView
from . import models, forms


class FollowUpDetailView(LoginRequiredMixin, DetailView):
    """
    view for one Follow up detail
    """
    model = models.FollowUp
    template_name = 'detail-followup.html'

    def get_queryset(self):
        followup = models.FollowUp.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return followup


class FollowUpCreateView(LoginRequiredMixin, CreateView):
    """
    view for create new Follow up
    """
    model = models.FollowUp
    form_class = forms.FollowUpCreateForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw.update({'creator': self.request.user})
        return kw

    def form_invalid(self, form):
        return JsonResponse({'massages': "Title or body cannot be blank."}, status=400)

    def form_valid(self, form):
        if not form.instance.organization.creator == self.request.user:
            return JsonResponse({'massages': "Organization not found."}, status=400)
        try:
            form.instance.creator = self.request.user
            self.object = form.save()
        except:
            return JsonResponse({'massages': "Title must be unique."}, status=400)
        return JsonResponse({'massages': "Follow Up created successfully."}, status=201)
