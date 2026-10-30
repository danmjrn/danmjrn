#!/usr/bin/env python3
"""Generate a bounded, honest card from public GitHub REST metadata only."""
import datetime,html,json,pathlib,urllib.request
request=urllib.request.Request('https://api.github.com/users/danmjrn/repos?type=owner&sort=updated&per_page=100',headers={'User-Agent':'danmjrn-public-profile','Accept':'application/vnd.github+json'})
with urllib.request.urlopen(request,timeout=20) as response: repos=json.load(response)
repos=[r for r in repos if not r.get('private') and not r.get('fork') and r['name']!='danmjrn']
updated=sorted(repos,key=lambda r:r['pushed_at'] or '',reverse=True)[:3]
stars=sum(r['stargazers_count'] for r in repos);languages=len({r['language'] for r in repos if r.get('language')})
now=datetime.datetime.now(datetime.timezone.utc).strftime('%d %b %Y · UTC')
parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 250" role="img"><title>Public repository activity — refreshed '+html.escape(now)+'</title><rect width="1000" height="250" rx="16" fill="#f1f1ef"/><g font-family="Arial,sans-serif" fill="#1c1d20"><text x="34" y="38" font-size="12" letter-spacing="2">PUBLIC GITHUB SNAPSHOT</text>']
for x,count,label in [(34,len(repos),'PUBLIC SOURCE REPOSITORIES'),(350,stars,'STARS ON PUBLIC REPOSITORIES'),(700,languages,'REPOSITORY LANGUAGES')]:
 parts.append(f'<text x="{x}" y="101" font-size="48" letter-spacing="-2">{count}</text><text x="{x}" y="126" font-size="9" letter-spacing=".6">{label}</text>')
parts.append('<path d="M34 150H966" stroke="#d0d2d4"/><text x="34" y="179" font-size="10">RECENTLY PUSHED</text>')
for i,r in enumerate(updated): parts.append(f'<text x="{34+i*315}" y="205" font-size="13">{html.escape(r["name"][:34])}</text>')
parts.append(f'<text x="34" y="231" font-size="9" fill="#626569">Refreshed {html.escape(now)} · Private work excluded</text></g></svg>')
pathlib.Path('assets/activity.svg').write_text(''.join(parts)+'\n')
print('Public activity card refreshed; no private data requested.')
