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
            'mute':False,
        }
        for k, v in default_config.iteritems():
            if config is None or not config.has_key(k):
                self[k] = v
            else:
                self[k] = config[k]
