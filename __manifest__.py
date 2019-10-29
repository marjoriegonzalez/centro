# -*- coding: utf-8 -*-
{
    'name': "centro",

    'summary': """
        Aplicación web para Centro Medico""",

    'description': """
        Aplicacion web para el modulo de Desarrollo Web
    """,

    'author': "Marjorie Gonzalez, Javiera Bazaes,Jorge Meza",
    'website': "http://www.utalca.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Estudiante',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menus.xml',
        'views/templates.xml',
        #'views/paciente2.xml',
        'views/paciente3.xml',
        'views/paciente.xml',
        'views/reserva.xml',
        'views/especialidad.xml',
        'views/especialista.xml',
        'views/consulta.xml',
        'views/receta.xml',
        'views/agenda.xml',
        'views/agenda_especialista.xml',
        'reports/report_paciente.xml',
        'reports/report_reserva.xml',
        'reports/report_especialista.xml',
        'reports/report_receta.xml',
        'reports/report_especialidad.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}