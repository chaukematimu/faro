import logging
from typing import TYPE_CHECKING

from frappe import _
import frappe
from erpnext.selling.doctype.customer.customer import Customer as ERPNextCustomer
from frappe.geo.doctype.country.country import Country
from frappe.types import DF

logger = logging.getLogger(__name__)


class Customer(ERPNextCustomer):
    if TYPE_CHECKING:
        is_passport_or_id_number: DF.Literal["ID Number", "Passport"]
        passport_or_id_number: DF.Data
        passport_country: Country

    @property
    def can_lay_buy(self):
        rules = [
            self.customer_type == "Individual",
            self.is_passport_or_id_number != "",
        ]
        if self.is_passport_or_id_number == "ID Number":
            rules.append(self.is_valid_id_number_customer)
        if self.is_passport_or_id_number == "Passport":
            rules.append(self.is_valid_passport_customer)
        return all(rules)

    def validate(self):
        super().validate()
        if self.is_passport_or_id_number == "ID Number":
            if not self.is_valid_id_number_customer:
                if not self.is_valid_id_number_customer:
                    frappe.throw(
                        _(
                            "Invalid ID Number rules"
                        )
                    )
        if self.is_passport_or_id_number == "Passport":
            if not self.is_valid_passport_customer:
                frappe.throw(
                    _(
                        "Invalid Passport rules"
                    )
                )

    @property
    def is_valid_id_number_customer(self):
        rules = [
            self.passport_or_id_number.isdigit(),
            len(self.passport_or_id_number) == 13
            # TODO : validate ID using Luhn algorithm
        ]
        return all(rules)

    @property
    def is_valid_passport_customer(self):
        rules = [
            len(self.passport_or_id_number) > 6,
            self.passport_country is not None and self.passport_country != 'South Africa'
        ]
        return all(rules)
