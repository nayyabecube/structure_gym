# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from datetime import date, datetime, timedelta
from openerp.exceptions import Warning, ValidationError, UserError
from odoo import exceptions, _


class EcubeAttendance(models.Model):
	_name = 'ecube.attendance'
	_rec_name = 'date'

	date = fields.Date(string="Date", required= True)
	stages = fields.Selection([('draft','Draft'),('approved','Approved')],string='Stages',default='draft')
	tree_link = fields.One2many('ecube.attendance.tree','tree_linked')


						
	@api.multi
	def in_waiting(self):
		self.stages = "draft"
						
	@api.multi
	def in_validate(self):
		counter = 0
		for x in self.tree_link:
			if x.approved != True:
				counter = counter + 1

		print counter

		if counter == 0:
			self.stages = "approved"
		else:
			raise ValidationError('Please Approve all the Overtimes')

	@api.multi
	def unlink(self):
		for x in self:
			if x.stages == "approved":
				raise  ValidationError('Cannot Delete Record')
	
		return super(EcubeAttendance,self).unlink()

class EcubeAttendanceTree(models.Model):
	_name = 'ecube.attendance.tree'

	employee = fields.Many2one('hr.employee',string="Employee", required= True)
	working_days = fields.Float(string="Total Days") 
	late_arrival = fields.Float(string="Late Arrival")
	half_day = fields.Float(string="Half Day")
	absent = fields.Float(string="Absent")
	total_work_days = fields.Float(string="Working Days" ,readonly=True)
	remarks = fields.Char(string="Remarks")
	approved = fields.Boolean(string="Approved" , default = True)
	tree_linked = fields.Many2one('ecube.attendance')



	@api.onchange('late_arrival','half_day','absent','working_days')
	def calculate_working_days(self):
		total_late_aririval = 0
		total_late_aririval = self.late_arrival/4
		total_late_half_days = self.half_day/2
		self.total_work_days = self.working_days - total_late_aririval - total_late_half_days - self.absent