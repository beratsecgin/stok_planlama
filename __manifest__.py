{
    'name': 'Stok Planlama Modülü',
    'version': '1.0.0',
    'summary': 'Stok planlama ve haftalık değişim raporlarını analiz etme modülü.',
    'description': """
        Bu modül, stok planlama ve haftalık değişim raporlarını içerir.
        Kullanıcılar için özelleştirilmiş filtreler sunar.
    """,
    'author': 'Berat Seçgin',
    'website': 'https://github.com/beratsecgin/stok_planlama',
    'category': 'Warehouse Management',
    'depends': ['base', 'stock', 'sale_management', 'purchase'],
    'data': [
        'views/haftalik_degisim_raporu_views.xml',
        'views/stok_planlama_menu.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
