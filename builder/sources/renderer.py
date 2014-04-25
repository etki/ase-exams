import os
import re

class AseRenderer:
    template_cache = {}
    tag_pattern = re.compile(r'{(?:#.*?#|%.*?%|{.*?})}')
    include_pattern = re.compile(r"{%\s*include\s*'([\w-]+)'\s*%}")
    var_pattern = re.compile(r"{{\s*([\w-]+)\s*}}")
    def __init__(self, template_dir, ext='.tpl', global_args={}):
        self.template_dir = template_dir
        self.ext = ext
        self.global_args = global_args
        
    def add_global_args(self, args):
        self.global_args.update(args)
    
    def render(self, template, args=None):
        template = self._get_template(template)
        args = dict(self.global_args).update(args)
        
        tags = set(re.findall(self.tag_pattern, template))
        for tag in tags:
            if tag.startswith('{{'):
                match = self.var_pattern.match(tag)
                if match is not None and match.group(1) in args:
                    template = template.replace(tag, str(args[match.group(1)]))
            elif tag.startswith('{%'):
                match = self.include_pattern.match(tag)
                if match is not None:
                    inject = self.render(match.group(1), args)
                    template = template.replace(tag, inject)
            else:
                template = template.replace(tag, '')
        return template.strip()
    
    def _get_template(self, template):
        if not template.endswith(self.ext):
            template = template + self.ext
        path = os.path.join(self.template_dir, template)
        with open(path, 'r') as f:
            self.template_cache[path] = f.read()
            return self.template_cache[path]
