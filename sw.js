/* JKMVS PWA service worker — नेटवर्क-प्रथम; ऑफलाइनसाठी cache + offline.html */
const CACHE_NAME = 'jkmvs-cache-v10';
const SHELL_FILES = ['index.html','join.html','pathyapustak-yojana.html','vidyarthi-sahayya.html','vidyarthi-manch.html','vidyarthi-nama.html',
  'press-releases.html','offline.html','press.css','pwa.js','manifest.json','icon-192.png','icon-512.png','apple-touch-icon.png'];
const PASS = /ibb\.co|wsrv\.nl|weserv\.nl|youtube\.com|youtu\.be|ytimg\.com|googlevideo\.com|instagram\.com|cdninstagram\.com|script\.google\.com|ipify\.org|cloudinary\.com|googleapis\.com|firebaseapp\.com|firebaseio\.com|gstatic\.com|google\.com|cdnjs\.cloudflare\.com|jsdelivr\.net/;

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((c) => Promise.allSettled(SHELL_FILES.map((f) => c.add(f)))).catch(() => {}));
  self.skipWaiting();
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || PASS.test(req.url)) return; // बाहेरील सेवा थेट ब्राउझरवर
  e.respondWith(
    fetch(req).then((resp) => {
      if (resp.ok && resp.type === 'basic') { const cl = resp.clone(); caches.open(CACHE_NAME).then((c) => c.put(req, cl)); }
      return resp;
    }).catch(() => caches.match(req).then((m) => m || (req.mode === 'navigate' ? caches.match('offline.html') : undefined)))
  );
});
