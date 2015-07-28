#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
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

{
    'name': 'Payroll Configurable Compute',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 39,
    'description': """
Dynamic salary computation for the Generic Payroll.
=======================

Adds python_compute methods to the salary methods.
    """,
    'author': 'OpenERP SA',
    'website': 'https://www.odoo.com/page/employees',
    'depends': [
        'hr',
        'hr_contract',
        'hr_holidays',
        'hr_payroll',
        'decimal_precision',
        'report',
    ],
    'data': [
    ],
    'test': [
        #'test/payslip.yml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
