# -*- coding: utf-8 -*-
{
    'name': "HR Attendance Sheet And Policies",

    'summary': """Managing  Attendance Sheets for Employees
        """,

    'description': """
        
    """,

<<<<<<< HEAD
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
=======
    'author': "Ramadan Khalil",
    'website': "rkhalil1990@gmail.com",
    'price': 99,
    'currency': 'EUR',

    'category': 'hr',
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
    'version': '0.2',
    'images': ['static/description/bannar.jpg'],

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                'hr_payroll',
                'hr_holidays',
                'hr_attendance'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/change_att_data_view.xml',
        'views/hr_attendance_sheet_view.xml',
        'views/hr_attendance_policy_view.xml',
        'wizard/change_att_data_view.xml',
        'data/hr_attendance_sheet_data.xml',
    ],

    'license': 'OPL-1',
    'demo': [
        'demo/demo.xml',
    ],
}
