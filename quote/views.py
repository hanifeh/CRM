from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import QuoteItem, Quote
from .forms import QuoteItemCreateFormSet
from organization.models import Organization
from product.models import Product


class ViewCreateQuote(LoginRequiredMixin, TemplateView):
    """
    Create one quote and many quote item
    """
    template_name = "create-quote.html"

    def get(self, *args, **kwargs):
        formset = QuoteItemCreateFormSet(queryset=QuoteItem.objects.none())
        organizations = Organization.objects.filter(creator=self.request.user)
        products = Product.objects.all()
        return self.render_to_response({'formset': formset, 'organizations': organizations, 'products': products})

    def post(self, *args, **kwargs):
        formset = QuoteItemCreateFormSet(data=self.request.POST)
        if formset.is_valid():
            organization = Organization.objects.get(pk=self.request.POST['organization'])
            quote = Quote.objects.create(creator=self.request.user, organization=organization)
            for form in formset:
                form.instance.quote = quote
                try:
                    form.save()
                except:
                    quote.delete()
                    messages.error(self.request, 'Invalid input.')
                    return redirect(reverse_lazy('quote:create-quote'))
            messages.success(self.request, 'Quote create successfully.')
            return redirect(reverse_lazy("quote:create-quote"))
        else:
            messages.error(self.request, 'Invalid input.')
            return redirect(reverse_lazy('quote:create-quote'))
        # return self.render_to_response({'form': formset})
