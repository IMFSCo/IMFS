# -*- coding: utf-8 -*-
{
    'name': "Automation Creation of Requisition",
    'summary': """customization for automated creation of internal requisition from manufacturing order""",
    'author': "SIT & think digital",
    'website': "http://sitco.odoo.com/",
    'category': 'Custom',
    'version': '12.0.1',

    'depends': ['mrp'],

    'data': [
        'views/model_view.xml',
            ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
