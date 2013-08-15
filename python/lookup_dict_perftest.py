import cProfile 
from immutable import freeze_dict

def init_dict(obj_count):
    d = {}
    for i in xrange(obj_count):
        d[i] = i
    return d

def lookup_dict(d, obj_count):
    for i in xrange(obj_count):
        d[i]

def init_classSlot(obj_count):
    slots = tuple("s%i"%i for i in xrange(obj_count))
    class Slot(object):
        __slots__ = slots
    sl = Slot()
    for attr in slots:
        setattr(sl, attr, attr)
    return sl

def lookup_classSlot(s, obj_count):
    for i in xrange(obj_count):
        getattr(s, "s%i"%i)

for obj_count in (100000, 1000000):
    print "Inserting {} integers".format(obj_count)
    d = init_dict(obj_count)
    print  "Measuring dict lookup perfs"
    cProfile.run("lookup_dict(d, %i)"%obj_count)
    sl = init_classSlot(obj_count)
    print  "Measuring 'Slot' class lookup perfs"
    cProfile.run("lookup_classSlot(sl, %i)"%obj_count)
    dp = type('',(),d).__dict__ 
    print  "Measuring dictproxy lookup perfs"
    cProfile.run("lookup_dict(dp, %i)"%obj_count)
    di = freeze_dict(d) 
    print  "Measuring frozen dict lookup perfs"
    cProfile.run("lookup_dict(di, %i)"%obj_count)

