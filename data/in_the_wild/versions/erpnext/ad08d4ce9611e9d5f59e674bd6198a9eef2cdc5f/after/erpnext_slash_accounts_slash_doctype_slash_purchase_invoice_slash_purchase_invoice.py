# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, erpnext
from frappe.utils import cint, cstr, formatdate, flt, getdate, nowdate
from frappe import _, throw
import frappe.defaults

from erpnext.controllers.buying_controller import BuyingController
from erpnext.accounts.party import get_party_account, get_due_date, get_patry_tax_withholding_details
from erpnext.accounts.utils import get_account_currency, get_fiscal_year
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import update_billed_amount_based_on_po
from erpnext.stock import get_warehouse_account_map
from erpnext.accounts.general_ledger import make_gl_entries, merge_similar_entries, delete_gl_entries
from erpnext.accounts.doctype.gl_entry.gl_entry import update_outstanding_amt
from erpnext.buying.utils import check_for_closed_status
from erpnext.accounts.general_ledger import get_round_off_account_and_cost_center
from frappe.model.mapper import get_mapped_doc
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_invoice,\
	unlink_inter_company_invoice
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class PurchaseInvoice(BuyingController):
	def __init__(self, *args, **kwargs):
		super(PurchaseInvoice, self).__init__(*args, **kwargs)
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

	def before_save(self):
		if not self.on_hold:
			self.release_date = ''

	def invoice_is_blocked(self):
		return self.on_hold and (not self.release_date or self.release_date > getdate(nowdate()))

	def validate(self):
		if not self.is_opening:
			self.is_opening = 'No'

		self.validate_posting_time()
		self.set_tax_withholding()
		super(PurchaseInvoice, self).validate()

		if not self.is_return:
			self.po_required()
			self.pr_required()
			self.validate_supplier_invoice()

		# validate cash purchase
		if (self.is_paid == 1):
			self.validate_cash()

		if self._action=="submit" and self.update_stock:
			self.make_batches('warehouse')

		self.validate_release_date()
		self.check_conversion_rate()
		self.validate_credit_to_acc()
		self.clear_unallocated_advances("Purchase Invoice Advance", "advances")
		self.check_for_closed_status()
		self.validate_with_previous_doc()
		self.validate_uom_is_integer("uom", "qty")
		self.validate_uom_is_integer("stock_uom", "stock_qty")
		self.set_expense_account(for_validate=True)
		self.set_against_expense_account()
		self.validate_write_off_account()
		self.validate_multiple_billing("Purchase Receipt", "pr_detail", "amount", "items")
		self.validate_fixed_asset()
		self.validate_fixed_asset_account()
		self.create_remarks()
		self.set_status()
		validate_inter_company_party(self.doctype, self.supplier, self.company, self.inter_company_invoice_reference)

	def validate_release_date(self):
		if self.release_date and getdate(nowdate()) >= getdate(self.release_date):
			frappe.msgprint('Release date must be in the future', raise_exception=True)

	def validate_cash(self):
		if not self.cash_bank_account and flt(self.paid_amount):
			frappe.throw(_("Cash or Bank Account is mandatory for making payment entry"))

		if (flt(self.paid_amount) + flt(self.write_off_amount)
			- flt(self.get("rounded_total") or self.grand_total)
			> 1/(10**(self.precision("base_grand_total") + 1))):

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
			self.due_date = get_due_date(self.posting_date, "Supplier", self.supplier, self.company,  self.bill_date)

		super(PurchaseInvoice, self).set_missing_values(for_validate)

	def check_conversion_rate(self):
		default_currency = erpnext.get_company_currency(self.company)
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

		for d in self.get('items'):
			if d.purchase_order and not d.purchase_order in check_list and not d.purchase_receipt:
				check_list.append(d.purchase_order)
				check_for_closed_status('Purchase Order', d.purchase_order)

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

	def validate_warehouse(self):
		if self.update_stock:
			for d in self.get('items'):
				if not d.warehouse:
					frappe.throw(_("Warehouse required at Row No {0}").format(d.idx))

		super(PurchaseInvoice, self).validate_warehouse()

	def validate_item_code(self):
		for d in self.get('items'):
			if not d.item_code:
				frappe.msgprint(_("Item Code required at Row No {0}").format(d.idx), raise_exception=True)

	def set_expense_account(self, for_validate=False):
		auto_accounting_for_stock = erpnext.is_perpetual_inventory_enabled(self.company)

		if auto_accounting_for_stock:
			stock_not_billed_account = self.get_company_default("stock_received_but_not_billed")
			stock_items = self.get_stock_items()

		if self.update_stock:
			self.validate_item_code()
			self.validate_warehouse()
			warehouse_account = get_warehouse_account_map()

		for item in self.get("items"):
			# in case of auto inventory accounting,
			# expense account is always "Stock Received But Not Billed" for a stock item
			# except epening entry, drop-ship entry and fixed asset items

			if auto_accounting_for_stock and item.item_code in stock_items \
				and self.is_opening == 'No' and not item.is_fixed_asset \
				and (not item.po_detail or
					not frappe.db.get_value("Purchase Order Item", item.po_detail, "delivered_by_supplier")):

				if self.update_stock:
					item.expense_account = warehouse_account[item.warehouse]["account"]
				else:
					item.expense_account = stock_not_billed_account

			elif not item.expense_account and for_validate:
				throw(_("Expense account is mandatory for item {0}").format(item.item_code or item.item_name))

	def set_against_expense_account(self):
		against_accounts = []
		for item in self.get("items"):
			if item.expense_account not in against_accounts:
				against_accounts.append(item.expense_account)

		self.against_expense_account = ",".join(against_accounts)

	def po_required(self):
		if frappe.db.get_value("Buying Settings", None, "po_required") == 'Yes':
			for d in self.get('items'):
				if not d.purchase_order:
					throw(_("As per the Buying Settings if Purchase Order Required == 'YES', then for creating Purchase Invoice, user need to create Purchase Order first for item {0}").format(d.item_code))

	def pr_required(self):
		stock_items = self.get_stock_items()
		if frappe.db.get_value("Buying Settings", None, "pr_required") == 'Yes':
			for d in self.get('items'):
				if not d.purchase_receipt and d.item_code in stock_items:
					throw(_("As per the Buying Settings if Purchase Reciept Required == 'YES', then for creating Purchase Invoice, user need to create Purchase Receipt first for item {0}").format(d.item_code))

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

	def validate_purchase_receipt_if_update_stock(self):
		if self.update_stock:
			for item in self.get("items"):
				if item.purchase_receipt:
					frappe.throw(_("Stock cannot be updated against Purchase Receipt {0}")
						.format(item.purchase_receipt))

	def on_submit(self):
		super(PurchaseInvoice, self).on_submit()

		self.check_prev_docstatus()
		self.update_status_updater_args()

		frappe.get_doc('Authorization Control').validate_approving_authority(self.doctype,
			self.company, self.base_grand_total)

		if not self.is_return:
			self.update_against_document_in_jv()
			self.update_prevdoc_status()
			self.update_billing_status_for_zero_amount_refdoc("Purchase Order")
			self.update_billing_status_in_pr()

		# Updating stock ledger should always be called after updating prevdoc status,
		# because updating ordered qty in bin depends upon updated ordered qty in PO
		if self.update_stock == 1:
			self.update_stock_ledger()
			from erpnext.stock.doctype.serial_no.serial_no import update_serial_nos_after_submit
			update_serial_nos_after_submit(self, "items")

		# this sequence because outstanding may get -negative
		self.make_gl_entries()

		self.update_project()
		update_linked_invoice(self.doctype, self.name, self.inter_company_invoice_reference)

	def make_gl_entries(self, gl_entries=None, repost_future_gle=True, from_repost=False):
		if not self.grand_total:
			return
		if not gl_entries:
			gl_entries = self.get_gl_entries()

		if gl_entries:
			update_outstanding = "No" if (cint(self.is_paid) or self.write_off_account) else "Yes"

			make_gl_entries(gl_entries,  cancel=(self.docstatus == 2),
				update_outstanding=update_outstanding, merge_entries=False)

			if update_outstanding == "No":
				update_outstanding_amt(self.credit_to, "Supplier", self.supplier,
					self.doctype, self.return_against if cint(self.is_return) else self.name)

			if repost_future_gle and cint(self.update_stock) and self.auto_accounting_for_stock:
				from erpnext.controllers.stock_controller import update_gl_entries_after
				items, warehouses = self.get_items_and_warehouses()
				update_gl_entries_after(self.posting_date, self.posting_time, warehouses, items)

		elif self.docstatus == 2 and cint(self.update_stock) and self.auto_accounting_for_stock:
			delete_gl_entries(voucher_type=self.doctype, voucher_no=self.name)

	def get_gl_entries(self, warehouse_account=None):
		self.auto_accounting_for_stock = erpnext.is_perpetual_inventory_enabled(self.company)
		self.stock_received_but_not_billed = self.get_company_default("stock_received_but_not_billed")
		self.expenses_included_in_valuation = self.get_company_default("expenses_included_in_valuation")
		self.negative_expense_to_be_booked = 0.0
		gl_entries = []

		self.make_supplier_gl_entry(gl_entries)
		self.make_item_gl_entries(gl_entries)
		self.make_tax_gl_entries(gl_entries)

		gl_entries = merge_similar_entries(gl_entries)

		self.make_payment_gl_entries(gl_entries)
		self.make_write_off_gl_entry(gl_entries)
		self.make_gle_for_rounding_adjustment(gl_entries)

		return gl_entries

	def make_supplier_gl_entry(self, gl_entries):
		grand_total = self.rounded_total or self.grand_total
		if grand_total:
			# Didnot use base_grand_total to book rounding loss gle
			grand_total_in_company_currency = flt(grand_total * self.conversion_rate,
				self.precision("grand_total"))
			gl_entries.append(
				self.get_gl_dict({
					"account": self.credit_to,
					"party_type": "Supplier",
					"party": self.supplier,
					"against": self.against_expense_account,
					"credit": grand_total_in_company_currency,
					"credit_in_account_currency": grand_total_in_company_currency \
						if self.party_account_currency==self.company_currency else grand_total,
					"against_voucher": self.return_against if cint(self.is_return) else self.name,
					"against_voucher_type": self.doctype,
				}, self.party_account_currency)
			)

	def make_item_gl_entries(self, gl_entries):
		# item gl entries
		stock_items = self.get_stock_items()
		expenses_included_in_valuation = self.get_company_default("expenses_included_in_valuation")
		warehouse_account = get_warehouse_account_map()

		for item in self.get("items"):
			if flt(item.base_net_amount):
				account_currency = get_account_currency(item.expense_account)

				if self.update_stock and self.auto_accounting_for_stock and item.item_code in stock_items:
					val_rate_db_precision = 6 if cint(item.precision("valuation_rate")) <= 6 else 9

					# warehouse account
					warehouse_debit_amount = flt(flt(item.valuation_rate, val_rate_db_precision)
						* flt(item.qty)	* flt(item.conversion_factor), item.precision("base_net_amount"))

					gl_entries.append(
						self.get_gl_dict({
							"account": item.expense_account,
							"against": self.supplier,
							"debit": warehouse_debit_amount,
							"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
							"cost_center": item.cost_center,
							"project": item.project
						}, account_currency)
					)

					# Amount added through landed-cost-voucher
					if flt(item.landed_cost_voucher_amount):
						gl_entries.append(self.get_gl_dict({
							"account": expenses_included_in_valuation,
							"against": item.expense_account,
							"cost_center": item.cost_center,
							"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
							"credit": flt(item.landed_cost_voucher_amount),
							"project": item.project
						}))

					# sub-contracting warehouse
					if flt(item.rm_supp_cost):
						supplier_warehouse_account = warehouse_account[self.supplier_warehouse]["account"]
						if not supplier_warehouse_account:
							frappe.throw(_("Please set account in Warehouse {0}")
								.format(self.supplier_warehouse))
						gl_entries.append(self.get_gl_dict({
							"account": supplier_warehouse_account,
							"against": item.expense_account,
							"cost_center": item.cost_center,
							"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
							"credit": flt(item.rm_supp_cost)
						}, warehouse_account[self.supplier_warehouse]["account_currency"]))

				elif item.is_fixed_asset:
					asset_accounts = self.get_company_default(["asset_received_but_not_billed",
						"expenses_included_in_asset_valuation", "capital_work_in_progress_account"])

					asset_amount = flt(item.net_amount) + flt(item.item_tax_amount/self.conversion_rate)
					base_asset_amount = flt(item.base_net_amount + item.item_tax_amount)

					if not self.update_stock:
						asset_rbnb_currency = get_account_currency(asset_accounts[0])
						gl_entries.append(self.get_gl_dict({
							"account": asset_accounts[0],
							"against": self.supplier,
							"remarks": self.get("remarks") or _("Accounting Entry for Asset"),
							"debit": base_asset_amount,
							"debit_in_account_currency": (base_asset_amount
								if asset_rbnb_currency == self.company_currency else asset_amount)
						}))
					else:
						cwip_account = get_asset_category_account(item.asset,
							'capital_work_in_progress_account') or asset_accounts[2]

						cwip_account_currency = get_account_currency(cwip_account)
						gl_entries.append(self.get_gl_dict({
							"account": cwip_account,
							"against": self.supplier,
							"remarks": self.get("remarks") or _("Accounting Entry for Asset"),
							"debit": base_asset_amount,
							"debit_in_account_currency": (base_asset_amount
								if cwip_account_currency == self.company_currency else asset_amount)
						}))

					if item.item_tax_amount:
						asset_eiiav_currency = get_account_currency(asset_accounts[0])
						gl_entries.append(self.get_gl_dict({
							"account": asset_accounts[1],
							"against": self.supplier,
							"remarks": self.get("remarks") or _("Accounting Entry for Asset"),
							"cost_center": item.cost_center,
							"credit": item.item_tax_amount,
							"credit_in_account_currency": (item.item_tax_amount
								if asset_eiiav_currency == self.company_currency else
									item.item_tax_amount / self.conversion_rate)
						}))
				else:
					gl_entries.append(
						self.get_gl_dict({
							"account": item.expense_account,
							"against": self.supplier,
							"debit": flt(item.base_net_amount, item.precision("base_net_amount")),
							"debit_in_account_currency": (flt(item.base_net_amount,
								item.precision("base_net_amount")) if account_currency==self.company_currency
								else flt(item.net_amount, item.precision("net_amount"))),
							"cost_center": item.cost_center,
							"project": item.project
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
									"debit": flt(item.item_tax_amount, item.precision("item_tax_amount")),
									"remarks": self.remarks or "Accounting Entry for Stock"
								})
							)

							self.negative_expense_to_be_booked += flt(item.item_tax_amount, \
								item.precision("item_tax_amount"))

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

		if self.auto_accounting_for_stock and self.update_stock and valuation_tax:
			for cost_center, amount in valuation_tax.items():
				gl_entries.append(
					self.get_gl_dict({
						"account": self.expenses_included_in_valuation,
						"cost_center": cost_center,
						"against": self.supplier,
						"credit": amount,
						"remarks": self.remarks or "Accounting Entry for Stock"
					})
				)

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

	def make_gle_for_rounding_adjustment(self, gl_entries):
		if self.rounding_adjustment:
			round_off_account, round_off_cost_center = \
				get_round_off_account_and_cost_center(self.company)

			gl_entries.append(
				self.get_gl_dict({
					"account": round_off_account,
					"against": self.supplier,
					"debit_in_account_currency": self.rounding_adjustment,
					"debit": self.base_rounding_adjustment,
					"cost_center": round_off_cost_center,
				}
			))

	def on_cancel(self):
		super(PurchaseInvoice, self).on_cancel()

		self.check_for_closed_status()

		self.update_status_updater_args()

		if not self.is_return:
			from erpnext.accounts.utils import unlink_ref_doc_from_payment_entries
			if frappe.db.get_single_value('Accounts Settings', 'unlink_payment_on_cancellation_of_invoice'):
				unlink_ref_doc_from_payment_entries(self)

			self.update_prevdoc_status()
			self.update_billing_status_for_zero_amount_refdoc("Purchase Order")
			self.update_billing_status_in_pr()

		# Updating stock ledger should always be called after updating prevdoc status,
		# because updating ordered qty in bin depends upon updated ordered qty in PO
		if self.update_stock == 1:
			self.update_stock_ledger()

		self.make_gl_entries_on_cancel()
		self.update_project()
		frappe.db.set(self, 'status', 'Cancelled')

		unlink_inter_company_invoice(self.doctype, self.name, self.inter_company_invoice_reference)

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
						and supplier = %(supplier)s
						and name != %(name)s
						and docstatus < 2
						and posting_date between %(year_start_date)s and %(year_end_date)s''', {
							"bill_no": self.bill_no,
							"supplier": self.supplier,
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
			if d.is_fixed_asset:
				account_type = frappe.db.get_value("Account", d.expense_account, "account_type")
				if account_type != 'Fixed Asset':
					frappe.throw(_("Row {0}# Account must be of type 'Fixed Asset'").format(d.idx))

	def on_recurring(self, reference_doc, auto_repeat_doc):
		self.due_date = None

	def block_invoice(self, hold_comment=None):
		self.db_set('on_hold', 1)
		self.db_set('hold_comment', cstr(hold_comment))

	def unblock_invoice(self):
		self.db_set('on_hold', 0)
		self.db_set('release_date', None)

  def set_tax_withholding(self):
		"""
			1. Get TDS Configurations against Supplier
		"""

		tax_withholding_details = get_patry_tax_withholding_details(self)
		for tax_details in tax_withholding_details:
			if flt(self.get("rounded_total") or self.grand_total) >= flt(tax_details['threshold']):
				if self.taxes:
					if tax_details['tax']['description'] not in [tax.description for tax in self.taxes]:
						self.append('taxes', tax_details['tax'])
				else:
					self.append('taxes', tax_details['tax'])

@frappe.whitelist()
def make_debit_note(source_name, target_doc=None):
	from erpnext.controllers.sales_and_purchase_return import make_return_doc
	return make_return_doc("Purchase Invoice", source_name, target_doc)

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	doc = get_mapped_doc("Purchase Invoice", source_name, {
		"Purchase Invoice": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Purchase Invoice Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"stock_qty": "transfer_qty"
			},
		}
	}, target_doc)

	return doc

@frappe.whitelist()
def change_release_date(name, release_date=None):
	if frappe.db.exists('Purchase Invoice', name):
		pi = frappe.get_doc('Purchase Invoice', name)
		pi.db_set('release_date', release_date)


@frappe.whitelist()
def unblock_invoice(name):
	if frappe.db.exists('Purchase Invoice', name):
		pi = frappe.get_doc('Purchase Invoice', name)
		pi.unblock_invoice()


@frappe.whitelist()
def block_invoice(name, hold_comment):
	if frappe.db.exists('Purchase Invoice', name):
		pi = frappe.get_doc('Purchase Invoice', name)
		pi.block_invoice(hold_comment)

@frappe.whitelist()
def make_inter_company_sales_invoice(source_name, target_doc=None):
	from erpnext.accounts.doctype.sales_invoice.sales_invoice import make_inter_company_invoice
	return make_inter_company_invoice("Purchase Invoice", source_name, target_doc)

