document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.faq-title').forEach(item => {
        item.addEventListener('click', () => {
            const content = item.nextElementSibling;

            // Toggle the 'open' class
            content.classList.toggle('open');

            // If the content is open, set max-height to its scrollHeight plus a little extra space
            if (content.classList.contains('open')) {
                content.style.maxHeight = content.scrollHeight + 30 + 'px';
            } else {
                content.style.maxHeight = null; // Reset max-height when closing
            }
        });
    });
});