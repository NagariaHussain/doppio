import frappe

@frappe.whitelist(allow_guest=True)
def ping():
    return "Ponggggg!"