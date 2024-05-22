$(document).ready(function() {
    function toggleMessages() {
        var messages = document.getElementById("messagesContent");
        var listings = document.getElementById("listingsContent");
       // var composeBtn = document.querySelector('.btn-compose');
        var btnMessages = document.querySelector('.btn-outline-primary');
        var btnListings = document.querySelector('.btn-outline-secondary');

        messages.style.display = "block";
        listings.style.display = "none";
        //composeBtn.style.display = "block";
        btnMessages.classList.add('btn-active');
        btnListings.classList.remove('btn-active');
    }

    function toggleListings() {
        var messages = document.getElementById("messagesContent");
        var listings = document.getElementById("listingsContent");
        //var composeBtn = document.querySelector('.btn-compose');
        var btnMessages = document.querySelector('.btn-outline-primary');
        var btnListings = document.querySelector('.btn-outline-secondary');

        listings.style.display = "block";
        messages.style.display = "none";
        //composeBtn.style.display = "none";
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
                                    <button class="trash-button"><i class="fa fa-trash"></i></button>
                                </div>
                            `;
                            listingsContent.append(listingHtml);
                        });
                    }

                    $('#userlistings-container').show();
                    $('#messagesContent').hide();
                } else {
                    console.error('Error fetching listings:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });
    }

    if (window.location.hash === "#messages") {
        toggleMessages();
    } else {
        toggleMessages();
    }

    $('#toMessages').click(function() {
        toggleMessages();
    });

    $('#toListings').click(function() {
        toggleListings();
    });

    function updateMessageBadge() {
        const badge = document.getElementById('messageCount');
        const count = 1; 
        
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }
    }

    updateMessageBadge();
});
