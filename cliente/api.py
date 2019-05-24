# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import json
from frappe import _
import frappe.utils
import frappe.async
import frappe.sessions
import frappe.utils.file_manager
import frappe.desk.form.run_method
from frappe.utils.response import build_response
import datetime
from datetime import date,datetime
import requests
import pytz


@frappe.whitelist()
def ruta(login_manager):
    ruta = frappe.db.get_value("User", login_manager.user,"ruta_login")
    frappe.errprint(ruta)
    frappe.local.response["home_page"] = ruta
