{
    'name': 'Booking Order',
    'version': '1.0',
    'sequence' : 1,
    'author': 'Sukma Risfa Sam Bima Yudha',
    'company': 'HashMicro',
    'website': 'https://www.hashmicro.com/',
    'summary': 'Adds a complete booking order management system.',
    'description': """
Manage Service Bookings & Work Orders
=====================================
This module allows you to manage service teams, create booking orders, check team availability to prevent double bookings, and automatically generate work orders upon confirmation.

Key Features:
------------
- Service Team Management
- Booking Order creation from Sales Orders
- Team availability check
- Automatic Work Order generation
- Work Order status tracking (Pending, In Progress, Done, Cancelled)
    """,
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