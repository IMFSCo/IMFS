# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Maintenance Plan',
 'summary': 'Extends preventive maintenance planning',
 'author': "Muhammad Faizan",
 'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
 'category': 'Custom',
 'version': '12.0.3.1.1',
 'license': 'AGPL-3',
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
