/* Tells a returning reader the scan has moved on since they last looked.
   Fires only on a minor or major bump (1.3.5 -> 1.4.0 speaks, 1.3.4 -> 1.3.5 stays quiet).
   First visit is silent: there is no "last time" to compare against. */
(function () {
  var KEY = 'ibc2026:lastSeenVersion';
  var SEMVER = /(\d+)\.(\d+)\.(\d+)/;

  var stamp = document.getElementById('version');
  if (!stamp) return;
  var cur = SEMVER.exec(stamp.textContent || '');
  if (!cur) return;

  // A quiet link to the notes, sitting on the version stamp itself. Done here rather than in the
  // markup because bump.py rewrites that whole paragraph on every version bump.
  if (!stamp.querySelector('a')) {
    var sep = document.createElement('span');
    sep.textContent = ' · ';
    var notes = document.createElement('a');
    notes.href = 'changes/';
    notes.textContent = 'release notes';
    notes.style.cssText = 'color:inherit;text-decoration:underline;text-underline-offset:2px';
    notes.addEventListener('mouseenter', function () { notes.style.color = '#B05708'; });
    notes.addEventListener('mouseleave', function () { notes.style.color = 'inherit'; });
    stamp.appendChild(sep);
    stamp.appendChild(notes);
  }

  var prev = null;
  try { prev = localStorage.getItem(KEY); } catch (e) { /* private mode, blocked storage */ }
  try { localStorage.setItem(KEY, cur[0]); } catch (e) { /* nothing to do */ }

  if (!prev || prev === cur[0]) return;
  var old = SEMVER.exec(prev);
  if (!old) return;

  var major = +cur[1] > +old[1];
  var minor = +cur[1] === +old[1] && +cur[2] > +old[2];
  if (!major && !minor) return;

  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var box = document.createElement('div');
  box.setAttribute('role', 'status');
  box.setAttribute('aria-live', 'polite');
  box.style.cssText = [
    'position:fixed', 'left:22px', 'bottom:22px', 'z-index:60', 'max-width:min(20rem,calc(100vw - 44px))',
    'box-sizing:border-box', 'display:flex', 'align-items:baseline', 'gap:10px',
    'background:#FDF0E2', 'border:1px solid #E7C9A6', 'border-radius:2px', 'padding:11px 13px',
    'box-shadow:0 3px 14px rgba(120,80,30,.16)', 'color:#1C1B19',
    'font-family:"Archivo Narrow",system-ui,sans-serif', 'font-size:13px', 'line-height:1.45',
    'opacity:0', 'transform:translateY(6px)',
    still ? 'transition:none' : 'transition:opacity .22s,transform .22s'
  ].join(';');

  var text = document.createElement('span');
  text.style.cssText = 'flex:1 1 auto';
  text.appendChild(document.createTextNode('Updated since you last looked. You were on v. ' + prev + ', this is v. ' + cur[0] + '. '));

  var link = document.createElement('a');
  link.href = 'changes/';
  link.textContent = 'What changed';
  link.style.cssText = 'color:#B05708;font-weight:700;text-decoration:underline;text-underline-offset:2px';
  text.appendChild(link);

  var close = document.createElement('button');
  close.type = 'button';
  close.setAttribute('aria-label', 'Dismiss');
  close.innerHTML = '&times;';
  close.style.cssText = 'flex:0 0 auto;background:none;border:0;padding:0 2px;cursor:pointer;' +
    'color:#8A6A4A;font-size:16px;line-height:1;font-family:inherit';

  box.appendChild(text);
  box.appendChild(close);
  document.body.appendChild(box);

  // Forcing layout gives the transition a starting point. requestAnimationFrame would not
  // run at all in a background tab, which left the notice sitting at zero opacity.
  void box.offsetHeight;
  box.style.opacity = '1';
  box.style.transform = 'none';

  var timer = setTimeout(hide, 12000);
  function hide() {
    clearTimeout(timer);
    box.style.opacity = '0';
    box.style.transform = 'translateY(6px)';
    setTimeout(function () { if (box.parentNode) box.parentNode.removeChild(box); }, still ? 0 : 260);
  }
  close.addEventListener('click', hide);
  link.addEventListener('click', function () { clearTimeout(timer); });
})();
