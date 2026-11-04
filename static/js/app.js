document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.barra-fill').forEach(function (barra) {
        const base = barra.dataset.base;
        const porcentaje = Math.min((base / 255) * 100, 100);
        setTimeout(function () {
            barra.style.width = porcentaje + '%';
        }, 200);
    });
    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const mensaje = btn.dataset.confirm || '¿Estás seguro?';
            if (!window.confirm(mensaje)) {
                e.preventDefault();
            }
        });
    });
    const cards = document.querySelectorAll('.card-pokemon');
    cards.forEach(function (card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(function () {
            card.style.transition = 'opacity 0.4s, transform 0.4s';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 80);
    });
});
