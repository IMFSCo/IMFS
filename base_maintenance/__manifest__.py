# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Base Maintenance",
    "version": "11.0.1.0.0",
<<<<<<< HEAD
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
=======
    "author": "Eficent, "
              "Odoo Community Association (OCA)",
    "development_status": "Beta",
    "website": "https://www.github.com/OCA/maintenance",
    "category": "Maintenance",
>>>>>>> e97b44b4024a274708fe25810a6af1e1ef67e33e
    "license": "AGPL-3",
    "depends": [
        "maintenance",
    ],
    "data": [
        "security/maintenance_security.xml",
        "security/ir.model.access.csv",
        "views/maintenance_team_views.xml",
        "views/maintenance_request_views.xml",
    ],
    "installable": True,
}
