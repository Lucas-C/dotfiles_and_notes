#!/usr/bin/env python2.7
# Blog post: https://chezsoi.org/lucas/blog/2015/04/19/en-django-tips/
# Initial idea from http://stackoverflow.com/a/1843657/636849
import os, django, errno, glob, sys
from StringIO import StringIO
from colorama import Fore, Style
from django.core.handlers.wsgi import WSGIRequest
from django.template import RequestContext
from django.template.loader import get_template
from django.template.base import VariableNode
from django.template.defaulttags import ForNode
from django.template.loader_tags import ExtendsNode, IncludeNode
from tplt_test_context import get_context_dict, DJANGO_SETTINGS_MODULE

class MissingVariableDefinition(Exception): pass

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    django.setup()
    tplt_context = build_tplt_context()
    template_files = list_html_files_relpaths(dirs=glob.glob('*/templates/'))
    dst_dump_dir = 'rendered_templates/'
    mkdir_p(dst_dump_dir)
    exit_code = 0
    for tplt_file in template_files:
        try:
            render_and_dump_template(tplt_file, tplt_context, dst_dump_dir)
        except MissingVariableDefinition:
            exit_code = 1
    sys.exit(exit_code)

def build_tplt_context():
    dummy_request = WSGIRequest({
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/',
            'wsgi.input': StringIO()})
    tplt_context = RequestContext(dummy_request)
    tplt_context.update(get_context_dict())
    return tplt_context

def list_html_files_relpaths(dirs):
    html_files = []
    cur_dir = os.getcwd()
    for dirname in dirs:
        os.chdir(dirname)
        html_files.extend(glob.glob('*.html'))
        os.chdir(cur_dir)
    return html_files

def render_and_dump_template(tplt_file, tplt_context, dst_dump_dir):
    template = get_template(tplt_file)
    required_vars = extract_required_vars(template)
    required_vars_basenames = list(set(v.split('|')[0].split('.')[0] for v in required_vars))
    print_template_description(template.origin.name, required_vars_basenames, tplt_context)
    output = template.render(tplt_context)
    with open(os.path.join(dst_dump_dir, tplt_file), 'w') as outfile:
        print >>outfile, output.encode('utf8', 'replace')

def extract_required_vars(node):
    if not hasattr(node, 'nodelist'):
        return []
    var_names = []
    for child_node in node.nodelist:
        if isinstance(child_node, VariableNode):
            var_names.append(child_node.filter_expression.token)
        elif isinstance(child_node, ForNode):
            var_names.append(child_node.sequence.var.var)
        elif isinstance(child_node, ExtendsNode):
            template = get_template(child_node.parent_name.var)
            var_names.extend(extract_required_vars(template))
        elif isinstance(child_node, IncludeNode):
            template = get_template(child_node.template.var)
            var_names.extend(extract_required_vars(template))
        var_names.extend(extract_required_vars(child_node))
    return var_names

def print_template_description(tplt_filepath, required_vars, defined_vars):
    defined_vars = [var for var in required_vars if var in defined_vars]
    missing_vars = [var for var in required_vars if var not in defined_vars]
    print tplt_filepath
    if defined_vars:
        print Fore.GREEN, ' -> ok:', ', '.join(defined_vars), Style.RESET_ALL
    if missing_vars:
        print Fore.RED, ' -> missing:', ', '.join(missing_vars), Style.RESET_ALL
        raise MissingVariableDefinition

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise

if __name__ == '__main__':
    main()
