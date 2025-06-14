// Cosmos-inspired Interactive Experience
document.addEventListener('DOMContentLoaded', function() {
    initReadingProgress();
    initBookNavigation();
    initSmoothAnimations();
});

// Reading Progress Bar
function initReadingProgress() {
    const progressBar = document.querySelector('.reading-progress');
    if (!progressBar) return;
    
    function updateProgress() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    }
    
    window.addEventListener('scroll', updateProgress);
    updateProgress();
}

// Book Navigation
function initBookNavigation() {
    // Start Reading Button
    const startReadingBtn = document.querySelector('.start-reading');
    if (startReadingBtn) {
        startReadingBtn.addEventListener('click', function() {
            const tocSection = document.querySelector('.table-of-contents');
            if (tocSection) {
                tocSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
    
    // Table of Contents Navigation
    const chapterEntries = document.querySelectorAll('.chapter-entry');
    chapterEntries.forEach(entry => {
        entry.addEventListener('click', function() {
            const chapterId = this.getAttribute('data-chapter');
            const targetSection = document.getElementById(chapterId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Smooth Animations
function initSmoothAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const elementsToAnimate = document.querySelectorAll(`
        .persona-story,
        .data-visualization,
        .psychological-insight,
        .moment-analysis,
        .chapter-quote,
        .methodology-note,
        .psychology-note,
        .final-insight,
        .pyramid-level,
        .territory,
        .prediction
    `);
    
    elementsToAnimate.forEach(el => observer.observe(el));
}

// Keyboard Navigation (Simple)
document.addEventListener('keydown', function(e) {
    // Escape to top
    if (e.key === 'Escape') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Number keys for chapters
    const chapterMap = {
        '1': 'preface',
        '2': 'personas', 
        '3': 'psychology',
        '4': 'moments',
        '5': 'influence',
        '6': 'future',
        '7': 'epilogue'
    };
    
    if (chapterMap[e.key] && !e.ctrlKey && !e.altKey) {
        const section = document.getElementById(chapterMap[e.key]);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }
});