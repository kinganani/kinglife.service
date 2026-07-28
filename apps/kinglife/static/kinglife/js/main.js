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
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    // Show standard widget
    const pwaWidget = document.getElementById('pwa-install-widget');
    if (pwaWidget && !localStorage.getItem('pwa_prompt_dismissed')) {
        setTimeout(() => {
            pwaWidget.classList.remove('hidden');
            // Force reflow
            void pwaWidget.offsetWidth;
            pwaWidget.classList.add('show');
        }, 2000); // 2 seconds after visiting
    }

    // Show button directly in preloader
    const preloaderInstallBtn = document.getElementById('preloader-pwa-install-btn');
    if (preloaderInstallBtn) {
        preloaderInstallBtn.style.display = 'inline-block';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const pwaWidget = document.getElementById('pwa-install-widget');
    const installBtn = document.getElementById('pwa-install-btn');
    const closeBtn = document.getElementById('pwa-close-btn');
    const preloaderInstallBtn = document.getElementById('preloader-pwa-install-btn');

    // Preloader Install Button
    if (preloaderInstallBtn) {
        preloaderInstallBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                await deferredPrompt.userChoice;
                deferredPrompt = null;
                preloaderInstallBtn.style.display = 'none';

                // Instantly hide preloader after they decide
                const preloader = document.getElementById('kinglife-preloader');
                if (preloader) {
                    preloader.style.opacity = '0';
                    setTimeout(() => { preloader.style.display = 'none'; }, 500);
                }
            }
        });
    }

    // Standard Widget Install Button
    if (installBtn && pwaWidget) {
        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const choiceResult = await deferredPrompt.userChoice;
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the A2HS prompt');
                } else {
                    console.log('User dismissed the A2HS prompt');
                }
                deferredPrompt = null;
                
                // Hide banner
                pwaWidget.classList.remove('show');
                setTimeout(() => pwaWidget.classList.add('hidden'), 400);
            }
        });
    }

    if (closeBtn && pwaWidget) {
        closeBtn.addEventListener('click', () => {
            pwaWidget.classList.remove('show');
            setTimeout(() => pwaWidget.classList.add('hidden'), 400);
            localStorage.setItem('pwa_prompt_dismissed', 'true');
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
