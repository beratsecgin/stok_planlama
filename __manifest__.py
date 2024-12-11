{
    'name': 'Stok Planlama',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Module for stock planning and performance reporting',
    'description': """
        A module to track and manage stock, sales KPIs, and inventory performance.
        Features:
        - Sales and inventory tracking
        - KPI reporting
        - Dynamic filtering
    """,
    'author': 'Berat Seçgin',
    'website': 'https://test.togo.com.tr',
    'depends': ['base', 'sale', 'stock'],  
    'data': [
        'security/ir.model.access.csv',
        'views/sales_kpi_views.xml',
        'data/sales_kpi_data.xml',  # To test sample data set
    ],
    'installable': True,
    'application': True,
}
