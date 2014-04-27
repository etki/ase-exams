import os
import urllib2

class AseAssetizer:
    def __init__(self, assets_dir, assets_definitions):
        self.dir = assets_dir
        self.assets = assets_definitions

    def install_assets(self):
        for name, asset in self.assets.iteritems():
            filepath = self.get_path(name)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    f.write(urllib2.urlopen(asset['url']).read())
    
    def get(self, asset_name):
        path = self.get_path(asset_name)
        with open(path, 'r') as f:
            return f.read()
    
    def get_path(self, asset_name):
        filename = asset_name + '.' + self.assets[asset_name]['type']
        return os.path.join(self.dir, filename)