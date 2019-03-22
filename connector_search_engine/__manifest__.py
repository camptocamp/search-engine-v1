# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Connector Search Engine',
    'version': '12.0.1.0.0',
    'author': 'Akretion,'
              'ACSONE SA/NV,'
              'Camptocamp,'
              'Odoo Community Association (OCA)',
    # FIXME
    'website': 'http://www.akretion.com',
    'license': 'AGPL-3',
    'category': 'Generic Modules',
    'depends': [
        'connector',
        'base_jsonify',
    ],
    'external_dependencies': {
        'python': ['unidecode'],
    },
    'data': [
        'views/se_backend.xml',
        'views/se_index.xml',
        'views/se_menu.xml',
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
