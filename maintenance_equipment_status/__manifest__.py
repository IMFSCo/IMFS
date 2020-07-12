# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Maintenance Equipment Status',
    'version': '11.0.1.0.0',
<<<<<<< HEAD
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
=======
    'category': '',
    'author': 'Eficent, Odoo Community Association (OCA)',
    'website': 'http://github.com/OCA/maintenance',
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
    'license': 'LGPL-3',
    'depends': [
        'maintenance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_equipment_status_views.xml',
        'views/maintenance_equipment_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
