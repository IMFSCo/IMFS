# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Maintenance Request Sequence',
    'summary': """
        Adds sequence to maintenance requests""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
    'depends': [
        'maintenance',
    ],
    'data': [
        'data/maintenance_request_data.xml',
        'views/maintenance_team.xml',
        'views/maintenance_request.xml',
    ],
}
