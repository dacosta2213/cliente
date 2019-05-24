// Copyright (c) 2019, CIAI and contributors
// For license information, please see license.txt

frappe.ui.form.on('Certificado', {
	refresh: function(frm) {
		$('.btn[data-fieldname=cert]').addClass('btn-primary');
		$('.btn[data-fieldname=lecturas]').addClass('btn-primary');
		$('.btn[data-fieldname=aprobar]').addClass('btn-primary');

		// if (frm.doc.cert_status == "Certificado") {
		// 	$('.page-icon-group').hide()
		// } else {
		// 	$('.page-icon-group').show()
		// }

	},
	aprobar: function(frm) {
		if (frm.doc.valido) {
			frappe.call({
							method: "cliente.cliente.doctype.certificado.certificado.acuerdo",
							args:{
								ciclo: frm.doc.ciclo
							},
							callback: function (r) {
								cur_frm.set_value("acuerdo", 1)
								frappe.msgprint(r.message,'Mensaje del Servidor')
							}
			})
		}
	},
	ciclo: function(frm) {
		$(cur_frm.fields_dict.tabla_html.wrapper).empty();
		frm.save()
	},
	lecturas_old: function(frm) { //Para hacer llamados a server externos en el frontend
		$.get("https://ciai.totall.mx/api/method/ciai.api.acuerdo?ciclo=" + frm.doc.ciclo ,function (r) {
							frappe.msgprint(r.message,'Mensaje del Servidor')
						});
	},
	lecturas: function(frm) {
		  if (frm.doc.valido) {
					frappe.call({
									method: "cliente.cliente.doctype.certificado.certificado.ciclo",
									args:{
										ciclo: frm.doc.ciclo
									},
									callback: function (r) {
										console.log(r.message)
										var result_table = $(frappe.render_template('lecturas', {
											lecturas: r.message
										}) )
										result_table.appendTo(cur_frm.fields_dict.tabla_html.wrapper);
									}
				  })
			}
	},
	cert: function(frm) {
		  if (frm.doc.valido) {
					frappe.call({
									method: "cliente.cliente.doctype.certificado.certificado.validar",
									args:{
										ciclo: frm.doc.ciclo,
										id: frm.doc.client_id,
										secret: frm.doc.client_secret,
										docname: frm.doc.name
									},
									callback: function (r) {
										// let m = JSON.parse(r.message)
										// console.log(m.message)
										// cur_frm.set_value("cadena", m.message)
										// cur_frm.set_value("cert_status", "Certificado")
										// setTimeout(frm.savesubmit(), 2000)
									}
				  })
			}
	},
	onload: function(frm){
		frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Configuracion Cliente",
					filters: {
					"name": "Configuracion Cliente"
					}
				},
				callback: function (data) {
					if (frm.doc.__unsaved)  {
						v = data.message;
						cur_frm.set_value("client_id", v.client_id);
						cur_frm.set_value("valido", v.valido);
						cur_frm.set_value("client_secret", v.client_secret);
					}
				}
				})
	}
});
