from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.conf import settings

from pyi2phosts.lib.utils import get_b32
from pyi2phosts.extsources.models import ExternalSource
from pyi2phosts.postkey.models import i2phost
from pyi2phosts.postkey.templatetags import paginator

class LocalTemplateView(TemplateView):
    """ Renders some template with passing some local config variables """

    def get_context_data(self, **kwargs):
        context = super(LocalTemplateView, self).get_context_data(**kwargs)
        context.update({
            'title': settings.SITE_NAME,
            'domain': settings.DOMAIN,
            'b64': settings.MY_B64,
            'b32': get_b32(settings.MY_B64)
        })
        return context


class LocalObjectList(ListView):
    """ Renders some list of objects """

    def get_context_data(self, **kwargs):
        context = super(LocalObjectList, self).get_context_data(**kwargs)
        context.update({
            'title': settings.SITE_NAME,
        })
        return context


class FaqView(LocalObjectList):
    """ Renders list of external sources for hosts.txt """

    queryset = ExternalSource.objects.filter(active=True)
    template_name = 'faq.html'
    context_object_name = 'sources_list'


class HostsListsView(LocalObjectList):
    """ Renders list of active hosts """

    def get_queryset(self):
        allowed_orders = ['name', 'last_seen', 'date_added']
        self.order_by = self.request.GET.get('order', 'name')
        if self.order_by not in allowed_orders:
            self.order_by = 'name'
        qs = super(HostsListsView, self).get_queryset()
        return qs.order_by(self.order_by)

    def get_context_data(self, **kwargs):
        """ we should pass order_by to template to not lose it while paginating """
        context = super(LocalObjectList, self).get_context_data(**kwargs)
        context.update({
            'order': self.order_by,
        })
        return context

    queryset = i2phost.objects.filter(activated=True)
    template_name = 'browse.html'
    context_object_name = 'host_list'
    paginate_by = 40
