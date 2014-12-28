#!/usr/bin/env python
# Debug mod_swgi: grep -C3 proxy /var/log/apache2/ssl_error.log | tail -n 100
import cgi, cStringIO, os, traceback

def pop_form(env):
    """Should be called only ONCE."""
    post_env = env.copy()
    post_env['QUERY_STRING'] = ''
    form = cgi.FieldStorage(
        fp = env['wsgi.input'],
        environ = post_env,
        keep_blank_values = True
    )
    return form

def application(env, start_response):
    # Recipe from https://code.google.com/p/modwsgi/wiki/DebuggingTechniques
    output = cStringIO.StringIO()
    print >> output, 'PID: {}\nUID: {}\nGID: {}\n'.format(os.getpid(), os.getuid(), os.getgid())
    for key in sorted(env.keys()):
        print >> output, '{}: {}'.format(key, repr(env[key]))
    print >> output, '\npath: "{}"'.format(env.get('PATH_INFO', ''))
    print >> output, 'method: {}'.format(env['REQUEST_METHOD'])
    print >> output, 'query_string: "{}"'.format(env['QUERY_STRING'])
    print >> output, 'form: {}'.format(pop_form(env))
    print >> output, '\nINPUT:\n'
    print >> output, env['wsgi.input'].read(int(env.get('CONTENT_LENGTH', '0')))
    write = start_response('200 OK', [('Content-Type', 'text/plain')])
    return [output.getvalue()]
