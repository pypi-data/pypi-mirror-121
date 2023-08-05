from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from .support import *
import datetime
import os
import json
import re

class BasicElement():
    if os.environ.get('D20_ORM_CONF') != None:
        conf = json.loads(os.environ.get('D20_ORM_CONF'))
        arangoURL=conf.get('D20_ORM_DBURL')
        username=conf.get('D20_ORM_DBUSERNAME')
        password=conf.get('D20_ORM_DBPASSWORD')        
    else:
        print(message="No configuration given, cannot start.")
        raise Exception

    db_client = Connection(arangoURL=arangoURL, username=username, password=password, verify=True, verbose=True, statsdClient=None, reportFileName=None, loadBalancing='round-robin', use_grequests=False, use_jwt_authentication=False, use_lock_for_reseting_jwt=True, max_retries=10)
    db_name = ''
    cascade = False
    @classmethod
    def search_attributes(cls):
        return []

    @classmethod
    def get_collection(cls):
        return None

    @classmethod
    def getAll(cls):
        return None

    def auth(self):
        return False
    
    def isEdge(self):
        return False

    def vertex(self):
        return {'_from': '', '_to': ''}

    def cascade_delete(self):
        return False

    def cascade_update(self):
        return False

    def cascade_create(self):
        return False

    def create(self):
        try:
            self.date_created= datetime.datetime.utcnow()
            self.date_updated = self.date_created
            self.deleted = self.get('deleted', False)
            if self.deleted == None:
                self.deleted = False
            to_insert = self.to_dict()
            for key in self.attributes:
                if key in to_insert and to_insert[key] == None:
                    to_insert.pop(key)
            if self.isEdge() == True:
                from_to = self.vertex()
                if self.get('_to') != None:
                    to_insert['_to'] = f'{from_to["_to"]}/{self.get("_to")}'
                if self.get('_from') != None:
                    to_insert['_from'] = f'{from_to["_from"]}/{self.get("_from")}'
            ins_obj = self.db[self.get_collection()].createDocument(to_insert)
            ins_obj.save()
            self._key = ins_obj._key
            if self.cascade == True:
                try:
                    self.cascade_create()
                except:
                    pass
        except:
            ins_obj = None
            self.status = False
        self.status = ins_obj != None

    def get_alias(self):
        return self.get('_key')

    def wipe(self):
        try:
            del_obj = self.db[self.get_collection()].fetchDocument(self._key)
            del_obj.delete()
            self.status = del_obj._key == None
        except:
            self.status = False
        self._key = None

    def delete(self):
        try:
            self.deleted = True
            self.active = False
            self.status = self.update()
            if self.cascade == True:
                try:
                    self.cascade_delete()
                except:
                    pass
        except:
            self.status = False
        self._key = None

    def find(self):
        try:
            found = self.db[self.get_collection()].fetchDocument(self._key)
            if found['deleted'] == True:
                found = None
            for key in self.attributes:
                setattr(self, key, found.getStore()[key] if key in found.getStore() else self.get(key))
            if '_to' in self.attributes:
                self._to = self.get('_to').split("/")[1]
            if '_from' in self.attributes:
                self._from = self.get('_from').split("/")[1]
            self.status = True
        except:
            self._key = None
            self.status = False

    def findGraph(self, query):
        search_query = []
        for k in query:
            if isinstance(query[k], str):
                # if type(query[k]) is not unicode:
                #     query[k] = unicode(query[k], encoding='utf-8')

                query[k] = re.sub("[àáâãäå]", 'a', query[k])
                query[k] = re.sub("[èéêë]", 'e', query[k])
                query[k] = re.sub("[ìíîï]", 'i', query[k])
                query[k] = re.sub("[òóôõö]", 'o', query[k])
                query[k] = re.sub("[ùúûü]", 'u', query[k])
                query[k] = re.sub("[ýÿ]", 'y', query[k])
                query[k] = query[k] + '$'
                search_query.append({'dim': k, 'op': '=~', 'val': query[k]})
            else:
                search_query.append({'dim': k, 'op': '==', 'val': query[k]})
        self.search(search_query)

    def search(self, query, limit=None):
        try:
        # qf = ' and '.join([ f'Regex_Test(m.`{att["dim"]}`,"{att["val"]}", true)' if isinstance(att['val'], str) else f'm.`{att["dim"]}` == {att["val"]}' for att in query])
            qf = ' and '.join([ f'Regex_Test(m.`{att["dim"]}`,"{att["val"]}", true)' if isinstance(att['val'], str) else f'm.`{att["dim"]}` {att["op"]} {att["val"]}' for att in query])
            if limit != None:
                qf = qf + ' limit ' + str(limit)
            query = 'for m in '+ self.get_collection() +'\
                    FILTER '+qf+'\
                    return DISTINCT m'
            self.found = self.db.AQLQuery(query, rawResults=True, batchSize=100)
            self.found = list(filter(lambda x: not 'deleted' in x or x['deleted'] != True, self.found))
            if '_to' in self.attributes:
                for x in self.found:
                    x['_to'] = x['_to'].split("/")[1]
                    x['_from'] = x['_from'].split("/")[1]
            if 'password' in self.attributes:
                for x in self.found:
                    x['password'] = ''
            self.status = True
            if self.found == None:
                self.found = []
        except:
            self._key = None
            self.status = False
            self.found = []

    def get(self, att, default=None):
        res = getattr(self, att, default)
        if res == None:
            return default
        return res

    def get_class(self):
        return 'BasicElement'

    def get_distinct_elements(self, dims=['_key']):
        d = ', '.join([f'{dim} = doc.{dim}' for dim in dims])
        ds = '{' + ', '.join([f'{dim}' for dim in dims]) + '}'
        filter = ' and '.join([ f'm.{att} == "{self.get(att)}"' if isinstance(self.get(att), str) else f'm.{att} == {self.get(att)}' for att in self.get('attributes') if self.get(att) != None])
        query = f'FOR doc in {self.get_collection()} FILTER {filter} COLLECT {d} RETURN DISTINCT {ds}'
        self.delements = []
        [self.delements.append(e) for e in self.db.AQLQuery(query, rawResults=True, batchSize=1000)]

    def make(self):
        self.attributes = ['_key']
        for key in self.attributes:
            setattr(self, key, None)

    def do_publish(self, t):
        try:
            to_update = {'publish':t}
            update_obj = self.get_collection().fetchDocument(self._key)
            before = update_obj['_rev']
            update_obj.set(to_update)
            update_obj.patch()
            after = update_obj['_rev']
        except:
            return False
        return before != after

    def to_dict(self):
        res = {}
        for key in self.attributes:
            res[key] = self.get(key)
        return res

    def update(self):
        try:
            self.date_updated = datetime.datetime.utcnow()
            to_update = self.to_dict()
            try:
                to_update.pop('date_created')
            except:
                pass
            try:
                to_update.pop('user_created')
            except:
                pass
            for key in self.attributes:
                if key in to_update and (to_update[key] == None or re.search(r'^(obj_){1}\w+$', key) != None or re.search(r'^(alias_){1}\w+$', key) != None):
                    to_update.pop(key)
            update_obj = self.db[self.get_collection()].fetchDocument(self._key)
            before = update_obj['_rev']
            update_obj.set(to_update)
            update_obj.patch()
            after = update_obj['_rev']
            if self.cascade == True and before != after:
                try:
                    self.cascade_update()
                except:
                    pass
        except:
            return False
        return before != after

    def __init__(self, mode, data = None):
        # try:
        self.db = self.db_client[self.db_name]
        self.make()
        for key in self.attributes:
            setattr(self, key, data[key] if key in data else None)
        if mode == 'create': # OK
            self.status = self.create()
        elif mode == 'update': # OK
            self.status = self.update()
        elif mode == 'set': # OK
            self.status = True
        elif mode == 'find':  # OK
            self.find()
        elif mode == 'fetch':  # OK
            self.findGraph(data)
        elif mode == 'delete': # OK
            self.delete()
        elif mode == 'publish': # OK
            self.status = self.do_publish(data['publish'])
        elif mode == 'auth': # OK
            self.auth()
        elif mode == 'search': # OK
            self.search(data)
        elif mode == 'limited_search': # OK
            self.search(data.pop('query', None), data.pop('limit', None))
        # except:
        #     print("Unexpected error.")
        #     self._key = None
        #     self.status = False