#!/usr/bin/env python
from tornado import template
import argparse

import urllib.request
from json import loads

import datetime

class ModelTemplateGenerator(object):
    '''
    generates ExtJs model from dictionary
    '''

    @property
    def generated(self):
        '''
        gets the generated model
        '''
        return self.__generated

    @staticmethod
    def get_ext_type(field):
        '''
        python to ext type mapping 
        '''

        if isinstance(field, int):
            return "integer"

        if isinstance(field, str):
            return "string"

        if isinstance(field, datetime.datetime):
            return "date"

        return "string"
    
    @staticmethod
    def get_field(field):
        return "{ name : {}, type: {}  }".format

    def __init__(self, dictionary, proxyRestPath, applicationName, modelName, idProperty = "_id", rootProperty = "data"):

        rawTemplate = '''
Ext.define('{{ applicationName }}.model.{{ modelName }}', {
    extend: 'Ext.data.Model',

    idProperty: '{{ idProperty }}',

    proxy: {
        type: 'rest',
        url: '{{ proxyRestPath }}',
        reader: {
            type: 'json',
            rootProperty: '{{ rootProperty }}'
        }
    fields: [{% for field in dictionary.keys() %}{
            name: '{{ field }}',
            type: '{{ get_ext_type(dictionary[field]) }}'
        },{% end %}]
    }
});
        '''
        
        t = template.Template(rawTemplate)
        result = t.generate(applicationName = applicationName, 
                modelName = modelName,
                proxyRestPath = proxyRestPath, 
                idProperty = idProperty, 
                get_ext_type = ModelTemplateGenerator.get_ext_type,
                rootProperty = rootProperty,
                dictionary = dictionary)

        result = str(result).replace("},]","}]")

        lines = result.split("\\n")[1:]

        self.__generated = "\n".join(lines[:-1])

def get_data(fetchUrl, root):
        raw = urllib.request.urlopen(fetchUrl).read().decode('utf-8')
        rawData = loads(raw)[root]
        return rawData[0] if isinstance(rawData, list) else rawData
 
if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(description='''
        generate an extjs model from a given rest endpoint
    ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    PARSER.add_argument('-n', '--applicationName', required=True, help='name of the extjs application')
    PARSER.add_argument('-m', '--modelName',required=True, help='name of the model, which is associated with the store.')
    PARSER.add_argument('-u', '--fetchUrl',required=True, help='fetch sample data for model generation')

    PARSER.add_argument('-p', '--proxyRestPath', required=True, help='rest path for the extjs proxy.')
    PARSER.add_argument('-i', '--idProperty', default='_id', help='id property of the model.')
    PARSER.add_argument('-r', '--rootProperty', default='data', help='root property of the http proxy.')

    args = PARSER.parse_args()

    model = ModelTemplateGenerator(get_data(args.fetchUrl ,args.rootProperty), args.proxyRestPath, args.applicationName, args.modelName, args.idProperty, args.rootProperty)
    print(model.generated)
