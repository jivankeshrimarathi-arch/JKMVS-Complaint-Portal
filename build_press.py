#!/usr/bin/env python3
"""python build_press.py  -> press-releases/*.html, press-releases.html, sitemap.xml, rss.xml, robots.txt, index.html (nav+homepage section)"""
import json,os,re,html,datetime,glob
E=html.escape
D=json.load(open('press-releases.json',encoding='utf-8'));SITE=D['siteUrl'].rstrip('/')
if os.path.exists('press-releases-export.json'):
    have={r['slug'] for r in D['releases']};D['releases']+= [r for r in json.load(open('press-releases-export.json',encoding='utf-8')) if r.get('slug') not in have]
R=sorted([r for r in D['releases'] if r.get('status')=='published'],key=lambda r:r['date'],reverse=True)
ORG='जीवन केशरी मराठी विद्यार्थी समूह, नाशिक';LOGO='https://i.ibb.co/SDR0DXqb/ei-1764843850590-removebg-preview.png'
FONT='<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Mukta:wght@400;500;700&display=swap" rel="stylesheet">'
def fd(d):
    y,m,dd=map(int,d.split('-'));M='जानेवारी फेब्रुवारी मार्च एप्रिल मे जून जुलै ऑगस्ट सप्टेंबर ऑक्टोबर नोव्हेंबर डिसेंबर'.split();return f'{dd} {M[m-1]} {y}'
def img(r):return r.get('featuredImage') or LOGO
def card(r,i=0,feat=False):
    new='<span class="badge">नवीन</span>' if i==0 else ''
    return f'''<article class="card{' feat' if feat else ''}" data-slug="{E(r['slug'])}" data-t="{E((r['title']+' '+r['excerpt']+' '+' '.join(r.get('tags',[]))).lower())}" data-c="{E(r['category'])}" data-y="{r['date'][:4]}" data-m="{r['date'][5:7]}" data-d="{r['date']}"><img src="{E(img(r))}" alt="{E(r['title'])}" loading="{'eager' if feat else 'lazy'}"><div class="b"><div><span class="cat">{E(r['category'])}</span>{new}</div><div class="meta"><time datetime="{r['date']}">{fd(r['date'])}</time></div><h3><a href="/press-releases/{r['slug']}.html" style="text-decoration:none;color:inherit">{E(r['title'])}</a></h3><p>{E(r['excerpt'])}</p><a class="btn" href="/press-releases/{r['slug']}.html" style="align-self:flex-start;margin-top:auto">संपूर्ण प्रसिद्धीपत्रक वाचा →</a></div></article>'''
def page(title,desc,url,body,head=''):
    return f'''<!DOCTYPE html><html lang="mr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="alternate" type="application/rss+xml" href="{SITE}/rss.xml"><meta property="og:site_name" content="{ORG}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary_large_image">{FONT}<link rel="stylesheet" href="/press.css">{head}</head><body><header class="top"><div class="in"><a href="/"><img src="{LOGO}" alt="JKMVS लोगो">{ORG}</a><nav aria-label="मुख्य"><a href="/">मुखपृष्ठ</a> &nbsp; <a href="/press-releases.html">प्रेस रिलीज</a></nav></div></header>{body}<footer class="foot" style="text-align:center;padding:1.5rem;color:#6b5646">© २०२६ {ORG}</footer></body></html>'''
os.makedirs('press-releases',exist_ok=True)
for f in glob.glob('press-releases/*.html'):os.remove(f)
for r in R:
    url=f"{SITE}/press-releases/{r['slug']}.html";t=r.get('seoTitle') or r['title'];d=r.get('seoDescription') or r['excerpt']
    ld=json.dumps({"@context":"https://schema.org","@type":"NewsArticle","headline":r['title'][:110],"description":d,"image":[img(r)],"datePublished":r['date']+"T09:00:00+05:30","dateModified":r.get('modified',r['date'])+"T09:00:00+05:30","mainEntityOfPage":url,"author":{"@type":"Organization","name":r.get('author') or ORG},"publisher":{"@type":"Organization","name":ORG,"logo":{"@type":"ImageObject","url":LOGO}},"inLanguage":"mr","keywords":", ".join(r.get('tags',[]))},ensure_ascii=False)
    head=f'<meta property="og:type" content="article"><meta property="og:image" content="{E(img(r))}"><meta property="article:published_time" content="{r["date"]}"><meta name="twitter:image" content="{E(img(r))}"><script type="application/ld+json">{ld}</script><script src="/press-share.js" defer></script>'
    paras=''.join(f'<p>{E(p)}</p>' for p in r['content'].split('\n\n'))
    hl=f'<div class="hl"><h2 style="font-size:1.2rem">महत्त्वाचे मुद्दे</h2><ul>'+''.join(f'<li>{E(x)}</li>' for x in r.get('highlights',[]))+'</ul></div>' if r.get('highlights') else ''
    pdf=f'<a class="btn alt" href="{E(r["pdfUrl"])}" download><i></i>PDF डाउनलोड करा</a>' if r.get('pdfUrl') else ''
    ref=f' · संदर्भ क्र. {E(r["referenceNumber"])}' if r.get('referenceNumber') else ''
    msg=E(r['title']+'\n'+url).replace('\n','%0A')
    rel=[x for x in R if x is not r and x['category']==r['category']]+[x for x in R if x is not r and x['category']!=r['category']]
    relh=''.join(card(x,1) for x in rel[:4])
    body=f'''<main class="wrap"><article data-share-root data-title="{E(r['title'])}" data-url="{url}" data-date="{fd(r['date'])}" data-loc="{E(r.get('location',''))}" data-ref="{E(r.get('referenceNumber',''))}" data-excerpt="{E(r['excerpt'])}" data-text="{E(r['content'])}"><span class="cat">{E(r['category'])}</span><p class="meta"><time datetime="{r['date']}">{fd(r['date'])}</time> · {E(r.get('location',''))}{ref}</p><h1>{E(r['title'])}</h1><p class="sub">{E(r['excerpt'])}</p><img class="fi" src="{E(img(r))}" alt="{E(r['title'])}">{paras}{hl}<div class="acts">{pdf}</div><div id="shareHost"></div></article>{('<section class="rel" style="margin-top:2rem"><h2>हेही वाचा</h2><div class="grid">'+relh+'</div></section>') if relh else ''}</main>'''
    open(f"press-releases/{r['slug']}.html",'w',encoding='utf-8').write(page(t+' | JKMVS',d,url,body,head))
shell='''<main class="wrap"><div id="root"><p>लोड होत आहे…</p></div></main><script src="/press-live.js"></script><script src="/press-share.js" defer></script><script>(async()=>{const s=new URLSearchParams(location.search).get('s'),$=document.getElementById('root'),E=PL.E;
const nf=()=>{$.innerHTML='<p>हे प्रसिद्धीपत्रक आढळले नाही. <a href="/press-releases.html">सर्व प्रसिद्धीपत्रके</a></p>';document.head.insertAdjacentHTML('beforeend','<meta name="robots" content="noindex">')};
if(!s)return nf();let rs;try{rs=await PL.all()}catch(e){return nf()}const r=rs.find(x=>x.slug===s);if(!r)return nf();
const url=location.origin+'/press-release.html?s='+encodeURIComponent(s),img=r.featuredImage||PL.LOGO,d=r.seoDescription||r.excerpt;document.title=(r.seoTitle||r.title)+' | JKMVS';
const m=(k,v,a='name')=>{let e=document.head.querySelector('meta['+a+'="'+k+'"]');if(!e){e=document.createElement('meta');e.setAttribute(a,k);document.head.appendChild(e)}e.content=v};
m('description',d);m('og:title',r.title,'property');m('og:description',d,'property');m('og:image',img,'property');m('og:url',url,'property');m('og:type','article','property');m('twitter:image',img);
document.head.querySelector('link[rel=canonical]').href=url;
const ld=document.createElement('script');ld.type='application/ld+json';ld.textContent=JSON.stringify({'@context':'https://schema.org','@type':'NewsArticle',headline:r.title.slice(0,110),description:d,image:[img],datePublished:r.date+'T09:00:00+05:30',dateModified:(r.modified||r.date)+'T09:00:00+05:30',mainEntityOfPage:url,author:{'@type':'Organization',name:r.author||''},publisher:{'@type':'Organization',name:'जीवन केशरी मराठी विद्यार्थी समूह, नाशिक',logo:{'@type':'ImageObject',url:PL.LOGO}},inLanguage:'mr'});document.head.appendChild(ld);
const rel=rs.filter(x=>x.slug!==s).sort((a,b)=>(b.category===r.category)-(a.category===r.category)).slice(0,4);
$.innerHTML='<article data-share-root><span class="cat">'+E(r.category)+'</span><p class="meta"><time datetime="'+r.date+'">'+PL.fd(r.date)+'</time> · '+E(r.location||'')+(r.referenceNumber?' · संदर्भ क्र. '+E(r.referenceNumber):'')+'</p><h1>'+E(r.title)+'</h1><p class="sub">'+E(r.excerpt)+'</p>'+(r.featuredImage?'<img class="fi" src="'+E(img)+'" alt="'+E(r.title)+'">':'')+r.content.split(/\\n\\s*\\n/).map(p=>'<p>'+E(p)+'</p>').join('')+((r.highlights||[]).length?'<div class="hl"><h2 style="font-size:1.2rem">महत्त्वाचे मुद्दे</h2><ul>'+r.highlights.map(h=>'<li>'+E(h)+'</li>').join('')+'</ul></div>':'')+'<div class="acts">'+(r.pdfUrl?'<a class="btn alt" href="'+E(r.pdfUrl)+'" target="_blank" rel="noopener">PDF डाउनलोड करा</a>':'')+'</div><div id="shareHost"></div></article>'+(rel.length?'<section class="rel" style="margin-top:2rem"><h2>हेही वाचा</h2><div class="grid">'+rel.map(PL.card).join('')+'</div></section>':'');
const a=$.querySelector('article');Object.assign(a.dataset,{title:r.title,url,date:PL.fd(r.date),loc:r.location||'',ref:r.referenceNumber||'',excerpt:r.excerpt,text:r.content});if(window.PLShare)PLShare();else addEventListener('load',()=>window.PLShare&&PLShare())})()</script>'''
open('press-release.html','w',encoding='utf-8').write(page('प्रसिद्धीपत्रक | JKMVS नाशिक','जीवन केशरी मराठी विद्यार्थी समूह, नाशिक — प्रसिद्धीपत्रक',SITE+'/press-release.html',shell))
cats=sorted({r['category'] for r in R});yrs=sorted({r['date'][:4] for r in R},reverse=True)
M='जानेवारी फेब्रुवारी मार्च एप्रिल मे जून जुलै ऑगस्ट सप्टेंबर ऑक्टोबर नोव्हेंबर डिसेंबर'.split()
lst=f'''<main class="wrap"><h1>प्रेस रिलीज | प्रसिद्धीपत्रक</h1><p class="sub">{ORG} यांच्या उपक्रम, निवेदने, मागण्या, शैक्षणिक व सामाजिक कार्यासंदर्भातील अधिकृत प्रसिद्धीपत्रके.</p>
<div class="tools" role="search"><input id="q" type="search" placeholder="शोधा…" aria-label="शोधा"><select id="c" aria-label="श्रेणी"><option value="">सर्व श्रेणी</option>{''.join(f'<option>{E(c)}</option>' for c in cats)}</select><select id="y" aria-label="वर्ष"><option value="">सर्व वर्षे</option>{''.join(f'<option>{y}</option>' for y in yrs)}</select><select id="m" aria-label="महिना"><option value="">सर्व महिने</option>{''.join(f'<option value="{i+1:02d}">{n}</option>' for i,n in enumerate(M))}</select><select id="s" aria-label="क्रम"><option value="n">नवीन आधी</option><option value="o">जुने आधी</option></select></div>
<div class="grid" id="g">{''.join(card(r,i,i==0) for i,r in enumerate(R))}</div><p class="more"><button class="btn" id="mb">आणखी दाखवा</button></p><p id="none" hidden>कोणतेही प्रसिद्धीपत्रक आढळले नाही.</p></main>
<script>(()=>{{const g=document.getElementById('g'),$=i=>document.getElementById(i);let cs=[...g.children],n=9;window.plAdd=els=>{{els.forEach(e=>{{g.appendChild(e);cs.push(e)}});f()}};function f(){{const q=$('q').value.toLowerCase(),c=$('c').value,y=$('y').value,m=$('m').value,o=$('s').value=='o';cs.sort((a,b)=>o?a.dataset.d.localeCompare(b.dataset.d):b.dataset.d.localeCompare(a.dataset.d)).forEach(e=>g.appendChild(e));const v=cs.filter(e=>(!q||e.dataset.t.includes(q))&&(!c||e.dataset.c==c)&&(!y||e.dataset.y==y)&&(!m||e.dataset.m==m));cs.forEach(e=>{{e.hidden=true;e.classList.remove('feat')}});v.forEach((e,i)=>e.hidden=i>=n);$('mb').hidden=v.length<=n;$('none').hidden=v.length>0}}['q','c','y','m','s'].forEach(i=>$(i).addEventListener('input',()=>{{n=9;f()}}));$('mb').onclick=()=>{{n+=9;f()}};f()}})()</script><script src="/press-live.js"></script><script>PL.all().then(rs=>{{const have=new Set([...document.querySelectorAll('#g .card')].map(e=>e.dataset.slug)),t=document.createElement('div');t.innerHTML=rs.filter(r=>!have.has(r.slug)).map(PL.card).join('');plAdd([...t.children])}}).catch(()=>{{}})</script>'''
open('press-releases.html','w',encoding='utf-8').write(page('प्रेस रिलीज | प्रसिद्धीपत्रक | JKMVS नाशिक','जीवन केशरी मराठी विद्यार्थी समूह, नाशिक यांची अधिकृत प्रसिद्धीपत्रके.',SITE+'/press-releases.html',lst))
today=datetime.date.today().isoformat()
urls=[(SITE+'/',today),(SITE+'/press-releases.html',R[0]['date'] if R else today)]+[(f"{SITE}/press-releases/{r['slug']}.html",r.get('modified',r['date'])) for r in R]
open('sitemap.xml','w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc><lastmod>{d}</lastmod></url>' for u,d in urls)+'</urlset>')
open('robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /vidyarthi-nama-admin.html\nDisallow: /press-admin.html\nSitemap: {SITE}/sitemap.xml\n')
open('rss.xml','w',encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{ORG} — प्रेस रिलीज</title><link>{SITE}/press-releases.html</link><description>अधिकृत प्रसिद्धीपत्रके</description>'+''.join(f"<item><title>{E(r['title'])}</title><link>{SITE}/press-releases/{r['slug']}.html</link><guid>{SITE}/press-releases/{r['slug']}.html</guid><pubDate>{datetime.datetime.strptime(r['date'],'%Y-%m-%d').strftime('%a, %d %b %Y 09:00:00 +0530')}</pubDate><description>{E(r['excerpt'])}</description></item>" for r in R[:30])+'</channel></rss>')
# --- existing index.html: add nav item + homepage section (idempotent, nothing deleted)
if os.path.exists('index.html'):
    s=open('index.html',encoding='utf-8').read()
    s=re.sub(r'<!--PRESS-START-->.*?<!--PRESS-END-->','',s,flags=re.S)
    s=s.replace('<li><a href="press-releases.html">📣 प्रेस रिलीज</a></li>','').replace('<a href="press-releases.html" onclick="closeNav()">📣 प्रेस रिलीज</a>','')
    s=s.replace('<li><a href="#media">📰 माध्यमे</a></li>','<li><a href="#media">📰 माध्यमे</a></li>\n      <li><a href="press-releases.html">📣 प्रेस रिलीज</a></li>',1)
    s=s.replace('<a href="#media" onclick="closeNav()">📰 माध्यमे</a>','<a href="#media" onclick="closeNav()">📰 माध्यमे</a>\n  <a href="press-releases.html" onclick="closeNav()">📣 प्रेस रिलीज</a>',1)
    sec=f'<!--PRESS-START--><section id="press" style="padding:3rem 1rem;max-width:1100px;margin:auto"><link rel="stylesheet" href="press-home.css"><h2>प्रेस रिलीज | प्रसिद्धीपत्रक</h2><p class="sub">अधिकृत प्रसिद्धीपत्रके, निवेदने व मागण्या.</p><div class="grid">'+''.join(card(r,i,i==0) for i,r in enumerate(R[:4]))+'</div><p class="more"><a class="btn" href="press-releases.html">सर्व प्रसिद्धीपत्रके →</a></p></section><!--PRESS-END-->'
    s=s.replace('<footer>',sec+'\n<footer>',1);open('index.html','w',encoding='utf-8').write(s)

import base64
def emb(p):
    if not os.path.exists(p):return E(p)
    return 'data:image/'+('webp' if p.endswith('webp') else 'jpeg')+';base64,'+base64.b64encode(open(p,'rb').read()).decode()
# --- media clippings (media.json) -> index.html media grid
if os.path.exists('index.html') and os.path.exists('media.json'):
    s=open('index.html',encoding='utf-8').read()
    s=re.sub(r'<!--MEDIA-START-->.*?<!--MEDIA-END-->','',s,flags=re.S)
    mc=''.join(f'<div class="mcard rv"><div class="miwrap"><img src="{emb(x["image"])}" alt="{E(x["alt"])}" loading="lazy"><span class="mpbadge">{E(x["paper"])}</span></div><div class="mcb"><div class="mdate"><i class="fas fa-calendar-alt"></i>{E(x["date"])}</div><p>{E(x["text"])}</p></div></div>\n' for x in json.load(open('media.json',encoding='utf-8')))
    s=s.replace('<div class="mgrid">','<div class="mgrid"><!--MEDIA-START-->'+mc+'<!--MEDIA-END-->',1)
    open('index.html','w',encoding='utf-8').write(s)
# --- committee: college coordination (idempotent)
if os.path.exists('index.html'):
    s=open('index.html',encoding='utf-8').read()
    s=re.sub(r'<!--COORD-START-->.*?<!--COORD-END-->','',s,flags=re.S)
    blk='<!--COORD-START--><div class="dblock rv"><h3 class="dtitle"><i class="fas fa-university"></i> महाविद्यालय समन्वय विभाग</h3><div class="mgrs"><div class="mcard2"><div class="mavt">प्र</div><div class="mname">प्रथमेश संजय वानखेडे</div><div class="mrole">🔹 नाशिक शहर महाविद्यालय समन्वय प्रमुख</div></div></div></div><!--COORD-END-->'
    k='<div class="dblock rv">\n      <h3 class="dtitle"><i class="fas fa-users"></i> विद्यार्थी प्रतिनिधी</h3>'
    if k in s:s=s.replace(k,blk+'\n    '+k,1)
    s=s.replace('<p class="more"><a class="btn" href="press-releases.html">','<script defer src="press-live.js"></script><p class="more"><a class="btn" href="press-releases.html">',1) if 'press-live.js' not in s else s
    open('index.html','w',encoding='utf-8').write(s)
print(len(R),'releases built')
