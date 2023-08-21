// Copyright (c) 2023, ahmed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mssql Configurations", {
  // refresh: function(frm) {
  // }
});

frappe.ui.form.on("Journal Entry", {
  refresh(frm) {
    if (frm.doc.docstatus) {
      frm.add_custom_button(__("Send to SAP"), function () {
        frappe.msgprint(__("Sending to SAP ....."));
        let resp = frappe.call({
          method: "mssql_integration.api.mssql_server.send_to_mssql",
          type: "POST",
          async: false,
          args: {
            frm: frm.doc,
          },
          callback(resp) {
            if (!resp.message.success) {
              frm.reload_doc().then(() => frappe.throw(resp.message.message));
            } else {
              frappe.hide_msgprint();
            }
          },
        });
      });
    }
  },
});
