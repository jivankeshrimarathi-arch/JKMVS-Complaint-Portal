/* JKMVS: service worker नोंदणी + "अ‍ॅप इन्स्टॉल करा" सूचना */
(function () {
  if ('serviceWorker' in navigator) addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  var dp = null, KEY = 'jk-install-hide';
  var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone;
  function hidden() { try { return Date.now() - Number(localStorage.getItem(KEY) || 0) < 7 * 864e5; } catch (e) { return false; } }
  function chip(msg, act) {
    if (standalone || hidden() || document.getElementById('jkChip')) return;
    var d = document.createElement('div'); d.id = 'jkChip';
    d.setAttribute('style', 'position:fixed;left:50%;transform:translateX(-50%);bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:9998;max-width:92vw;background:#5C0A0A;color:#fff;border-radius:30px;padding:.5rem .6rem .5rem 1rem;display:flex;gap:.6rem;align-items:center;box-shadow:0 8px 24px rgba(0,0,0,.3);font:600 14px/1.4 system-ui,sans-serif');
    d.innerHTML = '<span>' + msg + '</span>' + (act ? '<button style="background:#FFE08A;color:#5C0A0A;border:0;border-radius:20px;padding:.45rem .9rem;font-weight:800;cursor:pointer">इन्स्टॉल</button>' : '') + '<button aria-label="बंद करा" style="background:none;border:0;color:#fff;font-size:20px;cursor:pointer;padding:0 .4rem">×</button>';
    var b = d.querySelectorAll('button');
    if (act) b[0].onclick = act;
    b[b.length - 1].onclick = function () { try { localStorage.setItem(KEY, Date.now()); } catch (e) {} d.remove(); };
    document.body.appendChild(d);
  }
  function install() { if (!dp) return; dp.prompt(); dp.userChoice.finally(function () { dp = null; var c = document.getElementById('jkChip'); if (c) c.remove(); document.querySelectorAll('[data-install]').forEach(function (x) { x.hidden = true; }); }); }
  addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault(); dp = e;
    document.querySelectorAll('[data-install]').forEach(function (x) { x.hidden = false; x.onclick = install; });
    setTimeout(function () { chip('📲 JKMVS अ‍ॅप फोनवर इन्स्टॉल करा', install); }, 4000);
  });
  addEventListener('appinstalled', function () { dp = null; var c = document.getElementById('jkChip'); if (c) c.remove(); });
  if (/iphone|ipad|ipod/i.test(navigator.userAgent) && !standalone) setTimeout(function () { chip('iPhone: Safari मध्ये Share → “Add to Home Screen”'); }, 5000);
})();
