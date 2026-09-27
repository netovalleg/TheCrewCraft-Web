import hashlib, json, os, sys
from urllib.parse import quote

base = sys.argv[1].rstrip('/')
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)

tpl = open('tools/instances.template.json', encoding='utf8').read().replace('__BASE__', base)
instances = json.loads(tpl)
with open('instances', 'w', encoding='utf8') as f:
    json.dump(instances, f, ensure_ascii=False, indent=2)

for name in instances:
    folder = os.path.join('files', name)
    items = []
    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith('.'))
        for fn in sorted(filenames):
            if fn.startswith('.'):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, folder).replace(os.sep, '/')
            data = open(full, 'rb').read()
            items.append({
                'path': rel,
                'size': len(data),
                'hash': hashlib.sha1(data).hexdigest(),
                'url': f"{base}/{quote(os.path.relpath(full, '.').replace(os.sep, '/'))}",
            })
    with open(os.path.join('files', name + '.json'), 'w', encoding='utf8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f'{name}: {len(items)} archivos')
