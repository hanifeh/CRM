import weasyprint
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from . import models
from .forms import QuoteItemCreateFormSet
from organization.models import Organization


class ViewCreateQuote(LoginRequiredMixin, TemplateView):
    """
    Create one quote and many quote item
    """
    template_name = "create-quote.html"

    def get(self, *args, **kwargs):
        formset = QuoteItemCreateFormSet(queryset=models.QuoteItem.objects.none())
        organizations = Organization.objects.filter(creator=self.request.user)
        return self.render_to_response({'formset': formset, 'organizations': organizations})

    def post(self, *args, **kwargs):
        formset = QuoteItemCreateFormSet(data=self.request.POST)
        if formset.is_valid():
            organization = Organization.objects.get(pk=self.request.POST['organization'], creator=self.request.user)
            quote = models.Quote.objects.create(creator=self.request.user, organization=organization)
            for form in formset:
                form.instance.quote = quote
                try:
                    form.save()
                except:
                    quote.delete()
                    messages.error(self.request, 'Invalid input.')
                    return redirect(reverse_lazy('quote:create-quote'))
            messages.success(self.request, 'Quote create successfully.')
            return redirect(reverse_lazy("quote:list-quotes"))
        else:
            messages.error(self.request, 'Invalid input.')
            return redirect(reverse_lazy('quote:create-quote'))


class ViewListQuote(LoginRequiredMixin, ListView):
    """
    :return List of Quotes for one user
    """
    model = models.Quote
    template_name = 'list-quotes.html'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        mode = self.request.GET.get('mode', None)
        if mode == 'organization':
            quotes = models.Quote.objects.filter(organization__name__contains=search, creator=self.request.user)
        elif mode == 'product':
            quotes = models.Quote.objects.filter(quoteitem__product__name__contains=search, creator=self.request.user)
        else:
            quotes = models.Quote.objects.filter(creator=self.request.user)
        return quotes


class ViewDetailQuote(LoginRequiredMixin, DetailView):
    """
    :return one Quote
    """
    model = models.Quote
    template_name = 'detail-quote.html'

    def get_queryset(self):
        quote = models.Quote.objects.filter(pk=self.kwargs['pk'], creator=self.request.user)
        return quote


class GetPDFQuote(LoginRequiredMixin, DetailView):
    """
    generate Quote to pdf
    """
    template_name = 'pdf-quote.html'
    model = models.Quote

    def get_queryset(self):
        quote = models.Quote.objects.filter(pk=self.kwargs['pk'], creator=self.request.user)
        return quote

    def get(self, request, *args, **kwargs):
        g = super().get(request, *args, **kwargs)
        rendered_content = g.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')
