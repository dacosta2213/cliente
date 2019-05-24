# -*- coding: utf-8 -*-
# Copyright (c) 2019, CIAI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests

class ConfiguracionCliente(Document):
	pass

@frappe.whitelist()
def validar(id,secret):
	headers = {
	    'Content-Type': "application/json"
	}
	response = requests.request("GET", "https://ciai.totall.mx/api/method/ciai.api.validar_cert?id=" + id + "&secret=" + secret)
	return response.text
