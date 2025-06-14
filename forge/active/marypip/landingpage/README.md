# Mary & Pip Landing Page

A sleek, modern prelaunch landing page for Mary & Pip - Your personal CFO, for how you actually live.

## Overview

Mary & Pip is a culturally fluent personal finance platform that acts as your real-time, behaviorally smart personal CFO. This landing page reflects the tone of a lifestyle brand with a clean, mobile-friendly UX.

## Features

- **Modern Design**: Clean, minimalist design with soft colors and smooth animations
- **Mobile-First**: Fully responsive design that looks great on all devices
- **Interactive Elements**: Scroll animations, hover effects, and smooth transitions
- **Email Capture**: Waitlist signup form with validation and success feedback
- **Performance Optimized**: Minimal JavaScript and efficient CSS animations

## Tech Stack

- HTML5
- TailwindCSS (via CDN)
- Vanilla JavaScript
- Custom CSS animations

## Getting Started

### Option 1: Using npm
```bash
npm install
npm start
```

### Option 2: Using Python
```bash
python3 -m http.server 8080
```

### Option 3: Direct file opening
Simply open `index.html` in your web browser.

## File Structure

```
├── index.html      # Main HTML file with all sections
├── styles.css      # Custom CSS animations and styles
├── script.js       # JavaScript for interactivity
├── package.json    # Project configuration
└── README.md       # This file
```

## Customization

All copy and configuration can be easily edited through the `config` object in `script.js`:

```javascript
const config = {
    company: "Mary & Pip",
    tagline: "Your personal CFO, for how you actually live.",
    // ... more configuration options
};
```

## Deployment

This is a static site that can be deployed to any web hosting service:

- **Netlify**: Drag and drop the folder
- **Vercel**: Connect your Git repository
- **GitHub Pages**: Enable in repository settings
- **AWS S3**: Upload as static website

## Design Philosophy

The design follows a lifestyle brand aesthetic inspired by:
- Apple's clean minimalism
- Notion's approachable productivity
- Glossier's soft, human touch

## License

MIT License - feel free to use and modify as needed. 