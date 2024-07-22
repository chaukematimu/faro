import frappe


def execute():
    if frappe.db.has_column("Customer", "can_lay_buy"):
        customers = frappe.get_all("Customer")
        for customer in customers:
            customer = frappe.get_doc("Customer", customer)
            customer.can_lay_buy = customer.eligible_for_lay_buy()
            customer.save()
