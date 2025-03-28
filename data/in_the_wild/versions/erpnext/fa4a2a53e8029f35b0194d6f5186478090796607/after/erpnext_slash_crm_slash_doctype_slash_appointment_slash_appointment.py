# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from collections import Counter
from datetime import timedelta

import frappe
from frappe.model.document import Document
from frappe.desk.form.assign_to import add as add_assignemnt


class Appointment(Document):
	email=''

	def find_lead_by_email(self,email):
		lead_list = frappe.get_list('Lead', filters = {'email_id':email}, ignore_permissions = True)
		if lead_list:
			return lead_list[0].name
		self.email = email
		return None
	
	def before_insert(self):
		number_of_appointments_in_same_slot = frappe.db.count('Appointment', filters = {'scheduled_time':self.scheduled_time})
		settings = frappe.get_doc('Appointment Booking Settings')
		if(number_of_appointments_in_same_slot >= settings.number_of_agents):
			frappe.throw('Time slot is not available')
		# Link lead
		self.lead = self.find_lead_by_email(self.lead)

	def after_insert(self):
		# Auto assign
		self.auto_assign()
		# Check if lead was found 
		if(self.lead):
			# Create Calendar event
			self.create_calendar_event()
		else:
			# Send email to confirm
			verify_url = ''.join([frappe.utils.get_url(),'/book-appointment/verify?email=',self.email,"&appoitnment=",self.name]))
			frappe.sendmail(recipients=[self.email],message=verify_url',self.email,"&appoitnment=",self.name),subject="")
			frappe.msgprint("Please check your email to confirm the appointment")

	def set_verified(self,email):
		# Create new lead
		self.create_lead(email)
		# Create calender event
		self.create_calendar_event()
		self.save( ignore_permissions=True )
		frappe.db.commit()

	def create_lead(self,email):
		lead = frappe.get_doc({
			'doctype':'Lead',
			'lead_name':self.customer_name,
			'email_id':email,
			'notes':self.customer_details,
			'phone':self.customer_phone_number,
		})
		print(lead.insert( ignore_permissions=True ))
		# Link lead
		self.lead = lead.name

	def auto_assign(self):
		available_agents = _get_agents_sorted_by_asc_workload(self.scheduled_time.date())
		for agent in available_agents:
			if(_check_agent_availability(agent, self.scheduled_time)):
				agent = agent[0]
				add_assignemnt({
					'doctype':self.doctype,
					'name':self.name,
					'assign_to':agent
				})
			break

	def create_calendar_event(self):
		appointment_event = frappe.get_doc({
			'doctype': 'Event',
			'subject': ' '.join(['Appointment with', self.customer_name]),
			'starts_on': self.scheduled_time,
			'status': 'Open',
			'type': 'Public',
			'send_reminder': frappe.db.get_single_value('Appointment Booking Settings','email_reminders'),
			'event_participants': [dict(reference_doctype = "Lead", reference_docname = self.lead)]
		})
		employee = _get_employee_from_user(self._assign)
		if employee:
			appointment_event.append('event_participants', dict(
				reference_doctype = 'Employee',
				reference_docname = employee.name))
		appointment_event.insert(ignore_permissions=True)
		self.calendar_event = appointment_event.name
		self.save(ignore_permissions=True)

def _get_agents_sorted_by_asc_workload(date):
	appointments = frappe.db.get_list('Appointment', fields='*')
	agent_list = _get_agent_list_as_strings()	
	if not appointments:
		return agent_list
	appointment_counter = Counter(agent_list)
	for appointment in appointments:
		assigned_to = frappe.parse_json(appointment._assign)
		if not assigned_to:
			continue
		if (assigned_to[0] in agent_list) and appointment.scheduled_time.date() == date:
			appointment_counter[assigned_to[0]] += 1
	sorted_agent_list = appointment_counter.most_common()
	sorted_agent_list.reverse()
	
	return sorted_agent_list

def _get_agent_list_as_strings():
	agent_list_as_strings = []
	agent_list = frappe.get_doc('Appointment Booking Settings').agent_list
	for agent in agent_list:
		agent_list_as_strings.append(agent.user)
	return agent_list_as_strings


def _check_agent_availability(agent_email,scheduled_time):
	appointemnts_at_scheduled_time = frappe.get_list('Appointment', filters = {'scheduled_time':scheduled_time})
	for appointment in appointemnts_at_scheduled_time:
		if appointment._assign == agent_email:
			return False
	return True


def _get_employee_from_user(user):
	employee_docname = frappe.db.exists({'doctype':'Employee', 'user_id':user})
	if employee_docname:
		return frappe.get_doc('Employee', employee_docname[0][0]) # frappe.db.exists returns a tuple of a tuple
	return None