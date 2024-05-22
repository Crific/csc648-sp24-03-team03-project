from flask import Blueprint, render_template, request, jsonify
from db_connection import get_db_connection

# Define the Blueprint
search_bp = Blueprint('search_bp', __name__, template_folder='./public/html')

@search_bp.route('/searchingPost', methods=['GET'])
def searching_post():
    query = request.args.get('query', '').strip()
    category = request.args.get('category', '').strip()
    price_range = request.args.get('price_range', 'None').strip()
    rental_price_range = request.args.get('rental_price_range', 'None').strip()
    
    # Connect to the database
    mydb = get_db_connection()
    cur = mydb.cursor(dictionary=True)
    
    # Construct the SQL query based on the inputs
    sql_query = """
        SELECT Listing.*, Category.CategoryName 
        FROM Listing 
        JOIN Category ON Listing.CategoryID = Category.CategoryID 
        WHERE ItemName LIKE %s AND Listing.Verified IS NOT NULL
    """
    values = [f'%{query}%']
    
    if category and category != 'default':
        sql_query += " AND Category.CategoryName = %s"
        values.append(category)


    cur.execute(sql_query, values)
    results = cur.fetchall()
    numrows = len(results)
    cur.close()
    mydb.close()
    
    # Render the results into HTML
    htmlresponse = render_template('response.html', items=results, numrows=numrows)
    return jsonify({'htmlresponse': htmlresponse})
