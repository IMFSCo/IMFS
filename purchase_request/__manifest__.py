{
    "name": "Purchase Request",
<<<<<<< HEAD
    "version": "12.0.1",
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
    "summary": "Use this module to have notification of requirements of "
               "materials and/or external services and keep track of such "
               "requirements",
=======
    "author": "SIT & think digital",
    "version": "12.0.1",
    "summary": "Use this module to have notification of requirements of "
               "materials and/or external services and keep track of such "
               "requirements",
    "category": "Purchase Management",
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
    "depends": ['mail',
        "purchase",
        "product","purchase_requisition"
    ],
    "data": [
        "security/purchase_request.xml",
        "security/ir.model.access.csv",
        'wizard/wizard_view.xml',
        "data/purchase_request_sequence.xml",
        "data/purchase_request_data.xml",
        "data/pr_mail_template.xml",
        "views/purchase_request_view.xml",
        'views/request_for_purchase_view.xml',
        "reports/report_purchaserequests.xml",
#        "reports/report_modify_rfq.xml",
        "views/purchase_request_report.xml",
    ],
    
    'installable': True
}
