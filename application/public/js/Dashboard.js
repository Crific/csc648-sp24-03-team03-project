$(document).ready(function() {
    function toggleMessages() {
        var messages = document.getElementById("messagesContent");
        var listings = document.getElementById("listingsContent");
        var btnMessages = document.querySelector('.btn-outline-primary');
        var btnListings = document.querySelector('.btn-outline-secondary');

        messages.style.display = "block";
        listings.style.display = "none";
        btnMessages.classList.add('btn-active');
        btnListings.classList.remove('btn-active');
    }

    function toggleListings() {
        var messages = document.getElementById("messagesContent");
        var listings = document.getElementById("listingsContent");
        var btnMessages = document.querySelector('.btn-outline-primary');
        var btnListings = document.querySelector('.btn-outline-secondary');

        listings.style.display = "block";
        messages.style.display = "none";
        btnListings.classList.add('btn-active');
        btnMessages.classList.remove('btn-active');

        $.ajax({
            url: '/userListings',
            method: 'GET',
            success: function(response) {
                if (response.listings) {
                    var listingsContent = $('#userlistings-container');
                    listingsContent.empty();

                    if (response.listings.length === 0) {
                        listingsContent.append('<p>No listings found.</p>');
                    } else {
                        response.listings.forEach(function(listing) {
                            var listingHtml = `
                                <div class="recent-area">
                                    <p>${listing.ItemName}</p>
                                    <img src="${listing.PhotoURL}" class="recents" alt="${listing.ItemName}"/>
                                    <p class="description">Post Date: ${listing.PostDate}</p>
                                    <p class="description">Price: ${listing.Price}</p>
                                    <p class="description">Rental Price: ${listing.RentalPrice}</p>
                                    <p class="description">Category: ${listing.CategoryName}</p>
                                    <button class="trash-button btn-delete-listing" data-id="${listing.ListingID}"><i class="fa fa-trash"></i></button>
                                </div>
                            `;
                            listingsContent.append(listingHtml);
                        });
                    }

                    // Attach click event to delete buttons for listings
                    $('.btn-delete-listing').click(function() {
                        var listingId = $(this).data('id');
                        console.log("Deleting listing with ID:", listingId); // Log the listing ID
                        deleteListing(listingId);
                    });
                } else {
                    console.error('Error fetching listings:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });
    }

    function deleteListing(listingId) {
        var csrfToken = $('#csrf_token').val();
        console.log("Sending delete request for listing ID:", listingId); // Log the listing ID
        $.ajax({
            url: '/delete_listing',
            type: 'POST',
            data: { 
                id: listingId,
                csrf_token: csrfToken
            },
            success: function (response) {
                if (response.success) {
                    toggleListings();  // Refresh the listings after deletion
                } else {
                    alert('Error deleting listing.');
                }
            },
            error: function (xhr, status, error) {
                console.error("Error: " + error);
                alert('Error deleting listing.');
            }
        });
    }

    $('#toMessages').click(function() {
        toggleMessages();
    });

    $('#toListings').click(function() {
        toggleListings();
    });

    // Initial display
    if (window.location.hash === "#messages") {
        toggleMessages();
    } else {
        toggleListings();
    }
});
