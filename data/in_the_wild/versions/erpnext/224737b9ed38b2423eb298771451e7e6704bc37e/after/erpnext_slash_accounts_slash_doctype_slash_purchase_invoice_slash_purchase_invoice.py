# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, formatdate, flt, getdate
from frappe import msgprint, _, throw
from erpnext.setup.utils import get_company_currency
import frappe.defaults

from erpnext.controllers.buying_controller import BuyingController
from erpnext.accounts.party import get_party_account, get_due_date
from erpnext.accounts.utils import get_account_currency, get_fiscal_year
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import update_billed_amount_based_on_po
from erpnext.controllers.stock_controller import get_warehouse_account


form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class PurchaseInvoice(BuyingController):
	def __init__(self, arg1, arg2=None):
		super(PurchaseInvoice, self).__init__(arg1, arg2)
		self.status_updater = [{
			'source_dt': 'Purchase Invoice Item',
			'target_dt': 'Purchase Order Item',
			'join_field': 'po_detail',
			'target_field': 'billed_amt',
			'target_parent_dt': 'Purchase Order',
			'target_parent_field': 'per_billed',
			'target_ref_field': 'amount',
			'source_field': 'amount',
			'percent_join_field': 'purchase_order',
			'overflow_type': 'billing'
		}]

	def validate(self):
		if not self.is_opening:
			self.is_opening = 'No'

		super(PurchaseInvoice, self).validate()

		if not self.is_return:
			self.po_required()
			self.pr_required()
			self.validate_supplier_invoice()
			self.validate_advance_jv("Purchase Order")

		# validate cash purchase
		if (self.is_paid == 1):
			self.validate_cash()

		self.check_active_purchase_items()
		self.check_conversion_rate()
		self.validate_credit_to_acc()
		self.clear_unallocated_advances("Purchase Invoice Advance", "advances")
		self.check_for_closed_status()
		self.validate_with_previous_doc()
		self.validate_uom_is_integer("uom", "qty")
		self.set_against_expense_account()
		self.validate_write_off_account()
		self.update_valuation_rate("items")
		self.validate_multiple_billing("Purchase Receipt", "pr_detail", "amount", "items")
		self.validate_fixed_asset_account()
		self.create_remarks()

	def validate_cash(self):
		if not self.cash_bank_account and flt(self.paid_amount):
			frappe.throw(_("Cash or Bank Account is mandatory for making payment entry"))

		if flt(self.paid_amount) + flt(self.write_off_amount) \
				- flt(self.base_grand_total) > 1/(10**(self.precision("base_grand_total") + 1)):
			frappe.throw(_("""Paid amount + Write Off Amount can not be greater than Grand Total"""))

	def create_remarks(self):
		if not self.remarks:
			if self.bill_no and self.bill_date:
				self.remarks = _("Against Supplier Invoice {0} dated {1}").format(self.bill_no, 
					formatdate(self.bill_date))
			else:
				self.remarks = _("No Remarks")

	def set_missing_values(self, for_validate=False):
		if not self.credit_to:
			self.credit_to = get_party_account("Supplier", self.supplier, self.company)
		if not self.due_date:
			self.due_date = get_due_date(self.posting_date, "Supplier", self.supplier, self.company)

		super(PurchaseInvoice, self).set_missing_values(for_validate)

	def get_advances(self):
		if not self.is_return:
			super(PurchaseInvoice, self).get_advances(self.credit_to, "Supplier", self.supplier,
				"Purchase Invoice Advance", "advances", "debit_in_account_currency", "purchase_order")

	def check_conversion_rate(self):
		default_currency = get_company_currency(self.company)
		if not default_currency:
			throw(_('Please enter default currency in Company Master'))
		if (self.currency == default_currency and flt(self.conversion_rate) != 1.00) or not self.conversion_rate or (self.currency != default_currency and flt(self.conversion_rate) == 1.00):
			throw(_("Conversion rate cannot be 0 or 1"))

	def validate_credit_to_acc(self):
		account = frappe.db.get_value("Account", self.credit_to,
			["account_type", "report_type", "account_currency"], as_dict=True)

		if account.report_type != "Balance Sheet":
			frappe.throw(_("Credit To account must be a Balance Sheet account"))

		if self.supplier and account.account_type != "Payable":
			frappe.throw(_("Credit To account must be a Payable account"))

		self.party_account_currency = account.account_currency

	def check_for_closed_status(self):
		check_list = []
		pc_obj = frappe.get_doc('Purchase Common')

		for d in self.get('items'):
			if d.purchase_order and not d.purchase_order in check_list and not d.purchase_receipt:
				check_list.append(d.purchase_order)
				pc_obj.check_for_closed_status('Purchase Order', d.purchase_order)

	def validate_with_previous_doc(self):
		super(PurchaseInvoice, self).validate_with_previous_doc({
			"Purchase Order": {
				"ref_dn_field": "purchase_order",
				"compare_fields": [["supplier", "="], ["company", "="], ["currency", "="]],
			},
			"Purchase Order Item": {
				"ref_dn_field": "po_detail",
				"compare_fields": [["project", "="], ["item_code", "="], ["uom", "="]],
				"is_child_table": True,
				"allow_duplicate_prev_row_id": True
			},
			"Purchase Receipt": {
				"ref_dn_field": "purchase_receipt",
				"compare_fields": [["supplier", "="], ["company", "="], ["currency", "="]],
			},
			"Purchase Receipt Item": {
				"ref_dn_field": "pr_detail",
				"compare_fields": [["project", "="], ["item_code", "="], ["uom", "="]],
				"is_child_table": True
			}
		})

		if cint(frappe.db.get_single_value('Buying Settings', 'maintain_same_rate')) and not self.is_return:
			self.validate_rate_with_reference_doc([
				["Purchase Order", "purchase_order", "po_detail"],
				["Purchase Receipt", "purchase_receipt", "pr_detail"]
			])

	def set_against_expense_account(self):
		auto_accounting_for_stock = cint(frappe.defaults.get_global_default("auto_accounting_for_stock"))

		if auto_accounting_for_stock:
			stock_not_billed_account = self.get_company_default("stock_received_but_not_billed")

		against_accounts = []
		stock_items = self.get_stock_items()
		for item in self.get("items"):
			# in case of auto inventory accounting,
			# expense account is always "Stock Received But Not Billed" for a stock item 
			# except epening entry, drop-ship entry and fixed asset items

			if auto_accounting_for_stock and item.item_code in stock_items and self.is_opening == 'No' \
				and (not item.po_detail 
					or not frappe.db.get_value("Purchase Order Item", item.po_detail, "delivered_by_supplier")
					or not frappe.db.get_value("Item", item.item_code, "is_fixed_asset")):

				item.expense_account = stock_not_billed_account
				item.cost_center = None

				if stock_not_billed_account not in against_accounts:
					against_accounts.append(stock_not_billed_account)

			elif not item.expense_account:
				throw(_("Expense account is mandatory for item {0}").format(item.item_code or item.item_name))

			elif item.expense_account not in against_accounts:
				# if no auto_accounting_for_stock or not a stock item
				against_accounts.append(item.expense_account)

		self.against_expense_account = ",".join(against_accounts)

	def po_required(self):
		if frappe.db.get_value("Buying Settings", None, "po_required") == 'Yes':
			 for d in self.get('items'):
				 if not d.purchase_order:
					 throw(_("Purchse Order number required for Item {0}").format(d.item_code))

	def pr_required(self):
		stock_items = self.get_stock_items()
		if frappe.db.get_value("Buying Settings", None, "pr_required") == 'Yes':
			 for d in self.get('items'):
				 if not d.purchase_receipt and d.item_code in stock_items:
					 throw(_("Purchase Receipt number required for Item {0}").format(d.item_code))

	def validate_write_off_account(self):
		if self.write_off_amount and not self.write_off_account:
			throw(_("Please enter Write Off Account"))

	def check_prev_docstatus(self):
		for d in self.get('items'):
			if d.purchase_order:
				submitted = frappe.db.sql("select name from `tabPurchase Order` where docstatus = 1 and name = %s", d.purchase_order)
				if not submitted:
					frappe.throw(_("Purchase Order {0} is not submitted").format(d.purchase_order))
			if d.purchase_receipt:
				submitted = frappe.db.sql("select name from `tabPurchase Receipt` where docstatus = 1 and name = %s", d.purchase_receipt)
				if not submitted:
					frappe.throw(_("Purchase Receipt {0} is not submitted").format(d.purchase_receipt))


	def update_against_document_in_jv(self):
		"""
			Links invoice and advance voucher:
				1. cancel advance voucher
				2. split into multiple rows if partially adjusted, assign against voucher
				3. submit advance voucher
		"""

		lst = []
		for d in self.get('advances'):
			if flt(d.allocated_amount) > 0:
				args = {
					'voucher_no' : d.journal_entry,
					'voucher_detail_no' : d.jv_detail_no,
					'against_voucher_type' : 'Purchase Invoice',
					'against_voucher'  : self.name,
					'account' : self.credit_to,
					'party_type': 'Supplier',
					'party': self.supplier,
					'is_advance' : 'Yes',
					'dr_or_cr' : 'debit_in_account_currency',
					'unadjusted_amt' : flt(d.advance_amount),
					'allocated_amt' : flt(d.allocated_amount)
				}
				lst.append(args)

		if lst:
			from erpnext.accounts.utils import reconcile_against_document
			reconcile_against_document(lst)

	def update_status_updater_args(self):
		if cint(self.update_stock):
			self.status_updater.extend([{
				'source_dt': 'Purchase Invoice Item',
				'target_dt': 'Purchase Order Item',
				'join_field': 'po_detail',
				'target_field': 'received_qty',
				'target_parent_dt': 'Purchase Order',
				'target_parent_field': 'per_received',
				'target_ref_field': 'qty',
				'source_field': 'qty',
				'percent_join_field':'purchase_order',
				# 'percent_join_field': 'prevdoc_docname',
				'overflow_type': 'receipt',
				'extra_cond': """ and exists(select name from `tabPurchase Invoice`
					where name=`tabPurchase Invoice Item`.parent and update_stock = 1)"""
			},
			{
				'source_dt': 'Purchase Invoice Item',
				'target_dt': 'Purchase Order Item',
				'join_field': 'po_detail',
				'target_field': 'returned_qty',
				'target_parent_dt': 'Purchase Order',
				# 'target_parent_field': 'per_received',
				# 'target_ref_field': 'qty',
				'source_field': '-1 * qty',
				# 'percent_join_field': 'prevdoc_docname',
				# 'overflow_type': 'receipt',
				'extra_cond': """ and exists (select name from `tabPurchase Invoice`
					where name=`tabPurchase Invoice Item`.parent and update_stock=1 and is_return=1)"""
			}
		])
	
	def validate_purchase_receipt(self):
		for item in self.get("items"):
			if item.purchase_receipt:
				frappe.throw(_("Stock cannot be updated against Purchase Receipt {0}").format(item.purchase_receipt))

	def on_submit(self):
		self.check_prev_docstatus()
		self.validate_asset()

		frappe.get_doc('Authorization Control').validate_approving_authority(self.doctype,
			self.company, self.base_grand_total)

		if (self.update_stock == 1):
			# from erpnext.stock.doctype.purchase_receipt.purchase_receipt import update_stock_ledger
			self.update_stock_ledger()
			from erpnext.stock.doctype.serial_no.serial_no import update_serial_nos_after_submit
			update_serial_nos_after_submit(self, "items")
			self.update_status_updater_args()
			self.update_prevdoc_status()

		# this sequence because outstanding may get -negative
		self.make_gl_entries()
		
		if not self.is_return:
			self.update_against_document_in_jv()
			self.update_prevdoc_status()
			self.update_billing_status_for_zero_amount_refdoc("Purchase Order")
			self.update_billing_status_in_pr()

		self.update_project()
		
	def validate_asset(self):
		for d in self.get("items"):
			if frappe.db.get_value("Item", d.item_code, "is_fixed_asset"):
				if not d.asset:
					frappe.throw(_("Row #{0}: Asset is mandatory against a Fixed Asset Item").format(d.idx))
				else:
					asset = frappe.get_doc("Asset", d.asset)
					
					super(PurchaseInvoice, self).validate_asset(asset, d)
		
					if getdate(asset.purchase_date) != getdate(self.posting_date):
						frappe.throw(_("Purchase Date of asset {0} does not match with Purchase Invoice date")
							.format(d.asset))
					
					if asset.supplier and asset.supplier != self.supplier:
						frappe.throw(_("Supplier of asset {0} does not match with the supplier in the Purchase Invoice").format(d.asset))
				
					if asset.status != "Submitted":
						frappe.throw(_("Row #{0}: Asset {1} is already {2}")
							.format(d.idx, d.asset, asset.status))
					
					frappe.db.set_value("Asset", asset.name, "purchase_invoice", 
						(self.name if self.docstatus==1 else None))
						
					if self.docstatus==1 and not asset.supplier:
						frappe.db.set_value("Asset", asset.name, "supplier", self.supplier)

	def make_gl_entries(self):
		self.auto_accounting_for_stock = \
			cint(frappe.defaults.get_global_default("auto_accounting_for_stock"))

		self.stock_received_but_not_billed = self.get_company_default("stock_received_but_not_billed")
		self.expenses_included_in_valuation = self.get_company_default("expenses_included_in_valuation")
		self.negative_expense_to_be_booked = 0.0
		gl_entries = []
		
		
		self.make_supplier_gl_entry(gl_entries)
		self.make_item_gl_entries(gl_entries)
		self.make_tax_gl_entries(gl_entries)
		
		from erpnext.accounts.general_ledger import merge_similar_entries
		gl_entries = merge_similar_entries(gl_entries)
		
		self.make_payment_gl_entries(gl_entries)

		self.make_write_off_gl_entry(gl_entries)
		if gl_entries:
			from erpnext.accounts.general_ledger import make_gl_entries
			update_outstanding = "No" if (cint(self.is_paid) or self.write_off_account) else "Yes"
			
			make_gl_entries(gl_entries,  cancel=(self.docstatus == 2),
				update_outstanding=update_outstanding, merge_entries=False)

	def make_supplier_gl_entry(self, gl_entries):
		# parent's gl entry
		if self.grand_total:
			# Didnot use base_grand_total to book rounding loss gle
			grand_total_in_company_currency = flt(self.grand_total * self.conversion_rate,
				self.precision("grand_total"))
			gl_entries.append(
				self.get_gl_dict({
					"account": self.credit_to,
					"party_type": "Supplier",
					"party": self.supplier,
					"against": self.against_expense_account,
					"credit": grand_total_in_company_currency,
					"credit_in_account_currency": grand_total_in_company_currency \
						if self.party_account_currency==self.company_currency else self.grand_total,
					"against_voucher": self.return_against if cint(self.is_return) else self.name,
					"against_voucher_type": self.doctype,
				}, self.party_account_currency)
			)

	def make_item_gl_entries(self, gl_entries):
		# item gl entries
		stock_items = self.get_stock_items()
		warehouse_account = get_warehouse_account()

		for item in self.get("items"):
			if flt(item.base_net_amount):
				account_currency = get_account_currency(item.expense_account)
				
				if self.auto_accounting_for_stock and self.update_stock:
					expense_account = warehouse_account[item.warehouse]["name"]
				else:
					expense_account = item.expense_account
				
				gl_entries.append(
					self.get_gl_dict({
						"account": expense_account,
						"against": self.supplier,
						"debit": item.base_net_amount,
						"debit_in_account_currency": item.base_net_amount \
							if account_currency==self.company_currency else item.net_amount,
						"cost_center": item.cost_center
					}, account_currency)
				)
				
			if self.auto_accounting_for_stock and self.is_opening == "No" and \
				item.item_code in stock_items and item.item_tax_amount:
					# Post reverse entry for Stock-Received-But-Not-Billed if it is booked in Purchase Receipt
					if item.purchase_receipt:
						negative_expense_booked_in_pr = frappe.db.sql("""select name from `tabGL Entry`
							where voucher_type='Purchase Receipt' and voucher_no=%s and account=%s""",
							(item.purchase_receipt, self.expenses_included_in_valuation))

						if not negative_expense_booked_in_pr:
							gl_entries.append(
								self.get_gl_dict({
									"account": self.stock_received_but_not_billed,
									"against": self.supplier,
									"debit": flt(item.item_tax_amount, self.precision("item_tax_amount", item)),
									"remarks": self.remarks or "Accounting Entry for Stock"
								})
							)

							self.negative_expense_to_be_booked += flt(item.item_tax_amount, \
								self.precision("item_tax_amount", item))

	def make_tax_gl_entries(self, gl_entries):
		# tax table gl entries
		valuation_tax = {}
		for tax in self.get("taxes"):
			if tax.category in ("Total", "Valuation and Total") and flt(tax.base_tax_amount_after_discount_amount):
				account_currency = get_account_currency(tax.account_head)

				dr_or_cr = "debit" if tax.add_deduct_tax == "Add" else "credit"

				gl_entries.append(
					self.get_gl_dict({
						"account": tax.account_head,
						"against": self.supplier,
						dr_or_cr: tax.base_tax_amount_after_discount_amount,
						dr_or_cr + "_in_account_currency": tax.base_tax_amount_after_discount_amount \
							if account_currency==self.company_currency \
							else tax.tax_amount_after_discount_amount,
						"cost_center": tax.cost_center
					}, account_currency)
				)
			# accumulate valuation tax
			if self.is_opening == "No" and tax.category in ("Valuation", "Valuation and Total") and flt(tax.base_tax_amount_after_discount_amount):
				if self.auto_accounting_for_stock and not tax.cost_center:
					frappe.throw(_("Cost Center is required in row {0} in Taxes table for type {1}").format(tax.idx, _(tax.category)))
				valuation_tax.setdefault(tax.cost_center, 0)
				valuation_tax[tax.cost_center] += \
					(tax.add_deduct_tax == "Add" and 1 or -1) * flt(tax.base_tax_amount_after_discount_amount)
		
		if self.is_opening == "No" and self.negative_expense_to_be_booked and valuation_tax:
			# credit valuation tax amount in "Expenses Included In Valuation"
			# this will balance out valuation amount included in cost of goods sold

			total_valuation_amount = sum(valuation_tax.values())
			amount_including_divisional_loss = self.negative_expense_to_be_booked
			i = 1
			for cost_center, amount in valuation_tax.items():
				if i == len(valuation_tax):
					applicable_amount = amount_including_divisional_loss
				else:
					applicable_amount = self.negative_expense_to_be_booked * (amount / total_valuation_amount)
					amount_including_divisional_loss -= applicable_amount

				gl_entries.append(
					self.get_gl_dict({
						"account": self.expenses_included_in_valuation,
						"cost_center": cost_center,
						"against": self.supplier,
						"credit": applicable_amount,
						"remarks": self.remarks or "Accounting Entry for Stock"
					})
				)

				i += 1

	def make_payment_gl_entries(self, gl_entries):
		# Make Cash GL Entries
		if cint(self.is_paid) and self.cash_bank_account and self.paid_amount:
			bank_account_currency = get_account_currency(self.cash_bank_account)
			# CASH, make payment entries
			gl_entries.append(
				self.get_gl_dict({
					"account": self.credit_to,
					"party_type": "Supplier",
					"party": self.supplier,
					"against": self.cash_bank_account,
					"debit": self.base_paid_amount,
					"debit_in_account_currency": self.base_paid_amount \
						if self.party_account_currency==self.company_currency else self.paid_amount,
					"against_voucher": self.return_against if cint(self.is_return) else self.name,
					"against_voucher_type": self.doctype,
				}, self.party_account_currency)
			)
						
			gl_entries.append(
				self.get_gl_dict({
					"account": self.cash_bank_account,
					"against": self.supplier,
					"credit": self.base_paid_amount,
					"credit_in_account_currency": self.base_paid_amount \
						if bank_account_currency==self.company_currency else self.paid_amount
				}, bank_account_currency)
			)

	def make_write_off_gl_entry(self, gl_entries):
		# writeoff account includes petty difference in the invoice amount
		# and the amount that is paid
		if self.write_off_account and flt(self.write_off_amount):
			write_off_account_currency = get_account_currency(self.write_off_account)

			gl_entries.append(
				self.get_gl_dict({
					"account": self.credit_to,
					"party_type": "Supplier",
					"party": self.supplier,
					"against": self.write_off_account,
					"debit": self.base_write_off_amount,
					"debit_in_account_currency": self.base_write_off_amount \
						if self.party_account_currency==self.company_currency else self.write_off_amount,
					"against_voucher": self.return_against if cint(self.is_return) else self.name,
					"against_voucher_type": self.doctype,
				}, self.party_account_currency)
			)
			gl_entries.append(
				self.get_gl_dict({
					"account": self.write_off_account,
					"against": self.supplier,
					"credit": flt(self.base_write_off_amount),
					"credit_in_account_currency": self.base_write_off_amount \
						if write_off_account_currency==self.company_currency else self.write_off_amount,
					"cost_center": self.write_off_cost_center
				})
			)

	def on_cancel(self):
		self.check_for_closed_status()

		if not self.is_return:
			from erpnext.accounts.utils import remove_against_link_from_jv
			remove_against_link_from_jv(self.doctype, self.name)

			self.update_prevdoc_status()
			self.update_billing_status_for_zero_amount_refdoc("Purchase Order")
			self.update_billing_status_in_pr()

		self.make_gl_entries_on_cancel()
		self.update_project()
		self.validate_asset()

	def update_project(self):
		project_list = []
		for d in self.items:
			if d.project and d.project not in project_list:
				project = frappe.get_doc("Project", d.project)
				project.flags.dont_sync_tasks = True
				project.update_purchase_costing()
				project.save()
				project_list.append(d.project)

	def validate_supplier_invoice(self):
		if self.bill_date:
			if getdate(self.bill_date) > getdate(self.posting_date):
				frappe.throw(_("Supplier Invoice Date cannot be greater than Posting Date"))

		if self.bill_no:
			if cint(frappe.db.get_single_value("Accounts Settings", "check_supplier_invoice_uniqueness")):
				fiscal_year = get_fiscal_year(self.posting_date, company=self.company, as_dict=True)

				pi = frappe.db.sql('''select name from `tabPurchase Invoice`
					where
						bill_no = %(bill_no)s
						and name != %(name)s
						and docstatus < 2
						and posting_date between %(year_start_date)s and %(year_end_date)s''', {
							"bill_no": self.bill_no,
							"name": self.name,
							"year_start_date": fiscal_year.year_start_date,
							"year_end_date": fiscal_year.year_end_date
						})

				if pi:
					pi = pi[0][0]
					frappe.throw(_("Supplier Invoice No exists in Purchase Invoice {0}".format(pi)))

	def update_billing_status_in_pr(self, update_modified=True):
		updated_pr = []
		for d in self.get("items"):
			if d.pr_detail:
				billed_amt = frappe.db.sql("""select sum(amount) from `tabPurchase Invoice Item`
					where pr_detail=%s and docstatus=1""", d.pr_detail)
				billed_amt = billed_amt and billed_amt[0][0] or 0
				frappe.db.set_value("Purchase Receipt Item", d.pr_detail, "billed_amt", billed_amt, update_modified=update_modified)
				updated_pr.append(d.purchase_receipt)
			elif d.po_detail:
				updated_pr += update_billed_amount_based_on_po(d.po_detail, update_modified)

		for pr in set(updated_pr):
			frappe.get_doc("Purchase Receipt", pr).update_billing_percentage(update_modified=update_modified)
			
	def validate_fixed_asset_account(self):
		for d in self.get('items'):
			if frappe.db.get_value("Item", d.item_code, "is_fixed_asset"):
				account_type = frappe.db.get_value("Account", d.expense_account, "account_type")
				if account_type != 'Fixed Asset':
					frappe.throw(_("Row {0}# Account must be of type 'Fixed Asset'").format(d.idx))

	def on_recurring(self, reference_doc):
		self.due_date = None

@frappe.whitelist()
def make_debit_note(source_name, target_doc=None):
	from erpnext.controllers.sales_and_purchase_return import make_return_doc
	return make_return_doc("Purchase Invoice", source_name, target_doc)
