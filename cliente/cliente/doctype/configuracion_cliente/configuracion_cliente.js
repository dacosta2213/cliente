// Copyright (c) 2019, CIAI and contributors
// For license information, please see license.txt

frappe.ui.form.on('Configuracion Cliente', {
	refresh: function(frm) {

	},
	validar: function(frm) {
		if (frm.doc.client_id && frm.doc.client_secret) {
			frappe.call({
							method: "cliente.cliente.doctype.configuracion_cliente.configuracion_cliente.validar",
							args:{
								id: frm.doc.client_id,
								secret: frm.doc.client_secret
							},
							callback: function (data) {
								var success = data.message
								if (success.includes("Invalido")) {
									frm.set_value('valido', 0);
									frappe.msgprint ('Se HA ENCONTRADO UN ERROR. REVISA TUS CREDENCIALES.');
									frm.save();
								} else {

									frm.set_value('valido', 1);
									frappe.msgprint('VALIDACION EXITOSA!');
									frm.save();
								}
							}
		  });
	  } else {
			frappe.msgprint('Debes ingresar ID y Clave Secreta');
		}
	}
});
