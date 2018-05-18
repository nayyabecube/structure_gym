# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from datetime import date, datetime, timedelta

class EmployeeFormExtension(models.Model):
	_inherit = 'hr.employee'

	salaried_person = fields.Boolean(string="Salaried Person")
	rate_per_piece = fields.Boolean(string="Rate Per Piece")
	employee_type = fields.Selection([
		('temporary','Temporary'),
		('permanent','Permanent')
		],string='Employee Type',default='temporary')
	card_no = fields.Many2one('emp.card.num',string='Card No')
	# schedule = fields.Many2one('shifts.attendence',string='Shift')
	dor = fields.Date(string='DOR')
	doj = fields.Date(string='Date of Joining')
	doi = fields.Date(string='Date of issue',default=fields.Date.today)
	confirmation_date = fields.Date(string='Confirmation Date')
	religion = fields.Selection([
		('muslim','Muslim'),
		('non_musliom','Non Muslim')
		],string='Religion',default='muslim')
	fname = fields.Char(string='Father Name')
	cnic = fields.Char(string='CNIC NO')
	# social_security = fields.Boolean(string="Social Security")
	# ss_no = fields.Char(string="SS No")
	# eobi = fields.Boolean(string="EOBI")
	# merchant = fields.Boolean(string="Merchant")
	# eobi_no = fields.Char(string="EOBI No")
	name_card = fields.Char(string="Name")
	
	reff_name = fields.Char(string="Name")
	reff_city = fields.Char(string="City")
	reff_cnic = fields.Char(string="CNIC")
	reff_relation = fields.Char(string="Relation")
	qualification = fields.Char(string="Qualification")
	contact_address = fields.Char(string="Home Address")
	ntn = fields.Char(string="NTN")
	bank_account_id = fields.Char(string="Account Number")

	# experience_tree = fields.One2many("hr.employee.experience","tree_link")
	# leave_tree = fields.One2many("hr.employee.vocations","linked")
	bank = fields.Many2one("account.journal",string="Bank")
	incharge = fields.Many2one("hr.employee",string="Incharge")
	resigned = fields.Boolean(string="Resigned")

	# salary = fields.Float(string="Salary")
	# salary_structure = fields.Many2one('hr.payroll.structure',string="Salary Structure")\

