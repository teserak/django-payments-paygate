from __future__ import unicode_literals
import re
import xml.etree.ElementTree as ET

from django.utils.translation import ugettext_lazy as _

from payments.forms import CreditCardPaymentFormWithName

RESPONSE_STATUS = {
    'Approved': 'confirmed',
    'Not Done': 'duplicate',
    'Declined': 'rejected'}

class PaymentForm(CreditCardPaymentFormWithName):

    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()

        if not self.errors:
            if not self.payment.transaction_id:
                data = {
                    'cname': cleaned_data['name'],
                    'cc': cleaned_data['number'],
                    'exp': cleaned_data['expiration'].strftime('%m%Y'),
                    'budp': 0,
                    'cvv': cleaned_data['cvv2']
                }

                response = self.provider.get_payment_response(data)

                body = re.search(
                    '(<protocol.*?></protocol>)',
                    response.text,
                    re.DOTALL
                )

                response_data = None
                if body:
                    root = ET.fromstring(body.group(0))
                    response_data = list(root)
                    if response_data:
                        response_data = response_data[0].attrib


                if response.ok and \
                        not response_data.get('ecode', False) and \
                        RESPONSE_STATUS.get(response_data.get('sdesc', ''), False):

                    self.payment.transaction_id = response_data['tid']
                    self.payment.change_status(
                        RESPONSE_STATUS.get(response_data.get('sdesc', ''), 'error')
                    )
                else:
                    errors = [response_data.get('edesc')]
                    self._errors['__all__'] = self.error_class(errors)
                    self.payment.change_status('error')
        return cleaned_data
