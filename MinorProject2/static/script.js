document.addEventListener('DOMContentLoaded', function () {
    // 1. Highlight current page in navigation
    function highlightCurrentPage() {
        const path = window.location.pathname;
        let currentPage = path.split('/').pop() || 'index.html';

        if (path === '/' || path === '/index.html') {
            currentPage = 'home.html';
        }

        const navLinks = document.querySelectorAll('nav ul li a');
        navLinks.forEach(link => {
            link.classList.remove('current-page', 'active');
            let linkPage = link.getAttribute('href');
            if (linkPage.startsWith('#')) return;

            const normalizedLink = linkPage.split('#')[0].replace('.html', '').toLowerCase();
            const normalizedCurrent = currentPage.replace('.html', '').toLowerCase();

            if ((normalizedLink === normalizedCurrent) ||
                (normalizedCurrent === 'home' && (normalizedLink === '' || normalizedLink === 'index' || normalizedLink === 'home'))) {
                link.classList.add('current-page');
            }
        });
    }

    // 2. Smooth scrolling for anchor links
    function setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"], a[href*=".html#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                const [page, hash] = href.split('#');
                const currentPage = window.location.pathname.split('/').pop() || 'index.html';

                if (!page || page === currentPage || (page === 'index.html' && currentPage === 'home.html')) {
                    if (hash) {
                        e.preventDefault();
                        const targetElement = document.getElementById(hash);
                        if (targetElement) {
                            const headerHeight = document.querySelector('header')?.offsetHeight || 0;
                            window.scrollTo({
                                top: targetElement.offsetTop - headerHeight,
                                behavior: 'smooth'
                            });
                            history.pushState(null, null, `#${hash}`);
                        }
                    }
                }
            });
        });
    }

    // 3. Section switch buttons (sports/events tabs)
    function setupSectionButtons() {
        const sectionButtons = document.querySelectorAll('.section-btn');
        const sections = document.querySelectorAll('.sports-section, .events-section');

        sectionButtons.forEach(button => {
            button.addEventListener('click', function () {
                const sectionId = this.getAttribute('data-section');

                sectionButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                sections.forEach(section => {
                    section.classList.remove('active-section');
                    if (section.id === sectionId) {
                        section.classList.add('active-section');
                    }
                });
            });
        });
    }

    // 4. Event scroller
    function setupEventScroller() {
        const scrollerContainer = document.querySelector('.scroller-container');
        if (!scrollerContainer) return;

        let isPaused = false;
        let scrollPosition = 0;
        const scrollSpeed = 0.3;

        const scrollerTrack = scrollerContainer.querySelector('.scroller-track');
        const eventItems = scrollerTrack.querySelectorAll('.event-item');

        eventItems.forEach(item => {
            const clone = item.cloneNode(true);
            scrollerTrack.appendChild(clone);
        });

        function autoScroll() {
            if (!isPaused) {
                scrollPosition += scrollSpeed;
                if (scrollPosition >= scrollerTrack.scrollWidth / 2) {
                    scrollPosition = 0;
                }
                scrollerContainer.scrollLeft = scrollPosition;
            }
            requestAnimationFrame(autoScroll);
        }

        scrollerContainer.addEventListener('mouseenter', () => isPaused = true);
        scrollerContainer.addEventListener('mouseleave', () => isPaused = false);
        autoScroll();
    }

    // 5. Event gallery slideshow
    function setupEventGallery() {
        const slideshowContainer = document.querySelector('.slideshow-container');
        if (!slideshowContainer) return;

        const images = slideshowContainer.querySelectorAll('img');
        if (images.length === 0) return;

        let currentIndex = 0;
        let isPaused = false;

        function startSlideshow() {
            images.forEach(img => img.classList.remove('active'));
            images[0].classList.add('active');
            setInterval(showNextImage, 3000);
        }

        function showNextImage() {
            if (!isPaused) {
                images[currentIndex].classList.remove('active');
                currentIndex = (currentIndex + 1) % images.length;
                images[currentIndex].classList.add('active');
            }
        }

        slideshowContainer.addEventListener('mouseenter', () => isPaused = true);
        slideshowContainer.addEventListener('mouseleave', () => isPaused = false);

        startSlideshow();
    }

    // 6. Scroll to hash on load
    function scrollToHashIfPresent() {
        if (window.location.hash) {
            const targetId = window.location.hash.slice(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                const headerHeight = document.querySelector('header')?.offsetHeight || 0;
                setTimeout(() => {
                    window.scrollTo({
                        top: targetElement.offsetTop - headerHeight,
                        behavior: 'smooth'
                    });
                }, 100);
            }
        }
    }

    // 7. Booking flow functions
    function showBookingFlow() {
        document.getElementById('booking-flow').style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    function hideBookingFlow() {
        document.getElementById('booking-flow').style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    function loadBookingStep(page) {
        // Show loading state
        document.getElementById('dynamic-booking-container').innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <p>Loading booking system...</p>
            </div>
        `;
        
        fetch(page)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load page (HTTP ${response.status})`);
                }
                return response.text();
            })
            .then(html => {
                // Insert the loaded HTML
                document.getElementById('dynamic-booking-container').innerHTML = html;
                document.body.scrollIntoView({ behavior: 'smooth' });
    
                // Initialize specific page functionality
                if (page === 'login.html') {
                    initLoginStep();
                } 
                else if (page === 'sports_selection.html' || page === 'sports-selection.html') {
                    initSportsSelectionStep();
                } 
                else if (page === 'booking.html') {
                    initBookingStep();
                }
            })
            .catch(error => {
                console.error('Error loading booking step:', error);
                document.getElementById('dynamic-booking-container').innerHTML = `
                    <div class="error-state">
                        <h3>Error Loading Content</h3>
                        <p>${error.message || 'Unable to load the booking system. Please try again later.'}</p>
                        <button onclick="loadBookingStep('login.html')" class="book-btn">Return to Login</button>
                    </div>
                `;
            });
    }
    
    // Helper functions
    function initLoginStep() {
        const loginForm = document.querySelector('.email-box');
        if (loginForm) {
            loginForm.onsubmit = function(e) {
                e.preventDefault();
                const email = this.querySelector('input[type="email"]').value;
                if (email) {
                    localStorage.setItem('userEmail', email);
                    loadBookingStep('sports_selection.html');
                }
            };
        }
    }
    
    function initSportsSelectionStep() {
        const selectBtn = document.querySelector('.select-btn');
        if (selectBtn) {
            selectBtn.addEventListener('click', function() {
                const selectedSport = document.getElementById('sportDropdown').value;
                if (selectedSport === 'badminton') {
                    localStorage.setItem('selectedSport', selectedSport);
                    loadBookingStep('booking.html');
                } else {
                    const error = document.getElementById('errorMsg');
                    if (error) {
                        error.style.display = 'block';
                        error.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        }
    }
    
    function initBookingStep() {
        // Set minimum date to today and initialize with today's date
        const today = new Date();
        const todayFormatted = today.toISOString().split('T')[0];
        const dateInput = document.getElementById('date');
        
        // Initialize date picker
        if (dateInput) {
            dateInput.min = todayFormatted;
            dateInput.value = todayFormatted;
            
            // Date validation and slot update handler
            dateInput.addEventListener('change', function() {
                updateAvailableSlots(this.value);
            });
            
            // Initial slots load
            updateAvailableSlots(dateInput.value);
        }

        // Handle book button
        const bookBtn = document.getElementById('bookBtn');
        if (bookBtn) {
            bookBtn.addEventListener('click', function() {
                const selectedSlot = document.querySelector('.slot.selected');
                const selectedDate = dateInput?.value;
                
                if (selectedSlot && selectedDate) {
                    localStorage.setItem('selectedSlot', selectedSlot.textContent);
                    localStorage.setItem('selectedDate', selectedDate);
                    
                    // Replace with your actual Google Form URL
                    const formUrl = `https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?usp=pp_url&entry.date=${encodeURIComponent(selectedDate)}&entry.time=${encodeURIComponent(selectedSlot.textContent)}`;
                    window.open(formUrl, '_blank');
                } else {
                    alert('Please select both a date and time slot before proceeding');
                }
            });
        }
    }
    
    function updateAvailableSlots(date) {
        const slotsContainer = document.getElementById('slots');
        if (!slotsContainer) return;
        
        slotsContainer.innerHTML = '<div class="loading-slots">Loading available slots...</div>';
        
        // Simulate API call with timeout
        setTimeout(() => {
            if (!date) {
                slotsContainer.innerHTML = '<div class="no-slots">Please select a date to see available slots</div>';
                return;
            }
            
            // Sample slot data - replace with real data from your backend
            const slotData = {
                "2025-04-17": ["10:00 AM", "3:00 PM", "5:00 PM"],
                "2025-04-19": ["9:00 AM", "11:00 AM", "4:00 PM"],
                "2025-04-25": ["8:00 AM", "6:00 PM"],
                "2025-04-16": ["10:00 AM", "2:00 PM", "4:00 PM", "6:00 PM"]
            };
            
            if (slotData[date]) {
                slotsContainer.innerHTML = '';
                slotData[date].forEach(slot => {
                    const slotElement = document.createElement('div');
                    slotElement.className = 'slot';
                    slotElement.textContent = slot;
                    slotElement.onclick = function() {
                        document.querySelectorAll('.slot').forEach(el => el.classList.remove('selected'));
                        this.classList.add('selected');
                    };
                    slotsContainer.appendChild(slotElement);
                });
            } else {
                slotsContainer.innerHTML = '<div class="no-slots">No slots available for this date</div>';
            }
        }, 500);
    }

    // 8. Override navigation to trigger booking modal
    document.querySelectorAll('a[href="#rental"], a[href="login.html"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            loadBookingStep('login.html');
        });
    });

    // Run all setups
    function handlePageLoad() {
        highlightCurrentPage();
        setupSmoothScrolling();
        setupSectionButtons();
        setupEventScroller();
        setupEventGallery();
        scrollToHashIfPresent();
    }

    handlePageLoad();
    window.addEventListener('popstate', () => {
        highlightCurrentPage();
        scrollToHashIfPresent();
    });

    // Make functions available globally
    window.hideBookingFlow = hideBookingFlow;
    window.loadBookingStep = loadBookingStep;
});