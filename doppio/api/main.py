import frappe


@frappe.whitelist()
def ping():
	return "Ponggggg!"


@frappe.whitelist()
def get_my_todos():
	todos = frappe.get_all("ToDo", fields=["description", "status", "priority", "name"])
	return todos
