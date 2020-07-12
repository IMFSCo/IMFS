# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Maintenance Plan',
 'summary': 'Extends preventive maintenance planning',
<<<<<<< HEAD
 'author': "Muhammad Faizan",
 'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
 'category': 'Custom',
 'version': '12.0.3.1.1',
 'license': 'AGPL-3',
=======
 'version': '12.0.3.1.1',
 'author': 'Camptocamp SA, Eficent, Odoo Community Association (OCA)',
 'license': 'AGPL-3',
 'category': 'Maintenance',
 'website': 'https://github.com/OCA/maintenance',
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
 'images': [],
 'depends': [
     'maintenance',
     ],
 'data': [
     'security/ir.model.access.csv',
     'views/maintenance_kind_views.xml',
     'views/maintenance_plan_views.xml',
     'views/maintenance_equipment_views.xml',
     ],
 'demo': [
     'data/demo_maintenance_plan.xml'
 ],
 'post_init_hook': 'post_init_hook',
 'installable': True,
 }
