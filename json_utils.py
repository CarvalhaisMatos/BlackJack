from game import Game
from player import Player

def object_to_dict(obj):
    print obj
    d = { '__class__':obj.__class__.__name__, 
          '__module__':obj.__module__,
        }
    d.update(obj.__dict__)
    if d['__class__'] == 'ProxyPlayer':
        d.pop('socket')
    return d


def dict_to_object(d):
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
#        print 'MODULE:', module
        if class_name in ['Rules', 'PlayerState']:
            class_base = getattr(module, "Game")
            class_ = getattr(class_base, class_name)
        elif class_name == 'ProxyPlayer':
            module = __import__('player')
            class_ = getattr(module, 'Player')
        else:
            class_ = getattr(module, class_name)

#        print 'CLASS:', class_
        args = dict( (key.encode('ascii'), value) for key, value in d.items())
        print 'INSTANCE ARGS:', args
        inst = class_(**args)
    else:
        inst = d
    return inst
