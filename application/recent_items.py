from flask import Blueprint, render_template, jsonify
from db_connection import get_db_connection

recent_items = Blueprint('recent_items', __name__, static_folder='./public', template_folder='./public/html')

@recent_items.route('/recentItemsPost')
def recent_items_post():
    try:
        mydb = get_db_connection()
        cur = mydb.cursor(dictionary=True)
        query = """
            SELECT 
                Listing.*, 
                Category.CategoryName 
            FROM 
                Listing 
            JOIN 
                Category 
            ON 
                Listing.CategoryID = Category.CategoryID 
            WHERE
                Listing.Verified IS NOT NULL
            ORDER BY 
                ListingID DESC 
            LIMIT 4
        """
        cur.execute(query)
        items = cur.fetchall()
        cur.close()
        mydb.close()
        return render_template('RecentItemResponse.html', items=items)
    except Exception as e:
        print("Error occurred:", e)  # Log to console or log file
        return jsonify({'error': str(e)}), 500  # Return error as JSON
