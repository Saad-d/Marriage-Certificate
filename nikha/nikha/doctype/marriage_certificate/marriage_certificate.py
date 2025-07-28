# Copyright (c) 2025, Saad and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import date
from frappe.utils import getdate

class MarriageCertificate(Document):
	def before_save(self):
		if self.dob:
			dob_date = getdate(self.dob)
			today = date.today()
			age = today.year - dob_date.year - (
				(today.month, today.day) < (dob_date.month, dob_date.day)
			)
			self.groom_age = str(age)

		if self.bride_dob:
			dob_date = getdate(self.bride_dob)
			today = date.today()
			age_of_bride = today.year - dob_date.year - (
				(today.month, today.day) < (dob_date.month, dob_date.day)
			)
			self.age = str(age_of_bride)
	# def before_save(self):
    #     if self.dob:
    #         today = date.today()
    #         self.groom_age = today.year - self.dob.year - (
    #             (today.month, today.day) < (self.dob.month, self.dob.day)
    #         )
	