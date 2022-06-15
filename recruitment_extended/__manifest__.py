# -*- coding: utf-8 -*-
{
    'name': 'Recruitment Extended',
    'summary': """Something about the App.""",
    'description': """
App Name
========
Something about the App.
    """,
    'version': '13.0.1.0',
    'author': 'Company Name',
    'website': 'http://www.company.com',
    'category': 'Tools',
    'sequence': 1,
    'depends': [
        'base',
        'web',
        'hr_recruitment',
    ],
    'data': [

        ## Security
        'security/ir.model.access.csv',
        
        
        ## View
        'views/employee_view.xml',
        'views/menus.xml',
    ],
    'qweb': [
        ## Template
        'static/src/xml/*.xml',
    ],
    'external_dependencies': {
        'python': [
            'werkzeug',
        ],
    },
    'icon': '/recruitment_extended/static/description/icon.png',
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0,
    'currency': 'EUR',
    'license': 'OPL-1',
    'contributors': [
        'Azharul Amin Mulla',
    ],
}
