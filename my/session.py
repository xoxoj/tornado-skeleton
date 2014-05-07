import uuid
import pickle
import os.path

class Session:

    def __init__(self):
        self.meta = None
        self.data = None
    
    def prepare(self, meta):
        self.meta = meta
        if not meta['id']:
            self.meta['is_fresh'] = True
            self.meta['id'] = self.generate_id()
            self.data = dict()
        else:
            # TODO check if session id valid
            self.meta['is_fresh'] = False
            self.load()
        
    def __getitem__(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None
    
    def __setitem__(self, name, val):
        self.data[name] = val
        self.save()
        
    def __len__(self):
        return len(self.data)
        
    def save(self):
        pass
        
    def load(self):
        pass
    
    def generate_id(self):
        return str(uuid.uuid1())
        
class FileSession(Session):

    def prepare(self, meta):
        super().prepare(meta)
        
    def file_path(self):
        return os.path.join(self.meta['save_path'], 'sess_{}'.format(self.meta['id']))
        
    def save(self):
        with open(self.file_path(), 'w+b') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            
    def load(self):
        path = self.file_path()
        if not os.path.isfile(path):
            self.data = dict() 
        else:
            with open(path, 'rb') as f:
                self.data = pickle.load(f)
        
class Mixin:    
    def session_prepare(self, config=None):
        meta = {
            'cookie_name': 'SESS',
            'storage': FileSession,
            'request_ip': self.request.remote_ip,
        }
        if config:
            meta.update(config)
        meta['id'] = self.get_secure_cookie(meta['cookie_name'], None)
        self.session = meta['storage']()
        self.session.prepare(meta)
        if meta['is_fresh']:
            self.set_secure_cookie(meta['cookie_name'], self.session.meta['id'])
            
    def session_regenerate(self):
        pass