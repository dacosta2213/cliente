# -*- coding: utf-8 -*-
# Copyright (c) 2019, CIAI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt
from frappe.utils.file_manager import save_url
import shutil
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from xml.dom import minidom
import requests
from datetime import datetime
import string
from random import *

class Certificado(Document):
	pass

@frappe.whitelist()
def factura(name):
	c = frappe.get_doc("Certificado", name)
	factura = frappe.new_doc("Sales Invoice")
	factura.customer = c.expedido
	factura.is_pos = 0
	factura.append('items', { 'item_code': 'Certificado'})
	factura.insert()
	frappe.db.set_value("Certificado", name , 'cert_status', "Facturado con " + factura.name)
	frappe.msgprint('Factura  Agregada:  <a href="#Form/Sales%20Invoice/' + factura.name + '">  ' + factura.name + ' </a>' )

    # doc = frappe.get_doc({
	# 	"doctype": "Sales Invoice",
	# 	"customer": self.expedido ,
	# 	"lng": lng,
	# 	"lat": lat
	# 	})
    # doc.insert(ignore_permissions=True)
    # frappe.db.commit()



@frappe.whitelist()
def acuerdo(ciclo):
	response = requests.request("GET", "https://ciai.totall.mx/api/method/ciai.api.acuerdo?ciclo=" + ciclo)
	return response.text

@frappe.whitelist()
def ciclo(ciclo):
	response = requests.request("GET", "https://ciai.totall.mx/api/method/ciai.api.get_lect_todas?ciclo=" + ciclo)
	return response.json().get('message')

@frappe.whitelist()
def validar(id,secret,docname,ciclo):
	c = frappe.get_doc("Certificado", docname)
	caracteres = string.ascii_letters  + string.digits
	# caracteres = string.ascii_letters + string.punctuation + string.digits
	numeros = string.digits
	uuid = "".join(choice(numeros) for x in range(32))
	sello = "".join(choice(caracteres) for x in range(345))

	response = requests.request("GET", "https://ciai.totall.mx/api/method/ciai.api.validar_cert?id=" + id + "&secret=" + secret + "&ciclo=" + ciclo)
	if response.json().get('status') == 'error':
		frappe.msgprint((response.json().get('message')), "ERROR ENCONTRADO AL CERTIFICAR")
	else:
		cadena = response.json().get('message')
		if cadena == 'Certificado Invalido':
			frappe.db.set_value("Certificado", docname , 'cadena', response.json().get('message') )
			frappe.msgprint('Certificado Invalido')
			return cadena
		frappe.db.set_value("Certificado", docname , 'cert_status', "Certificado")
		frappe.db.set_value("Certificado", docname , 'cadena', response.json().get('message') )
		frappe.db.set_value("Certificado", docname , 'uuid', uuid)
		frappe.db.set_value("Certificado", docname , 'sello', sello)

		folio = c.name
		fecha = c.fecha
		cert= c.client_id
		secret = c.client_secret
		expedido = c.expedido
		direccion = c.direccion

		xmldata = """<?xml version="1.0" encoding="UTF-8"?>
<cert:Certificado xmlns:cert="https://www.ciai.totall.mx/ciai" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://www.ciai.totall.mx/ciai/cfdv1.xsd"
Version="1.0" Folio="{folio}" Fecha="{fecha}" ID="{cert}-{secret}"  NoCertificado="{cert}">
<cert:Emisor ID="CIAI-0000001" Nombre="CIAI TOTALL MX"/>
<cert:Receptor ID="{cert}" Nombre="{expedido}" Direccion="{direccion}"/>
<cert:Respuesta UUID="{uuid}" Sello="{sello}" Cadena="{cadena}" />
</cert:Certificado>""".format(**locals())

		dest = '/home/frappe/frappe-bench/sites/cliente.totall.mx/public/files/' + uuid
		f = open( dest + '.xml',"w+")
		f.write(xmldata)
		f.close()
		save_url( "/files/" + uuid +  ".xml" , uuid + ".xml" , "Certificado" , c.name , "Home/Attachments" , 0)
		frappe.msgprint(str(c.name) + " certificado exitosamente "  )
		c.reload()

	frappe.errprint(response)
	return response.text
