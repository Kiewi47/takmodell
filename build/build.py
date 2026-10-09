#!/usr/bin/env python3
"""Bygger produktionsversionen av 3D-takmodellen till dist/.

- Inbäddade bilder (data:image) läggs som egna filer i img/ (WebP, namn efter innehållets hash),
  så att de bara hämtas när de visas och kan cachas länge.
- Three.js levereras från vendor/ i stället för extern CDN.
- .htaccess sätter cache: index.html alltid färsk, img/ och vendor/ cachas i ett år.
Användning: python3 build.py <src.html> <dist-katalog> <three-paketkatalog>
"""
import base64, hashlib, io, os, re, shutil, sys
from PIL import Image

src, dist, three = sys.argv[1], sys.argv[2], sys.argv[3]
html = open(src, encoding='utf-8').read()
if os.path.isdir(dist):
    shutil.rmtree(dist)
os.makedirs(os.path.join(dist, 'img'))

seen = {}
def ut(m):
    mime, data = m.group(1), m.group(2)
    raw = base64.b64decode(data)
    h = hashlib.sha1(raw).hexdigest()[:14]
    if h not in seen:
        try:
            im = Image.open(io.BytesIO(raw))
            im = im.convert('RGBA') if im.mode in ('P', 'LA', 'RGBA') else im.convert('RGB')
            b = io.BytesIO(); im.save(b, 'WEBP', quality=82, method=6); out = b.getvalue()
            name = f'{h}.webp'
            if len(out) >= len(raw):           # behåll originalet om WebP inte blir mindre
                name = f'{h}.{mime.replace("jpeg", "jpg")}'; out = raw
        except Exception:
            name = f'{h}.{mime}'; out = raw
        open(os.path.join(dist, 'img', name), 'wb').write(out)
        seen[h] = name
    return 'img/' + seen[h]

html = re.sub(r'data:image/([a-z+]+);base64,([A-Za-z0-9+/=]+)', lambda m: ut(m), html)

# Three.js lokalt
vt = os.path.join(dist, 'vendor', 'three-0.160.0')
for rel in ['build/three.module.min.js', 'examples/jsm/controls/OrbitControls.js',
            'examples/jsm/environments/RoomEnvironment.js', 'examples/jsm/utils/BufferGeometryUtils.js']:
    d = os.path.join(vt, rel); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy(os.path.join(three, rel), d)
old = '{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}'
assert old in html, 'importmap hittades inte'
html = html.replace(old, '{"imports":{"three":"./vendor/three-0.160.0/build/three.module.min.js","three/addons/":"./vendor/three-0.160.0/examples/jsm/"}}')
# Byggversion: butiksskärmar i kioskläge jämför mot version.json och laddar om när en ny version publicerats
import json as _json
bygge = hashlib.sha1(html.encode('utf-8')).hexdigest()[:12]
html = html.replace('<script type="importmap">', f'<script>window.TAK_BUILD="{bygge}";</script><script type="importmap">', 1)
open(os.path.join(dist, 'version.json'), 'w').write(_json.dumps({'build': bygge}))
open(os.path.join(dist, 'index.html'), 'w', encoding='utf-8').write(html)

open(os.path.join(dist, '.htaccess'), 'w').write("""# 3D-takmodellen – cache och komprimering
<IfModule mod_headers.c>
  <FilesMatch "\\.(html|json)$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
  # Modellen får bara bäddas in (iframe) på Taklagrets egna sidor och e-handelns förhandsvisningar
  Header always set Content-Security-Policy "frame-ancestors 'self' https://taklagret.se https://www.taklagret.se https://shop-sweet-connect.lovable.app https://id-preview--d896781a-8c55-4548-9be3-b7ad2811e3e5.lovable.app"
  <FilesMatch "\\.(webp|jpg|png|js)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html application/javascript text/javascript
</IfModule>
AddType application/javascript .js
AddType image/webp .webp
""")
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(dist) for f in fs)
print(f'index.html {os.path.getsize(os.path.join(dist, "index.html"))/1e3:.0f} kB, bilder {len(seen)} st, totalt {tot/1e6:.2f} MB')
