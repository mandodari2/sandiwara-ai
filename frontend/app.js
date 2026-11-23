// Sandiwara AI — frontend logic (no build step).

let currentStory = null;

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

function showTab(name) {
  document.getElementById('view-library').classList.toggle('hidden', name !== 'library');
  document.getElementById('view-create').classList.toggle('hidden', name !== 'create');
  document.getElementById('tab-library').classList.toggle('active', name === 'library');
  document.getElementById('tab-create').classList.toggle('active', name === 'create');
}

async function loadStories() {
  const box = document.getElementById('story-list');
  try {
    const data = await api('/api/stories');
    if (!data.stories.length) {
      box.innerHTML = '<p>Belum ada cerita. Buat drama pertamamu!</p>';
      return;
    }
    box.innerHTML = data.stories.map(s => `
      <div class="story-card" onclick="openStory('${s.id}')">
        <h3>${escapeHtml(s.title)}</h3>
        <p>${escapeHtml(s.synopsis)}</p>
        <div class="meta">${escapeHtml(s.genre)} · ${s.episode_count} episode · ${s.characters.map(escapeHtml).join(', ')}</div>
      </div>`).join('');
  } catch (e) {
    box.innerHTML = `<p>Gagal memuat cerita: ${escapeHtml(e.message)}</p>`;
  }
}

async function openStory(id) {
  try {
    const story = await api(`/api/stories/${id}`);
    currentStory = story;
    document.getElementById('story-list').classList.add('hidden');
    document.getElementById('episode-view').classList.remove('hidden');
    document.getElementById('ep-title').textContent = story.title;
    document.getElementById('ep-synopsis').textContent = story.synopsis;
    const list = document.getElementById('ep-list');
    list.innerHTML = (story.episodes || []).map(ep => `
      <div class="episode">
        <h4>${escapeHtml(ep.title)}</h4>
        <button onclick="playEpisode('${story.id}', '${ep.id}', '${escapeHtml(ep.title)}')">▶ Putar</button>
        ${ep.audio_url ? `<a href="${ep.audio_url}" download><button>⬇ Unduh</button></a>` : '<span> (audio belum dibuat)</span>'}
      </div>`).join('');
  } catch (e) {
    alert('Gagal membuka cerita: ' + e.message);
  }
}

function backToLibrary() {
  document.getElementById('episode-view').classList.add('hidden');
  document.getElementById('story-list').classList.remove('hidden');
  document.getElementById('player').classList.add('hidden');
  loadStories();
}

async function playEpisode(storyId, episodeId, title) {
  // Fetch the story to get the script for display.
  const story = currentStory || await api(`/api/stories/${storyId}`);
  const ep = (story.episodes || []).find(e => e.id === episodeId);
  const player = document.getElementById('player');
  document.getElementById('player-title').textContent = `${story.title} — ${title}`;
  const audio = document.getElementById('audio');
  audio.src = ep.audio_url || `/api/episodes/${episodeId}/audio`;
  const scriptBox = document.getElementById('player-script');
  if (ep.script) {
    scriptBox.innerHTML = ep.script.scenes.map(sc => `
      <div class="scene">— ${escapeHtml(sc.location)} (${escapeHtml(sc.mood)}) —</div>
      ${sc.lines.map(l => `<div class="line"><span class="speaker">${escapeHtml(l.speaker)}:</span> ${escapeHtml(l.text)}</div>`).join('')}
    `).join('');
  } else {
    scriptBox.innerHTML = '';
  }
  player.classList.remove('hidden');
  player.scrollIntoView({ behavior: 'smooth' });
  audio.play().catch(() => {});
}

async function generateDrama(event) {
  event.preventDefault();
  const btn = document.getElementById('gen-btn');
  const status = document.getElementById('gen-status');
  const result = document.getElementById('gen-result');
  btn.disabled = true;
  status.textContent = '🎙️ Menulis naskah... merekam suara... mencampur audio... (bisa 1-2 menit)';
  result.classList.add('hidden');
  try {
    const data = await api('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: document.getElementById('f-title').value,
        synopsis: document.getElementById('f-synopsis').value,
        genre: document.getElementById('f-genre').value,
      }),
    });
    status.textContent = '✅ Drama selesai!';
    result.classList.remove('hidden');
    result.innerHTML = `
      <div class="episode">
        <h4>${escapeHtml(data.title)}</h4>
        <p>Tokoh: ${data.speakers.map(escapeHtml).join(', ')}</p>
        <button onclick="playGenerated('${data.story_id}', '${data.episode_id}', '${escapeHtml(data.title)}')">▶ Putar</button>
        <a href="${data.audio_url}" download><button>⬇ Unduh</button></a>
      </div>`;
  } catch (e) {
    status.textContent = '❌ Gagal: ' + e.message;
  } finally {
    btn.disabled = false;
  }
}

async function playGenerated(storyId, episodeId, title) {
  const story = await api(`/api/stories/${storyId}`);
  currentStory = story;
  playEpisode(storyId, episodeId, title);
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

loadStories();
