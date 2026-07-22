// static/js/search_filter.js
// Handles instant search and status filtering on the dashboard,
// entirely in the browser (no page reload needed)

const searchInput = document.getElementById("search-input");
const filterButtons = document.querySelectorAll(".filter-btn");
const foodCards = document.querySelectorAll(".food-card");

// Keeps track of which status filter is currently active
// "all" means no filter - show everything
let currentFilter = "all";

// This function re-checks EVERY card against both the search text 
// AND the active filter, and shows/hides each one accordingly
function applyFiltersAndSearch() {
    const searchText = searchInput.value.toLowerCase().trim();

    foodCards.forEach(card => {
        // data-food-name and data-status are custom attributes we'll 
        // add to each card in the HTML, so JavaScript can read them
        const foodName = card.getAttribute("data-food-name").toLowerCase();
        const cardStatus = card.getAttribute("data-status");

        // Check 1: does the search text match this card's food name?
        // If the search box is empty, everything counts as a match
        const matchesSearch = searchText === "" || foodName.includes(searchText);

        // Check 2: does this card match the currently selected filter?
        const matchesFilter = currentFilter === "all" || cardStatus === currentFilter;

        // Only show the card if BOTH conditions are true
        if (matchesSearch && matchesFilter) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

// Re-run the filter every time the user types in the search box
if (searchInput) {
    searchInput.addEventListener("input", applyFiltersAndSearch);
}

// Set up each filter button (All / Fresh / Warning / Urgent / Expired)
filterButtons.forEach(button => {
    button.addEventListener("click", () => {
        // Update which filter is active
        currentFilter = button.getAttribute("data-filter");

        // Update button styling so the ACTIVE filter is visually highlighted
        filterButtons.forEach(btn => btn.classList.remove("filter-active"));
        button.classList.add("filter-active");

        applyFiltersAndSearch();
    });
});
