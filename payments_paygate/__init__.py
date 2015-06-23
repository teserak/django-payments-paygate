from __future__ import unicode_literals

import requests
import json

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden

from .forms import PaymentForm
from payments import BasicProvider

# use .format(**dict) to fill
REQUEST_XML_TEMPLATE = '''\
<protocol ver="4.0" pgid="{pgid}" pwd="{pwd}"><authtx cref="{cref}" cname="{cname}" cc="{cc}" exp="{exp}" budp="{budp}" amt="{amt}" cur="{cur}" cvv="{cvv}" bno="" /></protocol>\
'''

class PayGateProvider(BasicProvider):

    def __init__(self, *args, **kwargs):
        self.pgid = kwargs.pop('pgid')
        self.pwd = kwargs.pop('pwd')
        self.endpoint = kwargs.pop(
            'endpoint', 'https://www.paygate.co.za/payxml/process.trans')
        super(PayGateProvider, self).__init__(*args, **kwargs)
        if not self._capture:
            raise ImproperlyConfigured(
                'PayGate does not support pre-authorization.')

    def get_transactions_data(self):
        data = {
            'pgid': self.pgid,
            'pwd': self.pwd,
            'amt': int(float(self.payment.total) * 100),
            'cur': self.payment.currency,
            'cref': self.payment.description,
        }
        return data

    def get_product_data(self, extra_data=None):
        data = self.get_transactions_data()

        if extra_data:
            data.update(extra_data)

        return data

    def get_payment_response(self, extra_data=None):
        post = self.get_product_data(extra_data)
        return requests.post(self.endpoint, data=REQUEST_XML_TEMPLATE.format(**post))

    def get_form(self, data=None):
        return PaymentForm(data=data, payment=self.payment, provider=self,
                           action='')

    def process_data(self, request):
        return HttpResponseForbidden('FAILED')
