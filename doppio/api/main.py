import frappe

@frappe.whitelist(allow_guest=True)
def ping():
    frappe.throw("Hello")
    return "Pong"