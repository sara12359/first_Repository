/**
 * Holiday Explorer - Main JavaScript
 * Handles AJAX requests and dynamic UI updates
 */

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('holiday-form');
    const searchBtn = document.getElementById('search-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const holidaysGrid = document.getElementById('holidays-grid');
    const noResults = document.getElementById('no-results');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');

    // Form submission handler
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const country = document.getElementById('country').value;
        const year = document.getElementById('year').value;

        if (!country || !year) {
            showError('Please select both a country and a year.');
            return;
        }

        await fetchHolidays(country, year);
    });

    /**
     * Fetch holidays from the API
     */
    async function fetchHolidays(country, year) {
        // Reset UI
        hideAllMessages();
        holidaysGrid.innerHTML = '';
        loadingSpinner.style.display = 'flex';
        searchBtn.disabled = true;

        try {
            const response = await fetch(`/api/holidays/?country=${country}&year=${year}`);
            const data = await response.json();

            loadingSpinner.style.display = 'none';
            searchBtn.disabled = false;

            if (data.success && data.holidays && data.holidays.length > 0) {
                displayHolidays(data.holidays);
            } else if (data.success && (!data.holidays || data.holidays.length === 0)) {
                noResults.style.display = 'flex';
            } else {
                showError(data.error || 'Failed to fetch holidays. Please try again.');
            }
        } catch (error) {
            loadingSpinner.style.display = 'none';
            searchBtn.disabled = false;
            showError('Network error. Please check your connection and try again.');
            console.error('Fetch error:', error);
        }
    }

    /**
     * Display holidays in the grid
     */
    function displayHolidays(holidays) {
        holidaysGrid.innerHTML = '';

        holidays.forEach((holiday, index) => {
            const card = createHolidayCard(holiday, index);
            holidaysGrid.appendChild(card);
        });
    }

    /**
     * Create a holiday card element
     */
    function createHolidayCard(holiday, index) {
        const card = document.createElement('div');
        card.className = 'holiday-card';
        card.style.animationDelay = `${index * 0.05}s`;

        // Format the date nicely
        const dateStr = formatDate(holiday.date_year, holiday.date_month, holiday.date_day);

        // Build the card HTML
        let cardHtml = `
            <div class="holiday-header">
                <h3 class="holiday-name">${escapeHtml(holiday.name)}</h3>
                ${holiday.type ? `<span class="holiday-type">${escapeHtml(holiday.type)}</span>` : ''}
            </div>
            <div class="holiday-date">
                <span class="holiday-date-icon">📅</span>
                <span>${dateStr}</span>
                ${holiday.week_day ? `<span>• ${escapeHtml(holiday.week_day)}</span>` : ''}
            </div>
            <div class="holiday-location">
                <span class="holiday-location-icon">📍</span>
                <span>${escapeHtml(holiday.location || holiday.country)}</span>
            </div>
        `;

        // Add local name if different
        if (holiday.name_local && holiday.name_local !== holiday.name) {
            cardHtml += `
                <div class="holiday-local-name">
                    Local: ${escapeHtml(holiday.name_local)}
                </div>
            `;
        }

        // Add description if available
        if (holiday.description) {
            cardHtml += `
                <div class="holiday-description">
                    ${escapeHtml(holiday.description)}
                </div>
            `;
        }

        card.innerHTML = cardHtml;
        return card;
    }

    /**
     * Format date from components
     */
    function formatDate(year, month, day) {
        try {
            const date = new Date(year, month - 1, day);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } catch {
            return `${month}/${day}/${year}`;
        }
    }

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Hide all message elements
     */
    function hideAllMessages() {
        noResults.style.display = 'none';
        errorMessage.style.display = 'none';
    }

    /**
     * Show error message
     */
    function showError(message) {
        hideAllMessages();
        errorText.textContent = message;
        errorMessage.style.display = 'flex';
    }
});
