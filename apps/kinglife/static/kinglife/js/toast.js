/* toast.js - Global Logic for Modern Toast Notifications & Network/Code Error Handlers */

function showToast(message, type = 'info', duration = 5000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = 'ℹ️';
    if (type === 'success') icon = '✓';
    else if (type === 'error') icon = '⚠️';
    else if (type === 'warning' || type === 'network') icon = '📡';

    toast.innerHTML = `
        <div class="toast-content">
            <div class="toast-icon">${icon}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" aria-label="Fermer">&times;</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 50);

    const hideTimeout = setTimeout(() => {
        hideToast(toast);
    }, duration);

    const closeBtn = toast.querySelector('.toast-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            clearTimeout(hideTimeout);
            hideToast(toast);
        });
    }
}

function hideToast(toast) {
    if (!toast) return;
    toast.classList.remove('show');
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 300);
}

document.addEventListener('DOMContentLoaded', function() {
    // Show all existing static toasts on page load
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        const hideTimeout = setTimeout(() => {
            hideToast(toast);
        }, 5000);

        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(hideTimeout);
                hideToast(toast);
            });
        }
    });

    // 📡 Detect Network Instability & Reconnection
    window.addEventListener('offline', function () {
        showToast("📡 Connexion internet instable ou interrompue. Mode dégradé hors-ligne actif.", "warning", 6000);
    });

    window.addEventListener('online', function () {
        showToast("✅ Connexion internet rétablie avec succès !", "success", 4000);
    });

    // ⚠️ Global Error Handler (Captures Code & Script Errors Gracefully)
    window.addEventListener('error', function (event) {
        if (event.message && !event.message.includes('Script error')) {
            const cleanMsg = event.message.replace(/^Uncaught\s+/i, '');
            showToast(`⚠️ Erreur capturée : ${cleanMsg}`, 'error', 6000);
        }
    });

    // ⚠️ Unhandled Promise Rejections (e.g. Failed Network Requests)
    window.addEventListener('unhandledrejection', function (event) {
        const reason = event.reason ? (event.reason.message || String(event.reason)) : 'Requête réseau interrompue';
        if (!reason.includes('canceled') && !reason.includes('aborted')) {
            showToast(`📡 Connexion instable ou erreur réseau : ${reason}`, 'warning', 5000);
        }
    });
});
