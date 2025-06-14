// Configuration object for easy customization
const config = {
    company: "Mary & Pip",
    tagline: "Your personal CFO, for how you actually live.",
    subheading: "Every time money hits your account, we help you decide what to do with it—in real time.",
    ctaText: "Join the Waitlist",
    launchText: "Launching soon for iOS. Join the waitlist today.",
    emailPlaceholder: "Enter your email",
    successMessage: "Thanks for joining! We'll be in touch soon.",
    features: [
        {
            icon: "💸",
            title: "Smart Allocator",
            description: "Get real-time nudges to allocate income to spend, save, invest"
        },
        {
            icon: "📲",
            title: "Integrated Dashboard",
            description: "See all your accounts in one clean view"
        },
        {
            icon: "📋",
            title: "Personalized To-Do List",
            description: "Intelligent action items that move you forward"
        },
        {
            icon: "🧠",
            title: "Built on Behavioral Finance",
            description: "No shame, just smart psychology"
        },
        {
            icon: "💡",
            title: "Culturally Fluent",
            description: "Feels like your favorite app, not a spreadsheet"
        }
    ]
};

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            // Add staggered delay for multiple elements
            setTimeout(() => {
                entry.target.classList.add('in-view');
                
                // Handle progress bars
                if (entry.target.classList.contains('progress-bar')) {
                    const width = entry.target.style.width;
                    entry.target.style.setProperty('--progress-width', width);
                }
            }, index * 100);
        }
    });
}, observerOptions);

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', () => {
    // Observe feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => observer.observe(card));
    
    // Observe persona tags
    const personaTags = document.querySelectorAll('.persona-tag');
    personaTags.forEach(tag => observer.observe(tag));
    
    // Observe upcoming features
    const upcomingFeatures = document.querySelectorAll('.upcoming-feature');
    upcomingFeatures.forEach(feature => observer.observe(feature));
    
    // Observe progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => observer.observe(bar));
    
    // Handle CTA buttons
    const ctaButtons = document.querySelectorAll('button');
    ctaButtons.forEach(button => {
        if (button.textContent.includes('Join')) {
            button.addEventListener('click', (e) => {
                if (!button.closest('form')) {
                    e.preventDefault();
                    scrollToWaitlist();
                }
            });
        }
    });
    
    // Handle form submission
    const waitlistForm = document.getElementById('waitlist-form');
    if (waitlistForm) {
        waitlistForm.addEventListener('submit', handleFormSubmit);
    }
});

// Scroll to waitlist form
function scrollToWaitlist() {
    const waitlistSection = document.getElementById('waitlist-form');
    if (waitlistSection) {
        waitlistSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // Focus on email input after scroll
        setTimeout(() => {
            const emailInput = waitlistSection.querySelector('input[type="email"]');
            if (emailInput) emailInput.focus();
        }, 800);
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const emailInput = form.querySelector('input[type="email"]');
    const submitButton = form.querySelector('button[type="submit"]');
    const email = emailInput.value;
    
    // Validate email
    if (!isValidEmail(email)) {
        showError(emailInput, 'Please enter a valid email address');
        return;
    }
    
    // Show loading state
    submitButton.classList.add('loading');
    submitButton.textContent = 'Joining...';
    
    try {
        // Simulate API call (replace with actual endpoint)
        await simulateApiCall(email);
        
        // Success
        showSuccessMessage();
        form.reset();
        submitButton.textContent = config.ctaText;
        
        // Track conversion (replace with actual analytics)
        trackConversion(email);
        
    } catch (error) {
        showError(emailInput, 'Something went wrong. Please try again.');
        submitButton.textContent = config.ctaText;
    } finally {
        submitButton.classList.remove('loading');
    }
}

// Email validation
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Simulate API call (replace with actual implementation)
function simulateApiCall(email) {
    return new Promise((resolve) => {
        // Store email locally for demo
        const waitlist = JSON.parse(localStorage.getItem('marypip_waitlist') || '[]');
        waitlist.push({ email, timestamp: new Date().toISOString() });
        localStorage.setItem('marypip_waitlist', JSON.stringify(waitlist));
        
        // Simulate network delay
        setTimeout(resolve, 1000);
    });
}

// Show error message
function showError(input, message) {
    input.classList.add('border-red-500');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-red-500 text-sm mt-2';
    errorDiv.textContent = message;
    input.parentElement.appendChild(errorDiv);
    
    // Remove error after 3 seconds
    setTimeout(() => {
        input.classList.remove('border-red-500');
        errorDiv.remove();
    }, 3000);
}

// Show success message
function showSuccessMessage() {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = config.successMessage;
    document.body.appendChild(successDiv);
    
    // Trigger animation
    setTimeout(() => successDiv.classList.add('show'), 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        successDiv.classList.remove('show');
        setTimeout(() => successDiv.remove(), 300);
    }, 5000);
}

// Track conversion (replace with actual analytics)
function trackConversion(email) {
    console.log('Conversion tracked:', email);
    // Add your analytics tracking code here
    // e.g., gtag('event', 'sign_up', { method: 'waitlist' });
}

// Smooth parallax effect for hero section
let ticking = false;
function updateParallax() {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.min-h-screen');
    
    if (hero && scrolled < window.innerHeight) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        hero.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;
    }
    
    ticking = false;
}

function requestTick() {
    if (!ticking) {
        window.requestAnimationFrame(updateParallax);
        ticking = true;
    }
}

// Enable parallax on desktop only
if (window.innerWidth > 768) {
    window.addEventListener('scroll', requestTick);
}

// Export config for external access
window.MaryPipConfig = config; 