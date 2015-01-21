"""
This file generates the markdown to be inserted into the README.
"""

import inspect
import kounta.objects

def get_return_type(doc):
    if not doc:
        return None

    lines = map(str.strip, doc.split('\n'))
    for line in lines:
        if ':return' in line or ':rtype' in line:
            return line[8:].strip()

    return None

def get_description(doc):
    if not doc:
        return None

    lines = map(str.strip, doc.split('\n'))
    r = []
    for line in lines:
        if ':return' not in line and ':rtype' not in line:
            r.append(line.strip())

    return ' '.join(r).strip()

for name, obj in inspect.getmembers(kounta.objects):
    if inspect.isclass(obj):
        name = str(obj)
        if name == 'kounta.objects.BaseObject':
            continue
        print '### %s' % name[15:]
        if obj.__doc__ is not None:
            print '\n'.join(map(str.strip, obj.__doc__.split('\n')))

        for property_name, property in vars(obj).iteritems():
            if property_name[0] == '_':
                continue
            desc = get_description(property.__doc__)
            print ' * `%s` (%s)%s%s' % (
                property_name,
                get_return_type(property.__doc__).replace('[', '\[').replace(']', '\]'),
                ': ' if desc else '',
                desc,
            )
        print
