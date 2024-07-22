import logging

from erpnext.selling.doctype.customer.customer import Customer as ERPNextCustomer

logger = logging.getLogger(__name__)


class Customer(ERPNextCustomer):

    def validate(self):
        super().validate()
