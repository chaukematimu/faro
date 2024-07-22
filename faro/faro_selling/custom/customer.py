import logging
from typing import TYPE_CHECKING

from frappe import _
import frappe
from erpnext.selling.doctype.customer.customer import Customer as ERPNextCustomer
from frappe.types import DF

logger = logging.getLogger(__name__)


class Customer(ERPNextCustomer):
    if TYPE_CHECKING:
        is_passport_or_id_number: DF.Literal["ID Number", "Passport"]
        passport_or_id_number: DF.Data
        passport_country: DF.Data

    @property
    def can_lay_buy(self):
        return False

    def validate(self):
        if self.is_passport_or_id_number == "ID Number":
            self.validate_id_number()
        super().validate()

    def validate_id_number(self):
        rules = [
            self.passport_or_id_number.isdigit(),
            len(self.passport_or_id_number) == 13
            # TODO : validate ID using Luhn algorithm
        ]
        if not all(rules):
            frappe.throw(
                _(
                    "Invalid ID Number"
                )
            )
