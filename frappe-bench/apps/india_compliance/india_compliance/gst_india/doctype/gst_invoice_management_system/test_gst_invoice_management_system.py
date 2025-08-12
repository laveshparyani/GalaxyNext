# Copyright (c) 2024, Resilient Tech and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase, change_settings
from frappe.utils import add_to_date

from india_compliance.gst_india.doctype.gst_invoice_management_system.gst_invoice_management_system import (
    IMSReconciler,
    get_data_for_upload,
    get_period_options,
    update_previous_ims_action,
)
from india_compliance.gst_india.doctype.purchase_reconciliation_tool.test_purchase_reconciliation_tool import (
    create_gst_inward_supply,
)
from india_compliance.gst_india.utils.api import create_integration_request
from india_compliance.gst_india.utils.tests import create_purchase_invoice

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class TestGSTInvoiceManagementSystem(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.gst_ims = frappe.get_doc(
            {
                "doctype": "GST Invoice Management System",
                "company": "_Test Indian Registered Company",
                "company_gstin": "24AAQCA8719H1ZC",
                "return_period": "122024",
            }
        )

        default_args = {
            "bill_date": "2024-12-11",
            "return_period_2b": "122024",
            "gen_date_2b": "2024-12-11",
        }

        create_gst_inward_supply(
            **default_args,
            bill_no="BILL-24-00001",
            previous_ims_action="No Action",
            action="Pending"
        )
        cls.invoice_name_1 = frappe.get_value(
            "GST Inward Supply", {"bill_no": "BILL-24-00001"}
        )

        create_gst_inward_supply(
            **default_args,
            bill_no="BILL-24-00002",
            previous_ims_action="Rejected",
            action="No Action",
            previous_action="Pending"
        )
        cls.invoice_name_2 = frappe.get_value(
            "GST Inward Supply", {"bill_no": "BILL-24-00002"}
        )

        cls.pinv = create_purchase_invoice(
            **{
                "bill_no": "BILL-24-00001",
                "bill_date": "2024-12-11",
                "items": [
                    {
                        "item_code": "_Test Trading Goods 1",
                        "qty": 1,
                    }
                ],
                "supplier": "_Test Registered Supplier",
                "supplier_gstin": "24AABCR6898M1ZN",
            }
        )

    def test_update_action(self):
        # Reconcile invoice with bill_no "BILL-24-00001"
        IMSReconciler().reconcile(
            frappe._dict(
                {
                    "company": self.gst_ims.company,
                    "company_gstin": self.gst_ims.company_gstin,
                }
            )
        )

        # Test matched invoice
        self.gst_ims.update_action((self.invoice_name_1,), "Rejected")
        ims_action, action, previous_action = frappe.get_all(
            "GST Inward Supply",
            filters={"name": self.invoice_name_1},
            fields=["ims_action", "action", "previous_action"],
            as_list=True,
        )[0]
        self.assertEqual(ims_action, "Rejected")
        self.assertEqual(action, "Pending")
        self.assertEqual(previous_action, "No Action")

        # Test unmatched invoice
        frappe.db.set_value("GST Inward Supply", self.invoice_name_1, "link_name", "")
        self.gst_ims.update_action((self.invoice_name_1,), "Rejected")
        ims_action, action, previous_action = frappe.get_all(
            "GST Inward Supply",
            filters={"name": self.invoice_name_1},
            fields=["ims_action", "action", "previous_action"],
            as_list=True,
        )[0]
        self.assertEqual(ims_action, "Rejected")
        self.assertEqual(action, "Ignore")
        self.assertEqual(previous_action, "Pending")

        # Test invoice with previous IMS Action "Rejected"
        self.gst_ims.update_action((self.invoice_name_2,), "No Action")
        ims_action, action, previous_action = frappe.get_all(
            "GST Inward Supply",
            filters={"name": self.invoice_name_2},
            fields=["ims_action", "action", "previous_action"],
            as_list=True,
        )[0]
        self.assertEqual(ims_action, "No Action")
        self.assertEqual(action, "Pending")
        self.assertEqual(previous_action, "Pending")

    def test_data_for_upload(self):
        # Empty data
        upload_data = get_data_for_upload("24AAQCA8719H1ZC", "save")
        self.assertDictEqual(upload_data, {})

        # Data for save request
        self.gst_ims.update_action((self.invoice_name_1,), "Accepted")

        upload_data = get_data_for_upload("24AAQCA8719H1ZC", "save")
        self.assertEqual("BILL-24-00001", upload_data["b2b"][0]["inum"])

        # Data for reset request
        self.gst_ims.update_action((self.invoice_name_2,), "No Action")

        upload_data = get_data_for_upload("24AAQCA8719H1ZC", "reset")
        self.assertEqual("BILL-24-00002", upload_data["b2b"][0]["inum"])

    def test_update_previous_ims_action(self):
        self.gst_ims.update_action((self.invoice_name_1,), "Accepted")
        self.gst_ims.update_action((self.invoice_name_2,), "No Action")

        upload_data = get_data_for_upload("24AAQCA8719H1ZC", "save")
        data = {
            "body": {
                "action": "SAVE",
                "data": {
                    "invdata": upload_data,
                },
            },
        }

        create_integration_request(
            data=data,
            reference_doctype="GST Invoice Management System",
            reference_name="GST Invoice Management System",
            request_id="12345",
        )
        error_report = {
            "b2b": [
                {
                    "stin": "24AABCR6898M1ZN",
                    "inv": [{"rtnprd": "122024", "inum": "BILL-24-00002"}],
                }
            ],
        }

        update_previous_ims_action("12345", error_report)

        # Previous IMS Action updated
        self.assertEqual(
            frappe.get_value(
                "GST Inward Supply", self.invoice_name_1, "previous_ims_action"
            ),
            "Accepted",
        )

        # Previous IMS Action not updated
        self.assertEqual(
            frappe.get_value(
                "GST Inward Supply", self.invoice_name_2, "previous_ims_action"
            ),
            "Rejected",
        )

    @change_settings("GST Settings", {"enable_api": 1, "sandbox_mode": 0})
    def test_get_period_options(self):
        periods = self.get_periods()

        # When there are no GSTR 3B return logs
        period_options = get_period_options(
            "_Test Indian Registered Company", "24AAQCA8719H1ZC"
        )
        self.assertListEqual(period_options, periods[:6])

        # When GSTR 3B filed period is more than 6 months
        self.create_gstr_3b_return_log(periods[-1])
        period_options = get_period_options(
            "_Test Indian Registered Company", "24AAQCA8719H1ZC"
        )
        self.assertListEqual(period_options, periods[:-1])

        # When GSTR 3B filed period is less than 6 months
        self.create_gstr_3b_return_log(periods[2])
        period_options = get_period_options(
            "_Test Indian Registered Company", "24AAQCA8719H1ZC"
        )
        self.assertListEqual(period_options, periods[:2])

    def test_auto_reconciliation(self):
        invoice_data = self.gst_ims.autoreconcile_and_get_data().get("invoice_data")

        for data in invoice_data:
            if data._inward_supply.bill_no == "BILL-24-00001":
                self.assertEqual(data._purchase_invoice.name, self.pinv.name)

    def get_periods(self):
        periods = []
        date = add_to_date(None, months=-1)

        for _ in range(10):
            period = date.strftime("%m%Y")

            periods.append(period)
            date = add_to_date(date, months=-1)

        return periods

    def create_gstr_3b_return_log(self, period):
        gstr3b_log = frappe.new_doc("GST Return Log")
        gstr3b_log.return_period = period
        gstr3b_log.company = "_Test Indian Registered Company"
        gstr3b_log.gstin = "24AAQCA8719H1ZC"
        gstr3b_log.return_type = "GSTR3B"
        gstr3b_log.filing_status = "Filed"
        gstr3b_log.insert()
