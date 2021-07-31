import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView
from . import models, tasks
from .forms import QuoteItemCreateFormSet
from organization.models import Organization


class QuoteCreateView(LoginRequiredMixin, CreateView):
    """
    view for Create one quote and many quote item
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


class QuoteListView(LoginRequiredMixin, ListView):
    """
    view for List of Quotes for one user
    """
    model = models.Quote
    template_name = 'list-quotes.html'
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        mode = self.request.GET.get('mode', None)
        if mode == 'organization':
            quotes = models.Quote.objects.filter(organization__name__contains=search, creator=self.request.user)
        elif mode == 'product':
            quotes = models.Quote.objects.filter(quoteitem__product__name__contains=search, creator=self.request.user)
        else:
            quotes = models.Quote.objects.filter(creator=self.request.user)
        return quotes.order_by('-id')


class QuoteDetailView(LoginRequiredMixin, DetailView):
    """
    view for one Quote detail
    """
    model = models.Quote
    template_name = 'detail-quote.html'

    def get_queryset(self):
        quote = models.Quote.objects.filter(pk=self.kwargs['pk'], creator=self.request.user)
        return quote


class QuoteGetPDF(LoginRequiredMixin, DetailView):
    """
    generate Quote to pdf
    """
    template_name = 'pdf-quote.html'
    model = models.Quote

    def get(self, request, *args, **kwargs):
        quote = models.Quote.objects.get(pk=self.kwargs['pk'], creator=self.request.user)
        html = render_to_string('pdf-quote.html', {'object': quote})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=quote{quote.pk}.pdf'
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/quote.css')])
        return response


class QuoteDownloadPDF(LoginRequiredMixin, DetailView):
    """
    Download Quote in pdf
    """
    template_name = 'pdf-quote.html'
    model = models.Quote

    def get(self, request, *args, **kwargs):
        quote = models.Quote.objects.get(pk=self.kwargs['pk'], creator=self.request.user)
        html = render_to_string('pdf-quote.html', {'object': quote})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=quote{quote.pk}.pdf'
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/quote.css')])
        return response


@require_http_methods(["GET"])
@login_required
def send_email(request, pk):
    """
    send quote to organization by email
    """
    quote = models.Quote.objects.get(pk=pk, creator=request.user)
    if quote:
        body = render_to_string('email-quote.txt', {'object': quote})
        email = quote.organization.organization_email
        sender = request.user.username
        tasks.send_email_task.delay(body, sender, email)
        messages.success(request, 'Send email request saved successfully.')
        return redirect(reverse_lazy('quote:list-quotes'))
    else:
        messages.error(request, 'Permission denied.')
        return redirect(reverse_lazy('quote:list-quotes'))
