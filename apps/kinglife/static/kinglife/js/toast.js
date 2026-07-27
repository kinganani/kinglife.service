/* toast.js - Logic for modern toast notifications */
document.addEventListener('DOMContentLoaded', function() {
    // Show all toasts on page load
    const toasts = document.querySelectorAll('.toast');
    
    toasts.forEach(toast => {
        // Add show class after a tiny delay for animation
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        // Auto hide after 5 seconds
        const hideTimeout = setTimeout(() => {
            hideToast(toast);
        }, 5000);

        // Close button click handler
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(hideTimeout);
                hideToast(toast);
            });
        }
    });

    function hideToast(toast) {
        toast.classList.remove('show');
        // Remove from DOM after animation completes (300ms)
        setTimeout(() => {
            if(toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }
});
