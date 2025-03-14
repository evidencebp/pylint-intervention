import webnotes
from webnotes.utils import cstr, flt, get_defaults, nowdate
from webnotes import msgprint
from webnotes.model.code import get_obj
sql = webnotes.conn.sql
	
# -----------------------------------------------------------------------------------------

class DocType:
	def __init__(self, doc, doclist=[]):
		self.doc = doc
		self.doclist = doclist
		self.validated = 1
		self.data = []

	def get_template(self):
		return [['Item Code', 'Warehouse', 'Quantity', 'Valuation Rate']]

	def get_csv_file_data(self):
		"""Get csv data"""
		filename = self.doc.file_list.split(',')
		if not filename:
			msgprint("Please Attach File. ", raise_exception=1)
			
		from webnotes.utils import file_manager
		fn, content = file_manager.get_file(filename[1])
		
		if not type(content) == str:
			content = content.tostring()

		return content

	def convert_into_list(self, data):
		"""Convert csv data into list"""
		count = 1
		for s in data:
			if s[0].strip() != 'Item Code': # remove the labels
				# validate
				if len(s) != 4:
					msgprint("Data entered at Row No " + cstr(count) + " in Attachment File is not in correct format.", raise_exception=1)
					self.validated = 0
				self.validate_item(s[0], count)
				self.validate_warehouse(s[1], count)
			
				# encode as ascii
				self.data.append([d.encode("ascii") for d in s])
				count += 1
			
		if not self.validated:
			raise Exception


	def get_reconciliation_data(self,submit = 0):
		"""Read and validate csv data"""
		import csv 
		data = csv.reader(self.get_csv_file_data().splitlines())
		self.convert_into_list(data)
		

	def validate_item(self, item, count):
		""" Validate item exists and non-serialized"""
		det = sql("select item_code, has_serial_no from `tabItem` where name = '%s'"% cstr(item), as_dict = 1)
		if not det:
			msgprint("Item: " + cstr(item) + " mentioned at Row No. " + cstr(count) + "does not exist in the system")
			self.validated = 0
		elif det and det[0]['has_serial_no'] == 'Yes':
			msgprint("""You cannot make Stock Reconciliation of items having serial no. \n
			You can directly upload serial no to update their inventory. \n
			Please remove Item Code : %s at Row No. %s""" %(cstr(item), cstr(count)))
			self.validated = 0


	def validate_warehouse(self, wh, count,):
		"""Validate warehouse exists"""
		if not sql("select name from `tabWarehouse` where name = '%s'" % cstr(wh)):
			msgprint("Warehouse: " + cstr(wh) + " mentioned at Row No. " + cstr(count) + " does not exist in the system")
			self.validated = 0



	def validate(self):
		"""Validate attachment data"""
		#self.data = [['it', 'wh1', 20, 150]]
		if self.doc.file_list:
			self.get_reconciliation_data()

			

	def get_system_stock(self, it, wh):
		"""get actual qty on reconciliation date and time as per system"""
		bin = sql("select name from tabBin where item_code=%s and warehouse=%s", (it, wh))
		prev_sle = bin and get_obj('Bin', bin[0][0]).get_sle_prev_timebucket(self.doc.reconciliation_date, self.doc.reconciliation_time) or {}
		return {
			'actual_qty': prev_sle.get('bin_aqat', 0), 
			'stock_uom' : sql("select stock_uom from tabItem where name = %s", it)[0][0], 
			'val_rate'  : prev_sle.get('valuation_rate', 0)
		}


	def make_sl_entry(self, is_submit, row, qty_diff, sys_stock):
		"""Make stock ledger entry"""
		in_rate = self.get_incoming_rate(row, qty_diff, sys_stock)	
		values = [{
				'item_code'					: row[0],
				'warehouse'					: row[1],
				'transaction_date'	 		: nowdate(),
				'posting_date'				: self.doc.reconciliation_date,
				'posting_time'			 	: self.doc.reconciliation_time,
				'voucher_type'			 	: self.doc.doctype,
				'voucher_no'				: self.doc.name,
				'voucher_detail_no'			: self.doc.name,
				'actual_qty'				: flt(is_submit) * flt(qty_diff),
				'stock_uom'					: sys_stock['stock_uom'],
				'incoming_rate'				: in_rate,
				'company'					: get_defaults()['company'],
				'fiscal_year'				: get_defaults()['fiscal_year'],
				'is_cancelled'			 	: (is_submit==1) and 'No' or 'Yes',
				'batch_no'					: '',
				'serial_no'					: ''
		 }]		
		get_obj('Stock Ledger', 'Stock Ledger').update_stock(values)
		
		
	def get_incoming_rate(self, row, qty_diff, sys_stock):
		"""Calculate incoming rate to maintain valuation rate"""
		in_rate = flt(row[3]) + (flt(sys_stock['actual_qty'])*(flt(row[3]) - flt(sys_stock['val_rate'])))/ flt(qty_diff)
		return in_rate


	def do_stock_reco(self, is_submit = 1):
		"""
			Make stock entry of qty diff, calculate incoming rate to maintain valuation rate.
			If no qty diff, but diff in valuation rate, make (+1,-1) entry to update valuation
		"""
		for row in self.data:
			# Get qty as per system
			sys_stock = self.get_system_stock(row[0],row[1])
			
			# Diff between file and system
			qty_diff = row[2] != '~' and flt(row[2]) - flt(sys_stock['actual_qty']) or 0
			rate_diff = row[3] != '~' and flt(row[3]) - flt(sys_stock['val_rate']) or 0

			# Make sl entry
			if qty_diff:
				self.make_sl_entry(is_submit, row, qty_diff, sys_stock)
			elif rate_diff:
				self.make_sl_entry(is_submit, row, 1, sys_stock)
				sys_stock['val_rate'] = row[3]
				sys_stock['actual_qty'] += 1
				self.make_sl_entry(is_submit, row, -1, sys_stock)

			if is_submit == 1:
				self.add_data_in_CSV(qty_diff, rate_diff)
				
			msgprint("Stock Reconciliation Completed Successfully...")
			

	def add_data_in_CSV(self, qty_diff, rate_diff):
		"""Add diffs column in attached file"""
		
		# add header
		out = "'Item Code', 'Warehouse', 'Qty', 'Valuation Rate', 'Qty Diff', 'Val Rate Diff'"
		
		# add data
		for d in self.data:
			s = [cstr(i) for i in d] + [cstr(qty_diff), cstr(rate_diff)]
			out += "\n" + ','.join(s)
		
		# write to file
		fname = self.doc.file_list.split(',')
		from webnotes.utils import file_manager
		file_manager.write_file(fname[1], out)
		
			

	def on_submit(self):
		if not self.doc.file_list:
			msgprint("Please attach file before submitting.", raise_exception=1)
		else:
			self.do_stock_reco(is_submit = 1)
			


	def on_cancel(self):
		self.validate()
		self.do_stock_reco(is_submit = -1)
