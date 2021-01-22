import sys
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

print("\n======================")
print("Tekton Jinja Template processing")

jjv_prefix = os.environ.get('TEKTON_JINJA_PREFIX') or 'jjv_'
print("using env var prefix = {pf}".format(pf=jjv_prefix))

tmpldir = os.environ['TEKTON_JINJA_TEMPLATE_DIR']
rndrdir = os.environ['TEKTON_JINJA_RENDERED_DIR']

def load_vars_from_env():
    jjv = {}
    for k, v in os.environ.items():
        if k.startswith(jjv_prefix):
            jjv[k[len(jjv_prefix):]] = v
    return jjv

print("loading jinja variables from environment vars...")
jjv = load_vars_from_env()

print("using jinja variables:")
print("======================")
for k, v in jjv.items():
    print("{k} = '{v}'".format(k=k, v=v))
print("======================")

print("initializing jinja environment ...")
print("template directory: {d}".format(d=tmpldir))
env = Environment( \
        loader=FileSystemLoader(tmpldir), \
        autoescape=select_autoescape(['html', 'xml']) \
    )

for tname in sys.argv[1:]:
    print("loading {t}...".format(t=tname))
    tmpl = env.get_template(tname)
    print("rendering {t}...".format(t=tname))
    tren = tmpl.render(jjv)
    print("rendered result:")
    print("======================")
    print(tren)
    print("======================")
    rfname = rndrdir + '/' + tname
    print("writing result to file {fname}".format(fname=rfname))
    with open(rfname, "w") as rfile:
        rfile.write(tren)
        # jinja seems to be stripping last newline?
        if tren[-1] != '\n':
            rfile.write("\n")
