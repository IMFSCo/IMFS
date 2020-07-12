# -*- coding: utf-8 -*-
{
    'name': 'Payroll Customization',
    'summary': """Payroll module related customizations""",
<<<<<<< HEAD
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
=======
    'author': "SIT & think digital",
    'website': "http://sitco.odoo.com/",
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
    'category': 'Custom',
    'version': '12.0.1',

    'depends': ['hr_payroll', 'hr_contract', 'account', 'base', 'hr','mail',
                ],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/multi_payslip_confirm.xml',
        'views/deductions_views.xml',
        'views/inherited_views.xml',
            ],

    'demo': [],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
