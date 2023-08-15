// Copyright (c) 2023, ahmed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mssql Configurations", {
  // refresh: function(frm) {
  // }
});

frappe.ui.form.on("Journal Entry", {
  before_submit: async function (frm) {
    let resp = await frappe.call({
      method: "mssql_integration.api.mssql_server.send_to_mssql",
      type: "POST",
      async: false,
      args: {
        frm: frm.doc,
      },
    });
    if (!resp.message.success) {
      frm.reload_doc().then(() => frappe.throw(resp.message.message));
    }
  },
});
