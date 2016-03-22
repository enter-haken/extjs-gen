#!/usr/bin/env python
import argparse
from tornado import template

from json import loads

import datetime

class StoreTemplateGenerator(object):
    '''
    generates ExtJs store
    '''

    @property
    def generated(self):
        '''
        gets the generated store
        '''
        return self.__generated

    def __init__(self, applicationName, modelName, autoload):

        rawTemplate = '''
Ext.define('{{ applicationName }}.store.{{ modelName }}', {
    extend: 'Ext.data.store',
    alias: 'store.{{ modelName.lower() }}'
    model: '{{ applicationName }}.model.{{ modelName }}'{% if autoload %},
    autoLoad: true {% end %}
});
        '''
        
        t = template.Template(rawTemplate)
        result = t.generate(applicationName = applicationName, 
                modelName = modelName,
                autoload = autoload)

        lines = str(result).split("\\n")[1:]

        self.__generated = "\n".join(lines[:-1])

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(description='''
        generate an extjs store
    ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    PARSER.add_argument('-n', '--applicationName', required=True, help='name of the extjs application')
    PARSER.add_argument('-m', '--modelName',required=True, help='name of the model, which is associated with the store.')
    PARSER.add_argument('-a', '--autoLoad', action='store_true', help='auto load store on creation')

    args = PARSER.parse_args()

    store = StoreTemplateGenerator(args.applicationName, args.modelName, args.autoLoad)
    print (store.generated)
