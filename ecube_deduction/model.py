# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError, UserError
import datetime
import datetime as dt


class EcubeDeductionClass(models.Model):
	_name = 'ecube.deduction'
	_rec_name = 'employee_id'

	description = fields.Text(string="Description")
	amount = fields.Float(string="Amount", required=True)

	employee_id = fields.Many2one('hr.employee',string="Employee", required=True)
	type_id = fields.Many2one('ecube.deduction.type',string="Type", required=True)

	date = fields.Date(string="Date", required=True)

class EcubePayrollTypeClass(models.Model):
    _name = 'ecube.deduction.type'
    _rec_name = 'name'

    name = fields.Char(string="Name")

