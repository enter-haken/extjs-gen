extjs-gen
=========

The goal of the `extjs-gen` project is to provide console centric tools for extjs code generation

### generateModel

```
usage: generateModel.py [-h] -n APPLICATIONNAME -m MODELNAME -u FETCHURL -p
                        PROXYRESTPATH [-i IDPROPERTY] [-r ROOTPROPERTY]

generate an extjs model from a given rest endpoint

optional arguments:
  -h, --help            show this help message and exit
  -n APPLICATIONNAME, --applicationName APPLICATIONNAME
                        name of the extjs application (default: None)
  -m MODELNAME, --modelName MODELNAME
                        name of the model, which is associated with the store.
                        (default: None)
  -u FETCHURL, --fetchUrl FETCHURL
                        fetch sample data for model generation (default: None)
  -p PROXYRESTPATH, --proxyRestPath PROXYRESTPATH
                        rest path for the extjs proxy. (default: None)
  -i IDPROPERTY, --idProperty IDPROPERTY
                        id property of the model. (default: _id)
  -r ROOTPROPERTY, --rootProperty ROOTPROPERTY
                        root property of the http proxy. (default: data)
```

#### Example

Getting a [model](http://docs.sencha.com/extjs/6.0/6.0.1-classic/#!/api/Ext.data.Model) for a Flickr feed list


```
$ ./generateModel.py -u "https://api.flickr.com/services/feeds/photos_public.gne?format=json&nojsoncallback=true" -n FlickrViewer -m Photo -i link -r items -p /photos
Ext.define('FlickrViewer.model.Photo', {
    extend: 'Ext.data.Model',

    idProperty: 'link',

    proxy: {
        type: 'rest',
        url: '/photos',
        reader: {
            type: 'json',
            rootProperty: 'items'
        }
    fields: [{
            name: 'link',
            type: 'string'
        },{
            name: 'date_taken',
            type: 'string'
        },{
            name: 'author',
            type: 'string'
        },{
            name: 'published',
            type: 'string'
        },{
            name: 'tags',
            type: 'string'
        },{
            name: 'author_id',
            type: 'string'
        },{
            name: 'description',
            type: 'string'
        },{
            name: 'media',
            type: 'string'
        },{
            name: 'title',
            type: 'string'
        }]
    }
});
```

The corresponding [store](http://docs.sencha.com/extjs/6.0/6.0.1-classic/#!/api/Ext.data.Store) can be generated with

### generateStore

```
usage: generateStore.py [-h] -n APPLICATIONNAME -m MODELNAME [-a]

generate an extjs store

optional arguments:
  -h, --help            show this help message and exit
  -n APPLICATIONNAME, --applicationName APPLICATIONNAME
                        name of the extjs application (default: None)
  -m MODELNAME, --modelName MODELNAME
                        name of the model, which is associated with the store.
                        (default: None)
  -a, --autoLoad        auto load store on creation (default: False)
```

The store for the Flickr model can look like

```
./generateStore.py -n FlickrViewer -m Photo -a
Ext.define('FlickrViewer.store.Photo', {
    extend: 'Ext.data.store',
    alias: 'store.photo'
    model: 'FlickrViewer.model.Photo',
    autoLoad: true 
});
```

### coming soon 

Be able to generate more complex structures with [model associations](http://docs.sencha.com/extjs/6.0/6.0.1-classic/#!/api/Ext.data.schema.Association) for e.g. [Yahoo Weather Api](https://developer.yahoo.com/weather/).

### Contact

Jan Frederik Hake, <jan_hake@gmx.de>. [@enter_haken](https://twitter.com/enter_haken) on Twitter.
