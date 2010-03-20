import logging
from multiprocessing.reduction import reduce_connection
import pickle

from mopidy import settings as raw_settings

logger = logging.getLogger('mopidy')

def get_version():
    return u'0.1.dev'

def get_mpd_protocol_version():
    return u'0.16.0'

def get_class(name):
    module_name = name[:name.rindex('.')]
    class_name = name[name.rindex('.') + 1:]
    logger.info('Loading: %s from %s', class_name, module_name)
    module = __import__(module_name, globals(), locals(), [class_name], -1)
    class_object = getattr(module, class_name)
    return class_object

def pickle_connection(connection):
    return pickle.dumps(reduce_connection(connection))

def unpickle_connection(pickled_connection):
    # From http://stackoverflow.com/questions/1446004
    unpickled = pickle.loads(pickled_connection)
    func = unpickled[0]
    args = unpickled[1]
    return func(*args)

class SettingsError(Exception):
    pass

class Settings(object):
    def __getattr__(self, attr):
        if attr.isupper() and not hasattr(raw_settings, attr):
            raise SettingsError(u'Setting "%s" is not set.' % attr)
        value = getattr(raw_settings, attr)
        if type(value) != bool and not value:
            raise SettingsError(u'Setting "%s" is empty.' % attr)
        return value

settings = Settings()
