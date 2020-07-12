# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Maintenance Request Sequence',
    'summary': """
        Adds sequence to maintenance requests""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
<<<<<<< HEAD
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
=======
    'author': 'Creu Blanca,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/maintenance',
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
    'depends': [
        'maintenance',
    ],
    'data': [
        'data/maintenance_request_data.xml',
        'views/maintenance_team.xml',
        'views/maintenance_request.xml',
    ],
}
