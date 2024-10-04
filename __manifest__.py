{
    'name': 'Manajemen Ruangan',
    'version': '1.0',
    'author': "Junizar Fajri",
    'website': "https://www.yourcompany.com",
    'category': 'Tools',
    'summary': 'Modul untuk manajemen master ruangan dan pemesanan ruangan.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/master_ruangan_views.xml',
        'views/pemesanan_ruangan_views.xml',
        'data/sequence_data.xml',
    ],
    'installable': True,
    'application': True,
}

