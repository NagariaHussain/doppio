import frappe
import random

@frappe.whitelist(allow_guest=True)
def ping():
    return f"Ponggg, your random number {random.randint(10, 100)}"