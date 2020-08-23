# -*- coding: utf-8 -*-
{
    'name': 'Payroll Customization',
    'summary': """Payroll module related customizations""",
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
    'version': '11.0.1',

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
