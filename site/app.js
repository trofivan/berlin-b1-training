document.querySelectorAll('[data-flip]').forEach((button) => {
  button.addEventListener('click', () => {
    const card = button.closest('.flip-card');
    const isFlipped = card.classList.toggle('is-flipped');
    card.querySelectorAll('[data-flip]').forEach((control) => {
      control.setAttribute('aria-pressed', String(isFlipped));
    });

    const focusTarget = isFlipped
      ? card.querySelector('.flip-card-back [data-flip]')
      : card.querySelector('.flip-card-front [data-flip]');
    window.setTimeout(() => focusTarget.focus({ preventScroll: true }), 320);
  });
});
