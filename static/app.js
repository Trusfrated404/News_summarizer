const article = document.querySelector('#article');
const analyzeBtn = document.querySelector('#analyzeBtn');
const sampleBtn = document.querySelector('#sampleBtn');
const toast = document.querySelector('#toast');
const sample = `Global renewable energy investment reached a record $623 billion in 2025, according to a new report released on Tuesday by the International Energy Agency. Solar power accounted for almost half of the spending as lower equipment prices encouraged new projects across Asia and Europe. The report said the trend could help countries meet climate targets, but warned that investment in electrical grids has not kept pace. India announced plans to accelerate approvals for major transmission corridors, while several European governments committed new funds for battery storage. Analysts said the expansion is a positive sign for energy security, although supply-chain disruptions and higher borrowing costs remain a concern for smaller developers.`;
article.addEventListener('input', () => document.querySelector('#wordCounter').textContent = `${article.value.trim().split(/\s+/).filter(Boolean).length} words`);
sampleBtn.onclick = () => { article.value = sample; article.dispatchEvent(new Event('input')); };
function showToast(message) { toast.textContent = message; toast.classList.add('show'); setTimeout(() => toast.classList.remove('show'), 2800); }
function tags(id, items) { document.querySelector(id).innerHTML = items.length ? items.map(x => `<span>${x}</span>`).join('') : '<em>None detected</em>'; }
analyzeBtn.onclick = async () => {
  if (article.value.trim().length < 80) return showToast('Please add a longer news article.');
  analyzeBtn.disabled = true; analyzeBtn.innerHTML = 'Analyzing…';
  try {
    const res = await fetch('/api/analyze', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({article:article.value})});
    const data = await res.json(); if (!res.ok) throw new Error(data.error);
    document.querySelector('#emptyState').hidden = true; document.querySelector('#results').hidden = false;
    document.querySelector('#summary').textContent = data.summary;
    document.querySelector('#sourceBadge').textContent = data.summary_source;
    document.querySelector('#sentiment').textContent = data.sentiment.label;
    document.querySelector('#sentimentDetail').textContent = `${data.sentiment.score}% signal strength`;
    document.querySelector('#readingTime').textContent = `${data.reading_time} min`;
    document.querySelector('#wordCount').textContent = `${data.word_count} words`;
    tags('#keywords', data.keywords); tags('#entities', data.entities);
    document.querySelector('#results').scrollIntoView({behavior:'smooth', block:'start'});
  } catch (e) { showToast(e.message || 'Something went wrong.'); }
  finally { analyzeBtn.disabled = false; analyzeBtn.innerHTML = 'Analyze article <span>→</span>'; }
};
document.querySelector('#askBtn').onclick = async () => {
  const question = document.querySelector('#question').value.trim(); if (!question) return showToast('Type a question first.');
  const btn = document.querySelector('#askBtn'); btn.disabled = true; btn.textContent = '…';
  try { const res = await fetch('/api/ask', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({article:article.value,question})}); const data = await res.json(); if(!res.ok) throw new Error(data.error); const answer=document.querySelector('#answer'); answer.hidden=false; answer.textContent=data.answer; } catch(e) {showToast(e.message);} finally {btn.disabled=false;btn.textContent='Ask';}
};
