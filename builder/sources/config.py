from os import path

class AseConfig(dict):
    def __init__(self, config=None, basedir=None):
        if basedir is None:
            basedir = __file__
            for x in xrange(3):
                basedir = path.dirname(basedir)
            basedir = path.abspath(basedir)
        default_config = {
            'questions_dir':path.join(basedir, 'text', 'questions'),
            'answers_dir':path.join(basedir, 'text', 'answers'),
            'html_dir':path.join(basedir, 'html'),
            'template_dir':path.join(basedir, 'builder', 'templates'),
            'definitions_file':path.join(basedir, 'text', 'definitions.md'),
            'assets_dir':path.join(basedir, 'assets'),
            'assets':{
                'bootstrap':{
                    'url':'http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
                    'type':'css'
                },
                'jquery':{
                    'url':'http://code.jquery.com/jquery-2.1.0.min.js',
                    'type':'js'
                }
            },
            'mute':False,
        }
        for k, v in default_config.iteritems():
            if config is None or not config.has_key(k):
                self[k] = v
            else:
                self[k] = config[k]
