import frappe
import time
from sqlalchemy import create_engine
from sqlalchemy import text
import json


def setup_db():
    attr = frappe.get_single('Mssql Configurations')
    username = attr.username
    password = attr.get_password('password')
    ip = attr.ipport
    db_name = attr.db_name
    engine = create_engine(
        f"mssql+pymssql://{attr.username}:{password}@{ip}/{db_name}",
        echo=True)
    return engine


@frappe.whitelist()
def send_to_mssql(frm):
    engine = setup_db()
    frm = json.loads(frm)
    company = frappe.get_doc('Company', frm.get('company'))
    try:
        with engine.connect() as conn:
            conn.execute(
                text(
                    "insert into OBTF (TransId, RefDate, DueDate, WritingDate, Memo) values (:trans_id, :ref_date, :due_date, :writing_date, :memo)"
                ), {
                    "trans_id": frm.get("name"),
                    "ref_date": frm.get("posting_date"),
                    "due_date": frm.get("creation"),
                    "writing_date": frm.get("creation"),
                    "memo": frm.get("user_remark")
                })

            for account in frm.get("accounts"):
                conn.execute(
                    text(
                        "insert into BTF1 (TransId, Line_ID, Account, Debit, Credit, FCCurrency) values (:trans_id, :line_id, :account, :debit, :credit, :fc_currency)"
                    ), {
                        "trans_id": account.get("name"),
                        "line_id": account.get("idx"),
                        "account": account.get("account"),
                        "debit": account.get("debit"),
                        "credit": account.get("credit"),
                        "fc_currency": company.default_currency
                    })
            conn.commit()
        return {"success": True}
    except:
        return {"success": False, "message": "check db configurations"}
