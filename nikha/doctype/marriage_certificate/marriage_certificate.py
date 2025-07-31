# Copyright (c) 2025, Saad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date
from frappe.utils import getdate
from frappe.utils.pdf import get_pdf
from frappe.utils.file_manager import save_file

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


	# def on_submit(self):
	# 	send_marriage_certificate_email(self, self.email_of_groom, self.groom_name)
	# 	send_marriage_certificate_email(self, self.email_of_bride, self.bride_name)



    

def send_marriage_certificate_email(doc, recipient_email, recipient_name):
    if not recipient_email:
        frappe.msgprint(f"Email not provided for {recipient_name}")
        return

    # Generate PDF
    pdf_data = frappe.get_print(doc.doctype, doc.name, print_format="Test", as_pdf=True)

    # Save PDF to attach in email
    file_name = f"{doc.name}.pdf"
    file_doc = save_file(file_name, pdf_data, doc.doctype, doc.name, is_private=1)

    # Email content
    subject = f"Marriage Certificate - {doc.groom_name} & {doc.bride_name}"
    message = f"""
    Dear {recipient_name},

    Congratulations! Please find attached your official Marriage Certificate.

    Regards,  
    NikahNama Team
    """

    # Send email
    frappe.sendmail(
        recipients=[recipient_email],
        subject=subject,
        message=message,
        attachments=[{
            "fname": file_name,
            "fcontent": pdf_data
        }],
        reference_doctype=doc.doctype,
        reference_name=doc.name
    )