#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.trail_balance_sql.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('trail_balance_sql.customer_report')
        active_wizard = self.env['trail.balance.sql'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['trail.balance.sql'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['trail.balance.sql'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()


        date = record_wizard.date

        # MoveLine = self.env['account.move.line']
        # total = MoveLine.with_context(date=self.env.context.get('date'))._query_get()
        # p
        # total = self.env.cr.execute("select * From 'MoveLine'")
        # order_list = self.env.cr.execute('select mrp_production_id from mrp_rel_mo where mrp_rel_mo_id = %s', (self.id))
        # self.env.cr.execute("select credit FROM account_move_line")
        # order_list = self.env.cr.browse()
        # print order_list
        # print "mmmmmmmmmmmmmmmmmmmmmmmm"

        # qry = "select * From account_account;"
        # self._cr.execute(qry)
        # result = self._cr.dictfetchall() 
        # print result
        # print "nnnnnnnnnnnnnnn"
        # print "nnnnnnnnnnnnnnn"
        # print "nnnnnnnnnnnnnnn"
        # user_ids=[] 
        # for ids in result:
        #     user_ids.append(ids.get('id'))

        # print user_ids
        # print "nnnnnnnnn"

        records = []
        rec = self.env['account.account'].search([('user_type_id.name','!=','View_Type')])
        for x in rec:
            records.append(x)

        def get_debit(num):
            # deb = 0
            # rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
            # for x in rec:
            #     deb = deb + x.debit
            pre_field = "debit"
            table_name = "account_move_line"
            line_id = num
            self.env.cr.execute("select SUM("+pre_field+") FROM "+table_name+" WHERE account_id = "+str(line_id)+" ")
            result = self._cr.fetchall()[0]

            return result


        def get_credit(num):
            # cre = 0
            # rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
            # for x in rec:
            #     cre = cre + x.credit

            # return cre
            pre_field = "credit"
            table_name = "account_move_line"
            line_id = num
            self.env.cr.execute("select SUM("+pre_field+") FROM "+table_name+" WHERE account_id = "+str(line_id)+" ")
            result = self._cr.fetchall()[0]

            return result

        def get_net(num):
            cre = 0
            deb = 0
            net = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
            for x in rec:
                cre = cre + x.credit
                deb = deb + x.debit

            net = deb - cre

            return abs(net)




        

        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.move',
            'date': date,
            'records': records,
            'get_debit': get_debit,
            'get_credit': get_credit,
            'get_net': get_net,

            }

        return report_obj.render('trail_balance_sql.customer_report', docargs)