{
    'name': 'Product/Material Internal Requisitions by Employees/Users',
    'version': '12.0.1',
    'summary': """This module allow your employees/users to create Internal Requisitions.""",
<<<<<<< HEAD
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
=======
    'author': 'SIT & think digital',
    'website': 'http://sitco.odoo.com',
    'category': 'Warehouse',
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
    'depends': ['stock','product','hr','purchase_requisition','purchase_request','sh_message'],
    'data':[
        'security/ir.model.access.csv',
        'security/requisition_security.xml',
        'wizard/wizard_view.xml',
        'wizard/manufacturing_report_view.xml',
        'data/requisition_sequence.xml',
        'data/employee_approval_template.xml',
        'data/confirm_template.xml',
        'report/requisition_report.xml',
        'views/requisition_view.xml',
        'views/hr_employee_view.xml',
        'views/stock_picking_view.xml',
        'views/automatic_purchase_request.xml',
    ],
    'installable' : True,
    'application' : False,
}
