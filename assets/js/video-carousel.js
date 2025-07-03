// Video Carousel with Scroll-based Transitions

(function() {
    'use strict';
    
    // Configuration
    const TRANSITION_DURATION = 2000; // 2 seconds for fade
    const SCROLL_THRESHOLD = 100; // pixels before section change triggers
    
    // Get elements
    const videoSlides = document.querySelectorAll('.video-slide');
    const fadeOverlay = document.querySelector('.fade-overlay');
    const textContent = document.querySelector('.text-content');
    
    // Track current video
    let currentVideoIndex = 0;
    let isTransitioning = false;
    
    // Section markers for video changes (6 videos now)
    const sectionMap = [
        { id: 'intro', videoIndex: 0, scrollPosition: 0 },
        { id: 'theory', videoIndex: 1, scrollPosition: 800 },
        { id: 'excitation', videoIndex: 2, scrollPosition: 1600 },
        { id: 'chronology', videoIndex: 3, scrollPosition: 2400 },
        { id: 'oscillations', videoIndex: 4, scrollPosition: 3200 },
        { id: 'predictions', videoIndex: 5, scrollPosition: 4000 }
    ];
    
    // Initialize first video
    function init() {
        videoSlides[0].classList.add('active');
        
        // Ensure first video plays
        const firstVideo = videoSlides[0].querySelector('video');
        if (firstVideo) {
            firstVideo.play();
        }
        
        // Add section markers to content for scroll detection
        addSectionMarkers();
        
        // Set up scroll listener
        const textColumn = document.querySelector('.text-column');
        textColumn.addEventListener('scroll', handleScroll);
        
        // Also set up intersection observer for better detection
        setupIntersectionObserver();
    }
    
    // Add invisible markers to content for section detection
    function addSectionMarkers() {
        const headers = textContent.querySelectorAll('h2');
        headers.forEach((header, index) => {
            if (index < sectionMap.length) {
                header.classList.add('section-marker');
                header.dataset.section = sectionMap[index].id;
            }
        });
    }
    
    // Handle scroll events
    function handleScroll(e) {
        if (isTransitioning) return;
        
        const scrollTop = e.target.scrollTop;
        const scrollHeight = e.target.scrollHeight;
        const clientHeight = e.target.clientHeight;
        
        // Calculate scroll percentage (0 to 1)
        const scrollPercentage = Math.min(1, Math.max(0, scrollTop / Math.max(1, scrollHeight - clientHeight)));
        
        // Determine which video should be showing based on percentage
        const videoCount = sectionMap.length;
        const sectionSize = 1 / videoCount;
        let targetVideoIndex = Math.floor(scrollPercentage / sectionSize);
        
        // Ensure we don't exceed the last video
        targetVideoIndex = Math.min(targetVideoIndex, videoCount - 1);
        
        // Change video if needed
        if (targetVideoIndex !== currentVideoIndex) {
            console.log(`Changing from video ${currentVideoIndex} to ${targetVideoIndex} at scroll ${Math.round(scrollPercentage * 100)}%`);
            transitionToVideo(targetVideoIndex);
        }
    }
    
    // Transition between videos with fade to black
    function transitionToVideo(newIndex) {
        if (isTransitioning || newIndex === currentVideoIndex) return;
        
        isTransitioning = true;
        const currentSlide = videoSlides[currentVideoIndex];
        const newSlide = videoSlides[newIndex];
        
        // Start fade to black
        fadeOverlay.classList.add('active');
        
        setTimeout(() => {
            // Switch videos during black screen
            currentSlide.classList.remove('active');
            newSlide.classList.add('active');
            
            // Ensure new video starts playing
            const newVideo = newSlide.querySelector('video');
            if (newVideo) {
                newVideo.currentTime = 0;
                newVideo.play();
            }
            
            // Update current index
            currentVideoIndex = newIndex;
            
            // Fade back from black
            setTimeout(() => {
                fadeOverlay.classList.remove('active');
                
                // Allow new transitions after fade completes
                setTimeout(() => {
                    isTransitioning = false;
                }, TRANSITION_DURATION / 2);
            }, 500);
        }, TRANSITION_DURATION / 2);
    }
    
    // Alternative: Change video based on visible sections
    function setupIntersectionObserver() {
        const options = {
            root: document.querySelector('.text-column'),
            rootMargin: '-40% 0px -40% 0px',
            threshold: 0
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sectionId = entry.target.dataset.section;
                    const section = sectionMap.find(s => s.id === sectionId);
                    if (section) {
                        transitionToVideo(section.videoIndex);
                    }
                }
            });
        }, options);
        
        // Observe all section markers
        document.querySelectorAll('.section-marker').forEach(marker => {
            observer.observe(marker);
        });
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (isTransitioning) return;
        
        if (e.key === 'ArrowDown' && currentVideoIndex < videoSlides.length - 1) {
            transitionToVideo(currentVideoIndex + 1);
        } else if (e.key === 'ArrowUp' && currentVideoIndex > 0) {
            transitionToVideo(currentVideoIndex - 1);
        }
    });
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();