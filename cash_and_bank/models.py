# -*- coding: utf-8 -*-
from openerp import models, fields, api


class account_extend(models.Model):
	_inherit = 'account.bank.statement'

	branch = fields.Many2one('branch',string="Branch",readonly=True)
	actual_bal = fields.Float(string="Ledger Balance",compute="compute_act_tot")
	virtual_bal = fields.Float(string="Cash Book Balance",compute="compute_vit_tot")
	total_bal = fields.Float(string="Total Balance",compute="compute_tot_tot")
	check = fields.Boolean(compute="check_status")
	test = fields.Boolean()


	@api.one
	def check_status(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if users.reconciled == True:
			self.check = True
		else:
			self.check = False



	# @api.onchange('journal_id')
	# def select_branch(self):
	# 	users = self.env['res.users'].search([('id','=',self._uid)])
	# 	if self.journal_id:
	# 		self.branch = users.branch.id


	@api.onchange('name')
	def select_journal(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if users.reconciled == True:
			self.test = True
		else:
			self.test = False
		self.branch = users.branch.id
		rec = self.env['account.journal'].search([('type','=','cash'),('branch','=',self.branch.id)])
		if rec:
			for x in rec:
				self.journal_id = x[0].id



	@api.one
	def compute_act_tot(self):
		deb = 0
		cre = 0
		tot = 0
		rec = self.env['account.move.line'].search([('account_id','=',self.journal_id.default_debit_account_id.id)])
		for x in rec:
			deb = deb + x.debit
			cre = cre + x.credit

		tot = deb - cre
		self.actual_bal = tot


	@api.one
	def compute_vit_tot(self):
		rec = self.env['account.bank.statement'].search([('journal_id','=',self.journal_id.id)])
		for x in rec:
			if x.line_ids:
				for y in x.line_ids:
					if not y.journal_entry_ids:
						self.virtual_bal = self.virtual_bal + y.amount


		# if self.line_ids:
		# 	for x in self.line_ids:
		# 		if not x.journal_entry_ids:
		# 			self.virtual_bal = self.virtual_bal + x.amount



	@api.one
	def compute_tot_tot(self):
		self.total_bal = self.actual_bal + self.virtual_bal


class LockerEcube(models.Model):
	_name = 'locker.ecube'
	_rec_name = 'date'

	date = fields.Date(string="Date",required=True)
	branch = fields.Many2one('branch',string="Branch",readonly=True)
	amount = fields.Float(string="Amount")
	stages = fields.Selection([
		('draft', 'Draft'),
		('validate', 'Validate'),
		], default='draft')

	@api.multi
	def get_validate(self):
		self.stages = 'validate'


	@api.multi
	def get_draft(self):
		self.stages = 'draft'


	@api.onchange('date')
	def set_branch(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		self.branch = users.branch.id



class CashIssueEcube(models.Model):
	_name = 'cashissue.ecube'
	_rec_name = 'date'

	date = fields.Date(string="Date",required=True)
	amount = fields.Float(string="Amount")
	account_id = fields.Many2one('account.account',string="Account")
	stages = fields.Selection([
		('draft', 'Draft'),
		('validate', 'Validate'),
		], default='draft')


	@api.multi
	def get_validate(self):
		self.stages = 'validate'


	@api.multi
	def get_draft(self):
		self.stages = 'draft'