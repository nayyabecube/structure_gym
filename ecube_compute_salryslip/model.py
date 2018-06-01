# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from datetime import date, datetime, timedelta
from openerp.exceptions import Warning, ValidationError, UserError
from odoo import exceptions, _

class EcubeEmployeeComputedSalary(models.Model):
	_inherit = 'hr.employee'

	
	@api.model 
	def EcubeAttendance_WorkingDays(self, payslip):
		# result=employee.EcubeAttendance_WorkingDays(payslip)
		duration = 0.0
		tsheet_obj = self.env['ecube.attendance'] 
		timesheets = tsheet_obj.search([('date', '>=', payslip.date_from),('date', '<=', payslip.date_to)])
		for x in timesheets:
			for y in x.tree_link:
				if y.employee.id == self.id:
					duration = duration + float(y.total_work_days)
		return duration


	@api.model 
	def EcubeAttendance_Actual_pay(self, payslip):
		# result=employee.EcubeAttendance_Actual_pay(payslip)
		actual_working_days = 0.0
		actual_month_days = 0.0
		absent_days = 0.0
		duration = 0.0
		tsheet_obj = self.env['ecube.attendance'] 
		timesheets = tsheet_obj.search([('date', '>=', payslip.date_from),('date', '<=', payslip.date_to)])
		for x in timesheets:
			for y in x.tree_link:
				if y.employee.id == self.id:
					actual_working_days = duration + float(y.total_work_days)
					actual_month_days = duration + float(y.working_days)
		absent_days = actual_month_days - actual_working_days
		duration = (self.contract_id.wage / actual_month_days ) * absent_days

		return duration

	
	@api.model 
	def Salary_Slip_Deduction_Advance(self, payslip):
		# result=employee.Salary_Slip_Deduction_Advance(payslip)
		duration = 0.0 
		timesheets = self.env['ecube.deduction'].search([('date', '>=', payslip.date_from),('date', '<=', payslip.date_to),('employee_id','=',self.id)])
		for x in timesheets:
			if x.type_id.name == "Advance":
				duration = duration + x.amount
		return duration
