{
    'name': 'Booking Order',
    'summary': """
                Booking Order
                """,
    'version': '10.0',
    'sequence' : 1,
    'author': 'Sukma Risfa Sam Bima Yudha',
    'company': 'HashMicro',
    'website': 'https://www.hashmicro.com/',
    'category': 'Custom Development',
    'depends': ['base', 'sale'],
    'data': [
        'data/sequence.xml',

        # Views
        'views/service_team_views.xml',
        'views/sale_order_views.xml',
        'views/work_order_views.xml',
        'views/menu_views.xml',

        # Wizard
        'wizards/cancel_work_order.xml',

        # Report
        'reports/report.xml',
        'reports/report_work_order.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}