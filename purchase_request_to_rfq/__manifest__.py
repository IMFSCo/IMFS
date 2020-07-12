{
    "name": "Purchase Request to RFQ",
    "version": "12.0.1",
    'author': "Muhammad Faizan",
    'website': "https://www.linkedin.com/in/engr-muhammad-faizan-80011782/",
    'category': 'Custom',
    "depends": [
        "purchase_request",
        "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence.xml",
        "wizard/purchase_request_line_make_purchase_order_view.xml",
        "views/purchase_request_view.xml",
        "views/purchase_order_view.xml",
    ],
    
    "installable": True
}
