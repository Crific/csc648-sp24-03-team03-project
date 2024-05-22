from flask import Blueprint, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import os
from db_connection import get_db_connection  # Use the shared database connection function
from flask_login import current_user, login_required
import logging

item_bp = Blueprint('item_bp', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@item_bp.route('/submit_item', methods=['POST'])
@login_required
def submit_item():
    conn = get_db_connection()
    if not conn:
        logging.error('Database connection failed')
        return 'Database connection failed', 500

    # Retrieve user ID from current_user
    user_id = current_user.UserID  # Ensure this matches your User model
    if not user_id:
        logging.error('User not logged in')
        return 'User not logged in', 403

    item_name = request.form['itemName']
    item_price = request.form['itemPrice']
    item_rental_price = request.form['rentalPrice']
    category_id = request.form['categoryID']
    item_desc = request.form.get('itemDesc', '')
    item_pic = request.files['itemPic']

    # Log received form data
    logging.debug(f"Received form data: item_name={item_name}, item_price={item_price}, category_id={category_id}, item_desc={item_desc}")

    if item_pic and item_pic.filename != '':
        filename = secure_filename(item_pic.filename)
        product_images_path = '/var/www/csc648-sp24-03-team03/application/public/Product_Images'
        thumbnails_path = os.path.join(product_images_path, 'Thumbnails')

        # Ensure the Thumbnails directory exists
        if not os.path.exists(thumbnails_path):
            os.makedirs(thumbnails_path)

        # Save the original image
        file_path = os.path.join(product_images_path, filename)
        item_pic.save(file_path)

        # Create and save the thumbnail
        thumbnail_file_path = os.path.join(thumbnails_path, filename)
        with Image.open(item_pic) as img:
            img.thumbnail((128, 128))  # Adjust the thumbnail size as needed
            img.save(thumbnail_file_path)

        cursor = conn.cursor()
        sql = """
        INSERT INTO Listing (UserID, ItemName, ItemDescription, CategoryID, Price, RentalPrice, PhotoName, PhotoPath, ThumbnailPhotoPath, PostDate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())
        """
        cursor.execute(sql, (
            user_id,  # Use actual user ID from current_user
            item_name, 
            item_desc, 
            category_id, 
            item_price, 
            item_rental_price,
            filename, 
            file_path,
            thumbnail_file_path
        ))
        conn.commit()
        cursor.close()
        conn.close()

        logging.info('Item successfully submitted')
        return redirect(url_for('index'))

    logging.error('Failed to upload file')
    return 'Failed to upload file', 400
