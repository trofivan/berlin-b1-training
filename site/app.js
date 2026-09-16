const cards = [...document.querySelectorAll('.flip-card[data-card-id]')];
const storageKey = 'deutsch-b1:flipped-cards:v1';
let flippedIds = new Set();

try {
  const saved = JSON.parse(window.localStorage.getItem(storageKey));
  if (Array.isArray(saved)) {
    flippedIds = new Set(saved.filter((id) => typeof id === 'string'));
  }
} catch {
  // Cards still work when storage is unavailable or contains invalid JSON.
}

function setFlipped(card, isFlipped) {
  card.classList.toggle('is-flipped', isFlipped);
  card.querySelectorAll('[data-flip]').forEach((control) => {
    control.setAttribute('aria-pressed', String(isFlipped));
  });
  if (isFlipped) {
    flippedIds.add(card.dataset.cardId);
  } else {
    flippedIds.delete(card.dataset.cardId);
  }
}

function saveFlipped() {
  try {
    window.localStorage.setItem(storageKey, JSON.stringify([...flippedIds]));
  } catch {
    // Storage restrictions must not prevent flipping cards.
  }
}

cards.forEach((card) => {
  setFlipped(card, flippedIds.has(card.dataset.cardId));
  card.querySelectorAll('[data-flip]').forEach((button) => {
    button.addEventListener('click', () => {
      const isFlipped = !card.classList.contains('is-flipped');
      setFlipped(card, isFlipped);
      saveFlipped();

      const focusTarget = isFlipped
        ? card.querySelector('.flip-card-back [data-flip]')
        : card.querySelector('.flip-card-front [data-flip]');
      window.setTimeout(() => focusTarget.focus({ preventScroll: true }), 320);
    });
  });
});

document.querySelectorAll('[data-flip-all]').forEach((button) => {
  button.addEventListener('click', () => {
    const isFlipped = button.dataset.flipAll === 'true';
    cards.forEach((card) => setFlipped(card, isFlipped));
    saveFlipped();
  });
});
