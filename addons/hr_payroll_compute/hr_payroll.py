#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2015 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
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
##############################################################################
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval



class hr_salary_rule(osv.osv):

    _inherit = 'hr.salary.rule'

    _columns = {
        'amount_python_compute':fields.text('Python Code'),
        'condition_python':fields.text('Python Condition', required=True, readonly=False, help='Applied this rule for calculation if condition is true. You can specify condition like basic > 1000.'),
        'condition_select': fields.selection([('none', 'Always True'),('range', 'Range'), ('python', 'Python Expression')], "Condition Based on", required=True),
        # FIXME: can I extend this rather than override it completely?
        'amount_select':fields.selection([
            ('percentage','Percentage (%)'),
            ('fix','Fixed Amount'),
            ('code','Python Code'),
        ],'Amount Type', select=True, required=True, help="The computation method for the rule amount."),
    }
    _defaults = {
        'amount_python_compute': '''
# Available variables:
#----------------------
# payslip: object containing the payslips
# employee: hr.employee object
# contract: hr.contract object
# rules: object containing the rules code (previously computed)
# categories: object containing the computed salary rule categories (sum of amount of all rules belonging to that category).
# worked_days: object containing the computed worked days.
# inputs: object containing the computed inputs.

# Note: returned value have to be set in the variable 'result'

result = contract.wage * 0.10''',
        'condition_python':
'''
# Available variables:
#----------------------
# payslip: object containing the payslips
# employee: hr.employee object
# contract: hr.contract object
# rules: object containing the rules code (previously computed)
# categories: object containing the computed salary rule categories (sum of amount of all rules belonging to that category).
# worked_days: object containing the computed worked days
# inputs: object containing the computed inputs

# Note: returned value have to be set in the variable 'result'

result = rules.NET > categories.NET * 0.10''',
    }

    def _extended_compute(self, cr, uid, rule, localdict, context=None):
        if rule.amount_select == 'code':
            try:
                eval(rule.amount_python_compute, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), 'result_qty' in localdict and localdict['result_qty'] or 1.0, 'result_rate' in localdict and localdict['result_rate'] or 100.0
            except:
                raise osv.except_osv(_('Error!'), _('Wrong python code defined for salary rule %s (%s).')% (rule.name, rule.code))
        else:
            return super(hr_salary_rule, self)._extended_compute(cr, uid, rule, localdict, context=context)

    def _extended_condition(self, cr, uid, rule, localdict, context=None):
        if rule.condition_select == 'code':
            try:
                eval(rule.condition_python, localdict, mode='exec', nocopy=True)
                return 'result' in localdict and localdict['result'] or False
            except:
                raise osv.except_osv(_('Error!'), _('Wrong python condition defined for salary rule %s (%s).')% (rule.name, rule.code))
        else:
            return super(hr_salary_rule, self)._extended_condition(cr, uid, rule, localdict, context=context)

class hr_payslip(osv.osv):
    '''
    Pay Slip
    '''

    _inherit = 'hr.payslip'

    def _get_rule_data(self, rule):
        result = super(hr_payslip, self)._get_rule_data(rule)
        result['amount_python_compute'] = rule.amount_python_compute
        result['condition_python'] = rule.condition_python

