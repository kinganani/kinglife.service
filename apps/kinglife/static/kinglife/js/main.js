/* KINGLIFE SHAL U - Main JavaScript Interactivity */

document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.querySelector('.main-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // Scroll To Top
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Scroll Down Indicator
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            const businessSection = document.querySelector('.business-section');
            if (businessSection) {
                businessSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Business Slider Arrows (Simulated horizontal scroll / sliding)
    const prevBtn = document.querySelector('.slider-btn-prev');
    const nextBtn = document.querySelector('.slider-btn-next');
    const cardsGrid = document.querySelector('.business-cards-grid');

    if (prevBtn && nextBtn && cardsGrid) {
        nextBtn.addEventListener('click', () => {
            cardsGrid.scrollBy({ left: 300, behavior: 'smooth' });
        });
        prevBtn.addEventListener('click', () => {
            cardsGrid.scrollBy({ left: -300, behavior: 'smooth' });
        });
    }

    // Mobile Navbar Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const headerActions = document.querySelector('.header-actions');

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            const isOpen = navMenu.classList.toggle('active');
            if (headerActions) headerActions.classList.toggle('active');
            mobileToggle.innerHTML = isOpen ? '✕' : '☰';
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });

        // Close mobile menu when clicking a nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                if (headerActions) headerActions.classList.remove('active');
                mobileToggle.innerHTML = '☰';
                document.body.style.overflow = '';
            });
        });
    }
});


/* PWA Install Prompt Logic */
let deferredPrompt;

// Let the browser handle the native mini-infobar automatically by NOT preventing default.
window.addEventListener('beforeinstallprompt', (e) => {
    // We intentionally DO NOT call e.preventDefault() here.
    // This allows Chrome to automatically show its native install banner/infobar
    // at the bottom or top of the screen when the page loads, as requested.
    deferredPrompt = e;

    // Keep the preloader install button functional if it exists
    const preloaderInstallBtn = document.getElementById('preloader-pwa-install-btn');
    if (preloaderInstallBtn) {
        preloaderInstallBtn.style.display = 'inline-block';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const preloaderInstallBtn = document.getElementById('preloader-pwa-install-btn');

    // Preloader Install Button
    if (preloaderInstallBtn) {
        preloaderInstallBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                await deferredPrompt.userChoice;
                deferredPrompt = null;
                preloaderInstallBtn.style.display = 'none';

                const preloader = document.getElementById('kinglife-preloader');
                if (preloader) {
                    preloader.style.opacity = '0';
                    setTimeout(() => { preloader.style.display = 'none'; }, 500);
                }
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Preloader logic
    const preloader = document.getElementById('kinglife-preloader');
    if (preloader) {
        if (!sessionStorage.getItem('kinglife_preloader_shown')) {
            const message = document.querySelector('.kl-preloader-message');
            if (message) {
                setTimeout(() => {
                    message.textContent = "Préparation de votre espace...";
                }, 800);
            }

            setTimeout(() => {
                // If button is showing, user is probably deciding. But after 5 seconds, fade it anyway
                if (preloader.style.display !== 'none') {
                    preloader.style.opacity = '0';
                    setTimeout(() => { preloader.style.display = 'none'; }, 500);
                }

                sessionStorage.setItem('kinglife_preloader_shown', 'true');
            }, 1000); // 20 seconds wait to give time to install PWA inside preloader
        } else {
            preloader.style.display = 'none';
        }
    }
});
