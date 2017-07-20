# -*- coding: utf-8 -*-

{
    'name': "TMC Document Index",
    'version': '10.0.1.0.0',
    'summary': 'Fields and functions for document indexing',
    'author': 'Tribunal Municipal de Cuentas - Municipalidad de Rosario',
    'website': 'https://www.tmcrosario.gob.ar',
    'license': 'AGPL-3',
    'sequence': 150,
    'depends': [
        'tmc',
        'tmc_data',
        'base_search_fuzzy'
    ],
    'data': [
        'data/trgm_index_data.xml',
        'views/document.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'qweb': [],
    'external_dependencies': {
        'python': ['textract']
    }
}
