// Očísluje ovládací prvky na stránce a vrátí jejich popis pro jazykový model.
// U každého prvku zobrazí malý štítek s číslem, abyste viděli, co agent "vidí".
() => {
  document.querySelectorAll('.agent-cislo').forEach(s => s.remove());
  const vyber = 'a, button, select, textarea, input:not([type=hidden])';
  const prvky = [...document.querySelectorAll(vyber)]
    .filter(e => e.offsetParent !== null);             // jen viditelné prvky
  return prvky.map((e, i) => {
    e.setAttribute('data-agent', i);
    const r = e.getBoundingClientRect();
    const stitek = document.createElement('span');
    stitek.className = 'agent-cislo';
    stitek.textContent = i;
    stitek.style.cssText =
      `position:absolute; left:${r.left + scrollX - 6}px; top:${r.top + scrollY - 9}px;` +
      'background:#000; color:#fff; font:bold 11px sans-serif; padding:0 4px;' +
      'border-radius:3px; z-index:9999';
    document.body.appendChild(stitek);
    const nazev = e.labels?.[0]?.innerText || e.placeholder ||
                  e.innerText.trim() || e.name;
    let hodnota = '';
    if (e.tagName === 'SELECT') {
      hodnota = ' (možnosti: ' + [...e.options].map(o => o.text).join(', ') + ')';
    } else if (e.tagName === 'INPUT') {
      hodnota = ` = '${e.value}'`;
    }
    return `[${i}] ${e.tagName.toLowerCase()} ${nazev}${hodnota}`.slice(0, 150);
  });
}
