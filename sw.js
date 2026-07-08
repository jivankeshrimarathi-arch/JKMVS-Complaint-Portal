const CACHE_NAME = 'jkmvs-cache-v3';
const SHELL_FILES = [
  'index.html',
  'vidyarthi-manch.html',
  'vidyarthi-nama.html',
  'manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_FILES)).catch(()=>{})
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Network-first for EVERYTHING now (except third-party APIs we never cache).
// This means the browser always tries to fetch the latest file first;
// the cache is only used as a fallback if there's no internet connection.
self.addEventListener('fetch', (e) => {
  const url = e.request.url;
  if (url.includes('script.google.com') || url.includes('ipify.org') || url.includes('cloudinary.com') || url.includes('googleapis.com') || url.includes('firebaseapp.com') || url.includes('gstatic.com')) {
    e.respondWith(fetch(e.request));
    return;
  }
  e.respondWith(
    fetch(e.request).then((resp) => {
      if (e.request.method === 'GET' && resp.ok) {
        const clone = resp.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
      }
      return resp;
    }).catch(() => caches.match(e.request))
  );
});
