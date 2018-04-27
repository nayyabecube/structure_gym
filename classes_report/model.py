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
    _name = 'report.classes_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('classes_report.customer_report')
        active_wizard = self.env['classes.reports'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['classes.reports'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['classes.reports'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        branch = record_wizard.branch
        classes = record_wizard.classes
        types = record_wizard.types
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to


        if types == "all":
            branches = []
            rec = self.env['branch'].search([])
            for x in rec:
                branches.append(x)

        if types == "specfic":
            branches = []
            for x in branch:
                branches.append(x)


        record = []
        def get_rec(attr):
            del record [:]
            records = self.env['reg.form'].search([('branch','=',attr),('gymclasses','=',record_wizard.classes.id),('stages','=','member'),('joining','>=',record_wizard.date_from),('joining','<=',record_wizard.date_to)])
            for x in records:
                record.append(x)



        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'reg.form',
            'classes': classes.name,
            'date_from': date_from,
            'date_to': date_to,
            'record': record,
            'branches': branches,
            'get_rec': get_rec,
    
            }

        return report_obj.render('classes_report.customer_report', docargs)