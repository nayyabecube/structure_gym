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
from num2words import num2words

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.salary_slip.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('salary_slip.module_report')
        records = self.env['hr.payslip'].browse(docids)


        basic = []
        for x in records.line_ids:
            if x.salary_rule_id.category_id.name == "Basic":
                basic.append(x)


        allow = []
        for x in records.line_ids:
            if x.salary_rule_id.category_id.name == "Allowance":
                allow.append(x)

        deduct = []
        for x in records.line_ids:
            if x.salary_rule_id.category_id.name == "Deduction":
                deduct.append(x)


        net = []
        for x in records.line_ids:
            if x.salary_rule_id.category_id.name == "Net":
                net.append(x)





        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': records,
            'basic': basic,
            'allow': allow,
            'deduct': deduct,
            'net': net,

            }

        return report_obj.render('salary_slip.module_report', docargs)

    