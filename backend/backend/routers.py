from accounts import models as acc_models

allmodels = dict([(name.lower(), cls) for name,
                  cls in acc_models.__dict__.items() if isinstance(cls, type)])


class SQLRouter(object):
    db = ['sqldb', 'default']

    def db_for_read(self, model, **hints):
        if hasattr(model, 'params'):
            if model.params.db in self.db:
                return self.db[0]
            return None
        return self.db[0]

    def db_for_write(self, model, **hints):
        if hasattr(model, 'params'):
            if model.params.db in self.db:
                return self.db[0]
            return None
        return self.db[0]

    def allow_relation(self, obj1, obj2, **hints):
        if hasattr(obj1, 'params') or hasattr(obj2, 'params'):
            if hasattr(obj1, 'params') and obj1.params.db == 'mongodb':
                return None
            if hasattr(obj2, 'params') and obj2.params.db == 'mongodb':
                return None
            return True
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        model = allmodels.get(model_name)
        if db in self.db:
            if model and hasattr(model, 'params'):
                if model.params.db in self.db:
                    return True
                return False
            return True
        else:
            return None


class MongoRouter(object):
    db = 'mongodb'

    def db_for_read(self, model, **hints):
        if hasattr(model, 'params'):
            if model.params.db == self.db:
                return self.db
            return None
        return None

    def db_for_write(self, model, **hints):
        if hasattr(model, 'params'):
            if model.params.db == self.db:
                return self.db
            return None
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if hasattr(obj1, 'params') or hasattr(obj2, 'params'):
            if hasattr(obj1, 'params') and obj1.params.db == self.db:
                return True
            if hasattr(obj2, 'params') and obj2.params.db == self.db:
                return True
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        model = allmodels.get(model_name)
        if db == self.db:
            if hasattr(model, 'params'):
                if model.params.db == self.db:
                    return True
                return False
            return False
        else:
            return None
