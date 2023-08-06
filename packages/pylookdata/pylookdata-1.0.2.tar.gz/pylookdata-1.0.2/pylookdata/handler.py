import sqlalchemy 
import json
import os.path
import hashlib
import time
import shutil
import urllib.parse


class Config:
    def __init__(self):
        self.myconfig = {}
        self.initialize = True
        self.config = {}
        self.dirs = 'out'
        self.path = self.dirs + '/config.json'
        self.load_config()
        self.drivers = {"mysql": ["mysql", "mysql+mysqldb", "mysql+pymysql"],
                        "postgresql": ["postgresql", "postgresql+psycopg2", "postgresql+pg8000"],
                        "oracle": ["oracle", "oracle+cx_oracle"],
                        "mssql": ["mssql+pyodbc", "mssql+pymssql"],
                        "sqlite": ["sqlite"]} 
        
    def load_config(self):
        try:
            with open(self.path, encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            if self.initialize:
                self.initialize = False
            else:
                print('<Config.class.load_config()> Error Loading file')
            
    def save_config(self, config):
        try:
            if not os.path.exists('out'):
                os.makedirs('out')
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(config, f)
                
            self.load_config()
        except:
            print('<Config.class.save_config()> Error Saving file')
            
    def new_instance(self, database: str, servername: str, host: str, schema: list, user: str, password: str, port: int):
        id_ = hashlib.sha256(bytes(str(time.time()),'utf-8')).hexdigest()
        try:
            self.config[database].update(
                                   {id_: 
                                     {'name': servername,
                                      'host': host,
                                      'user': user,
                                      'password': password,
                                      'schemas': schema,
                                      'port': port
                                      }
                                    })
        except:
            self.config[database] = {id_: 
                                     {'name': servername,
                                      'host': host,
                                      'user': user,
                                      'password': password,
                                      'schemas': schema,
                                      'port': port
                                      }
                                     }
        
    def _getkeys(self, schema):
        for k_db, db in self.config.items():
            for k_s, s in db.items():
                if schema in s['schemas']:
                    return {'database': k_db, 'key': k_s} 
    
    def get_config(self, schema):
        config = {}
        keys = self._getkeys(schema)
        drivers = self.drivers[keys['database']]
        config = self.config[keys['database']][keys['key']]
        config.update({'drivers': drivers})
        config['schemas'] = schema
        self.myconfig = config
        return self
        
    def add_schema(self, schema):
        ## Incoming
        pass
    
    def list_config(self):
        print(json.dumps(self.config, indent=4))
    
    def build_engine(self):
        c = self.myconfig
        for driver in c['drivers']:
            try:
                url = f"{driver}://{c['user']}:{urllib.parse.quote_plus(c['password'])}@{c['host']}:{c['port']}/{c['schemas']}"
                return sqlalchemy.create_engine(url)
            
            except ModuleNotFoundError:
                print(f'<{driver}> Module not found, please check your packages')
                
    def clear_config(self):
        self.config = {}
    
    def clear_myconfig(self):
        self.myconfig = {}
    
    def delete_config(self):
        shutil.rmtree(self.dirs)