
{
  "name"                 :  "Equipment Allocations",
  "summary"              :  "The module provides a way to manage workplace equipments. The user can enter the repective request for an equipment allocation to an employee.",
  "category"             :  "Custom",
  "version"              :  "11.0.1",
  "author"               :  "Muhammad Faizan",
  "license"              :  "Other proprietary",
  "website"              :  "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
  "description"          :  """Odoo Equipment Allocations
Manage office equipment in odoo
Maintain equipment records in Odoo
Odoo equipment allocation records
Lend equipment to employees
Assign equipment to employees
""",
  "live_test_url":"http://odoodemo.webkul.com/?module=equipment_allocations",
  "depends":['hr_maintenance','maintenance','stock','hr','web'],
  "data":  [
      'edi/mail_template.xml',
      'security/maintenance_security.xml',
      'security/ir.model.access.csv',
      'wizard/wizard_view.xml',
      'wizard/allocation_wizard_view.xml',
      'wizard/replace_equipment_view.xml',
      'report/allocation_report.xml',
      'views/wk_maintenance.xml',
      'views/model_view.xml'
                            ],
#  "demo":['data/demo.xml'],
  "images":['static/description/Banner.png'],
  "application":True,
  "installable":True,
  "auto_install":False,
  "price":45,
  "currency":"EUR",
 # "pre_init_hook":"pre_init_check",
}
