$(document).ready(function() {

    // Function to handle search form submissions
    function performSearch() {
        var query = $('#searchText').val();
        var category = $('#category').val();

        // Redirect to Search.html with query parameters
        var searchParams = new URLSearchParams({
            query: query,
            category: category
        }).toString();

        window.location.href = 'Search.html?' + searchParams;
    }

    // Common functionality to handle search form submission
    $('#searchForm, #searchForm2').on('submit', function(event) {
        event.preventDefault();
        performSearch();
    });

    // Handle search button click event
    $('.searchButton').click(function() {
        performSearch();
    });

    // Load initial recent items if on Index.html
    if (window.location.pathname.endsWith("Index.html")) {
        $.ajax({
            url: '/recentItemsPost',
            method: 'GET',
            success: function(response) {
                $('#main-content').html(response);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching recent items:', error);
            }
        });
    }

    // If on Search.html, handle search and filters
    if (window.location.pathname.endsWith("Search.html")) {
        console.log("script.js loaded on Search.html");

        // Function to fetch and display search results
        function fetchSearchResults() {
            var urlParams = new URLSearchParams(window.location.search);
            var query = urlParams.get('query');
            var category = urlParams.get('category');

            console.log('Performing search with params:', {
                query: query,
                category: category
            });

            // Perform search with the extracted parameters
            $.ajax({
                url: '/searchingPost',
                method: 'GET',
                data: { query: query, category: category },
                success: function(response) {
                    $('#display-range').html(response.htmlresponse);
                    triggerAnimations();
                    sortResults(); // Ensure initial sort
                },
                error: function(xhr, status, error) {
                    console.error('Error during search:', error);
                }
            });
        }

        // Initial search results load
        fetchSearchResults();

        // Handle filter changes
        $('#price-r, #rentalprice-r').change(function() {
            sortResults();
        });

        // Function to sort results
        function sortResults() {
            var priceSort = $('#price-r').val();
            var rentalPriceSort = $('#rentalprice-r').val();

            if (priceSort !== 'None') {
                sortItems(priceSort, 'price');
            } else if (rentalPriceSort !== 'None') {
                sortItems(rentalPriceSort, 'rental-price');
            }
        }

        // Function to sort items
        function sortItems(sortOrder, sortType) {
            var items = $('.recent-area').get();
            items.sort(function(a, b) {
                var aText = $(a).find('.' + sortType).text().split(': ')[1].trim();
                var bText = $(b).find('.' + sortType).text().split(': ')[1].trim();

                var valA = aText === "Not Available" ? (sortOrder === 'LowHigh' ? Infinity : -Infinity) : parseFloat(aText);
                var valB = bText === "Not Available" ? (sortOrder === 'LowHigh' ? Infinity : -Infinity) : parseFloat(bText);

                if (sortOrder === 'LowHigh') {
                    return valA - valB;
                } else {
                    return valB - valA;
                }
            });
            $('#display-range').empty().append(items);
        }

        // Function to trigger animations
        function triggerAnimations() {
            $('#recent-area2').fadeOut(500, function() {
                setTimeout(function() {
                    $('.filters').addClass('show');
                    $('#search-results').addClass('show');
                    adjustFooterMarginTop(50);
                }, 500);
            });
        }

        // Function to adjust footer margin
        function adjustFooterMarginTop(num) {
            var marginsize = num !== undefined ? 30 + num : 30;
            $('#footer').css('margin-top', marginsize + 'px');
        }

        // Function to adjust main content height
        function adjustMainContentHeight() {
            var itemCount = $('.recent-area').length;
            var itemHeight = $('.recent-area').outerHeight(true);
            var newHeight;

            var windowWidth = window.innerWidth;

            if (windowWidth < 659) {
                newHeight = itemCount * itemHeight;
            } else if (windowWidth < 1098) {
                newHeight = Math.ceil(itemCount / 2) * itemHeight;
            } else if (windowWidth < 1387) {
                newHeight = Math.ceil(itemCount / 3) * itemHeight;
            } else if (windowWidth < 1676) {
                newHeight = Math.ceil(itemCount / 4) * itemHeight;
            } else {
                newHeight = Math.ceil(itemCount / 5) * itemHeight;
            }

            newHeight + 200;

            $('.main-content').css('height', newHeight);
        }

        adjustMainContentHeight();

        $(window).on('load resize', function() {
            adjustMainContentHeight();
        });

        setInterval(adjustMainContentHeight, 1);

        window.addEventListener('resize', adjustMainContentHeight);
    }

    // Common functionality
    $('#dropdownBtn').click(function() {
        $('#dropdownContent').toggleClass('show');
    });

    $(document).click(function(e) {
        if (!$(e.target).closest('#dropdownBtn').length && !$(e.target).closest('#dropdownContent').length) {
            $('#dropdownContent').removeClass('show');
        }
    });

    $('#toMessages').click(function() {
        toggleElements("messages");
        adjustMainContentHeightForMessages();
        adjustFooterMarginTop(30);
    });

    $('#toListings').click(function() {
        toggleElements("listings");
        adjustMainContentHeightForListings();
        adjustFooterMarginTop(30);
    });

    function toggleElements(selected) {
        const messageNum = document.querySelector(".message-num");
        const messageContainer = document.querySelector(".message-area");
        const listingNum = document.querySelector(".listing-num");
        const listingContainer = document.querySelector(".listing-area");

        if (selected === "messages") {
            messageNum.classList.add("message-num-show");
            messageContainer.classList.add("message-area-show");
            listingNum.classList.remove("listing-num-show");
            listingContainer.classList.remove("listing-area-show");

            $('#toMessages').addClass('active');
            $('#toListings').removeClass('active');
        } else if (selected === "listings") {
            messageNum.classList.remove("message-num-show");
            messageContainer.classList.remove("message-area-show");
            listingNum.classList.add("listing-num-show");
            listingContainer.classList.add("listing-area-show");

            $('#toListings').addClass('active');
            $('#toMessages').removeClass('active');
        }
    }

    function adjustFooterMarginTop(num) {
        var marginsize = num !== undefined ? 30 + num : 30;
        $('#footer').css('margin-top', marginsize + 'px');
    }

    function adjustMainContentHeightForListings() {
        var listingCount = $('.listing-container').length;
        var listingNewHeight = listingCount * $('.listing-container').outerHeight(true);

        $('.main-content').css('height', listingNewHeight);
    }

    function adjustMainContentHeightForMessages() {
        var messageCount = $('.message-container').length;
        var messageNewHeight = messageCount * $('.message-container').outerHeight(true);

        $('.main-content').css('height', messageNewHeight);
    }

    window.addEventListener('resize', adjustMainContentHeight);
});
