from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import ComposeForm
from flask_login import current_user, login_required
from db_connection import get_db_connection
import logging

compose = Blueprint('compose', __name__, static_folder='./public', template_folder='./public/html')

@compose.route('/Compose.html', methods=['GET'])
@login_required
def compose_page():
    form = ComposeForm()
    receiver_id = request.args.get('receiver_id')
    listing_id = request.args.get('listing_id')

    if not listing_id:
        flash('Listing ID is missing.', 'danger')
        return redirect(url_for('index'))

    form.receiver_id.data = receiver_id
    form.listing_id.data = listing_id

    item_details = []
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Listing.*, Category.CategoryName, User.UserName 
                FROM Listing 
                JOIN Category ON Listing.CategoryID = Category.CategoryID 
                JOIN User ON Listing.UserID = User.UserID 
                WHERE ListingID = %s
            """, (listing_id,))
            item = cursor.fetchone()
            cursor.close()
            conn.close()

            if not item:
                flash('Item not found.', 'danger')
                return redirect(url_for('index'))

            # Convert item to list and log
            item_details = list(item)
            logging.info(f"Item fetched: {item_details}")
        else:
            flash('Database connection failed.', 'danger')
            return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error fetching item details: {e}")
        flash(f"Error fetching item details: {e}", 'danger')
        return redirect(url_for('index'))

    return render_template('Compose.html', form=form, receiver_id=receiver_id, listing_id=listing_id, item_details=item_details)
