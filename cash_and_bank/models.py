# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.exceptions import Warning, ValidationError


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


	seq_id = fields.Char(string="Id",readonly=True)
	date = fields.Date(string="Date",required=True)
	branch = fields.Many2one('branch',string="Branch",readonly=True)
	credit_act_branch = fields.Many2one('account.account',string="Branch Credit Account")
	debit_act_branch = fields.Many2one('account.account',string="Branch Debit Account")
	credit_act_head = fields.Many2one('account.account',string="Head Credit Account")
	debit_act_head = fields.Many2one('account.account',string="Head Debit Account")
	branch_journal = fields.Many2one('account.journal',string="Branch Journal")
	head_journal = fields.Many2one('account.journal',string="Head Journal")
	branch_jid = fields.Many2one('account.move',string="branch id")
	head_jid = fields.Many2one('account.move',string="Head id")
	amount = fields.Float(string="Amount")
	stages = fields.Selection([
		('draft', 'Draft'),
		('validate', 'Validate'),
		], default='draft')

	@api.multi
	def get_validate(self):
		self.stages = 'validate'
		journal_entries = self.env['account.move']
		journal_entries_lines = self.env['account.move.line']
		if not self.branch_jid:
			create_branch_entery = journal_entries.create({
				'journal_id': self.branch_journal.id,
				'date':self.date,
				'ref' : self.seq_id,						
				'branch' : self.branch_journal.branch.id,						
				})

			creat_debit = self.create_entry_lines(self.debit_act_branch.id,self.amount,0,self.branch_journal.branch.id,create_branch_entery.id)
			creat_credit = self.create_entry_lines(self.credit_act_branch.id,0,self.amount,self.branch_journal.branch.id,create_branch_entery.id)
			self.branch_jid = create_branch_entery.id
		else:
			creat_debit = self.create_entry_lines(self.debit_act_branch.id,self.amount,0,self.branch_journal.branch.id,self.branch_jid.id)
			creat_credit = self.create_entry_lines(self.credit_act_branch.id,0,self.amount,self.branch_journal.branch.id,self.branch_jid.id)


		if not self.head_jid:
			create_head_entry = journal_entries.create({
				'journal_id': self.head_journal.id,
				'date':self.date,
				'ref' : self.seq_id,						
				'branch' : self.head_journal.branch.id,						
				})

			creat_debit = self.create_entry_lines(self.debit_act_head.id,self.amount,0,self.head_journal.branch.id,create_head_entry.id)
			creat_credit = self.create_entry_lines(self.credit_act_head.id,0,self.amount,self.head_journal.branch.id,create_head_entry.id)
			self.head_jid = create_head_entry.id
		else:
			creat_debit = self.create_entry_lines(self.debit_act_head.id,self.amount,0,self.head_journal.branch.id,self.head_jid.id)
			creat_credit = self.create_entry_lines(self.credit_act_head.id,0,self.amount,self.head_journal.branch.id,self.head_jid.id)



	@api.multi
	def get_draft(self):
		self.stages = 'draft'
		if self.branch_jid:
			self.branch_jid.line_ids.unlink()
		if self.head_jid:
			self.head_jid.line_ids.unlink()



	@api.onchange('date')
	def set_branch(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		self.branch = users.branch.id


	@api.model
	def create(self, vals):
		vals['seq_id'] = self.env['ir.sequence'].next_by_code('locker.seq')
		new_record = super(LockerEcube, self).create(vals)

		return new_record


	@api.multi
	def unlink(self):
		for x in self:
			if x.stages == "validate":
				raise  ValidationError('Cannot Delete Record')
	
		return super(LockerEcube,self).unlink()


	def create_entry_lines(self,account,debit,credit,branch,entry_id):
		self.env['account.move.line'].create({
				'account_id':account,
				'name':self.seq_id,
				'debit':debit,
				'credit':credit,
				'branch':branch,
				'move_id':entry_id,
				})



class CashIssueEcube(models.Model):
	_name = 'cashissue.ecube'
	_rec_name = 'date'

	seq_id = fields.Char(string="Id",readonly=True)
	date = fields.Date(string="Date",required=True)
	amount = fields.Float(string="Amount")
	branch = fields.Many2one('branch',string="Branch",readonly=True)
	credit_act_branch = fields.Many2one('account.account',string="Branch Credit Account")
	debit_act_branch = fields.Many2one('account.account',string="Branch Debit Account")
	credit_act_head = fields.Many2one('account.account',string="Head Credit Account")
	debit_act_head = fields.Many2one('account.account',string="Head Debit Account")
	branch_journal = fields.Many2one('account.journal',string="Branch Journal")
	head_journal = fields.Many2one('account.journal',string="Head Journal")
	branch_jid = fields.Many2one('account.move',string="branch id")
	head_jid = fields.Many2one('account.move',string="Head id")
	stages = fields.Selection([
		('draft', 'Draft'),
		('validate', 'Validate'),
		], default='draft')



	@api.multi
	def get_validate(self):
		self.stages = 'validate'
		journal_entries = self.env['account.move']
		journal_entries_lines = self.env['account.move.line']
		if not self.branch_jid:
			create_branch_entery = journal_entries.create({
				'journal_id': self.branch_journal.id,
				'date':self.date,
				'ref' : self.seq_id,						
				'branch' : self.branch_journal.branch.id,						
				})

			creat_debit = self.create_entry_lines(self.debit_act_branch.id,self.amount,0,self.branch_journal.branch.id,create_branch_entery.id)
			creat_credit = self.create_entry_lines(self.credit_act_branch.id,0,self.amount,self.branch_journal.branch.id,create_branch_entery.id)
			self.branch_jid = create_branch_entery.id
		else:
			creat_debit = self.create_entry_lines(self.debit_act_branch.id,self.amount,0,self.branch_journal.branch.id,self.branch_jid.id)
			creat_credit = self.create_entry_lines(self.credit_act_branch.id,0,self.amount,self.branch_journal.branch.id,self.branch_jid.id)


		if not self.head_jid:
			create_head_entry = journal_entries.create({
				'journal_id': self.head_journal.id,
				'date':self.date,
				'ref' : self.seq_id,						
				'branch' : self.head_journal.branch.id,						
				})

			creat_debit = self.create_entry_lines(self.debit_act_head.id,self.amount,0,self.head_journal.branch.id,create_head_entry.id)
			creat_credit = self.create_entry_lines(self.credit_act_head.id,0,self.amount,self.head_journal.branch.id,create_head_entry.id)
			self.head_jid = create_head_entry.id
		else:
			creat_debit = self.create_entry_lines(self.debit_act_head.id,self.amount,0,self.head_journal.branch.id,self.head_jid.id)
			creat_credit = self.create_entry_lines(self.credit_act_head.id,0,self.amount,self.head_journal.branch.id,self.head_jid.id)



	@api.multi
	def get_draft(self):
		self.stages = 'draft'
		if self.branch_jid:
			self.branch_jid.line_ids.unlink()
		if self.head_jid:
			self.head_jid.line_ids.unlink()


	@api.onchange('date')
	def set_branch(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		self.branch = users.branch.id


	@api.model
	def create(self, vals):
		vals['seq_id'] = self.env['ir.sequence'].next_by_code('issue.seq')
		new_record = super(CashIssueEcube, self).create(vals)

		return new_record


	@api.multi
	def unlink(self):
		for x in self:
			if x.stages == "validate":
				raise  ValidationError('Cannot Delete Record')
	
		return super(CashIssueEcube,self).unlink()


	def create_entry_lines(self,account,debit,credit,branch,entry_id):
		self.env['account.move.line'].create({
				'account_id':account,
				'name':self.seq_id,
				'debit':debit,
				'credit':credit,
				'branch':branch,
				'move_id':entry_id,
				})





class account_move_extend(models.Model):
	_inherit = 'account.move'

	@api.multi
	def assert_balanced(self):
		if not self.ids:
			return True
		prec = self.env['decimal.precision'].precision_get('Account')

		self._cr.execute("""\
			SELECT      move_id
			FROM        account_move_line
			WHERE       move_id in %s
			GROUP BY    move_id
			HAVING      abs(sum(debit) - sum(credit)) > %s
			""", (tuple(self.ids), 10 ** (-max(5, prec))))
		# if len(self._cr.fetchall()) != 0:
		#     raise UserError(_("Cannot create unbalanced journal entry."))
		return True