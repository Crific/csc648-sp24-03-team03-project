from flask import Blueprint, render_template, jsonify, request, url_for
from flask_login import login_required, current_user
from db_connection import get_db_connection
import logging

logging.basicConfig(level=logging.DEBUG)

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='./public/html')

@dashboard_bp.route('/userListings', methods=['GET'])
@login_required
def user_listings():
    try:
        mydb = get_db_connection()
        cur = mydb.cursor(dictionary=True)
        logging.debug('Database connection established.')
        
        query = """
            SELECT 
                Listing.ItemName, 
                Listing.PhotoName AS file_name, 
                Listing.Price,
                Listing.RentalPrice,
                Listing.PostDate,
                Category.CategoryName 
            FROM 
                Listing 
            JOIN 
                Category 
            ON 
                Listing.CategoryID = Category.CategoryID 
            WHERE 
                Listing.UserID = %s
        """
        logging.debug('Executing query: %s', query)
        cur.execute(query, (current_user.UserID,))
        listings = cur.fetchall()
        logging.debug('Query executed successfully. Listings: %s', listings)
        
        # Construct PhotoURL and handle null values
        for listing in listings:
            listing['PhotoURL'] = url_for('static', filename='Product_Images/Thumbnails/' + listing['file_name'])
            listing['PostDate'] = listing['PostDate'].strftime('%Y-%m-%d') if listing['PostDate'] else 'N/A'
            listing['RentalPrice'] = listing['RentalPrice'] if listing['RentalPrice'] is not None else 'N/A'
        
        cur.close()
        mydb.close()
        logging.debug('Database connection closed.')
        
        return jsonify({'listings': listings})
    except Exception as e:
        logging.error("Error occurred:", exc_info=True)
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/delete_message', methods=['POST'])
@login_required
def delete_message():
    try:
        message_id = request.form['id']
        mydb = get_db_connection()
        cur = mydb.cursor()
        logging.debug('Database connection established.')

        query = "DELETE FROM Message WHERE MessageID = %s AND ReceiverUserID = %s"
        logging.debug('Executing query: %s', query)
        cur.execute(query, (message_id, current_user.UserID))
        mydb.commit()

        cur.close()
        mydb.close()
        logging.debug('Message deleted and database connection closed.')

        return jsonify({'success': True})
    except Exception as e:
        logging.error("Error occurred:", exc_info=True)
        return jsonify({'error': str(e)}), 500
