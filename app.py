import mysql.connector
import qrcode
from threading import Thread, Lock
import uuid
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file, abort,make_response, jsonify
import os
from mysql.connector import Error
import logging

from datetime import datetime
app = Flask(__name__)
app.secret_key = 'my_secret_key_1234'  # Replace with your actual secret key

# Simulating a simple admin login (can be replaced with a database check)
admin_credentials = {
    "username": "admin",
    "password": "12345678"
}

# Establish database connection
conn = mysql.connector.connect(
    host="tnbeat2025.pixoustech.in",
    user="hei3blcfx7yy",
    password="Pixoustech@2023",
    database= "tnbeatexpo_registration",
)
cur = conn.cursor()

# Create and use database
cur.execute("CREATE DATABASE IF NOT EXISTS tnbeatexpo_registration;")
cur.execute("USE tnbeatexpo_registration;")

# Create the registration table
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS registrationmaster (
#         ID VARCHAR(50) PRIMARY KEY,
#         RegistrationType VARCHAR(250),
#         RegistrationNoPrefix VARCHAR(250),
#         RegistrationNo VARCHAR(250),
#         RegistrationRunningNo INT,
#         FirstName VARCHAR(350),
#         LastName VARCHAR(350),
#         Gender VARCHAR(350),
#         Age INT,
#         Community VARCHAR(350),
#         Phone VARCHAR(50),
#         Email VARCHAR(350),
#         District VARCHAR(350),
#         State VARCHAR(350),
#         ReferenceBy VARCHAR(350),
#         VisitorCategory VARCHAR(350),
#         PurposeOfVisit TEXT,
#         InterestedSector VARCHAR(350),
#         PurposeOfParticipation TEXT,
#         CompanyName TEXT,
#         BusinessCategory VARCHAR(350),
#         BusinessType VARCHAR(350),
#         BusinessTrade VARCHAR(350),
#         YearEstablished VARCHAR(350) DEFAULT 0,
#         BusinessTurnOver  VARCHAR(350) DEFAULT 0,
#         UdyogRegistrationId TEXT,
#         GSTNumber TEXT,
#         DescriptionOfProducts TEXT,
#         IsMoreStailsReq BIT(1),
#         IsActive BIT(1),
#         CreatedBy VARCHAR(50),
#         CreatedByUsername VARCHAR(250),
#         CreatedDate DATETIME,
#         ModifiedBy VARCHAR(50),
#         ModifiedByUserName VARCHAR(250),
#         DeletedBy VARCHAR(50),
#         DeletedByUserName VARCHAR(250),
#         DeletedDate DATETIME,
#         Seminars TEXT,
#         ReferenceByOthers VARCHAR(500),
#         OthersCategory VARCHAR(100),
#         IsStallCancelled BIT(1),
#         NatureOfActivities VARCHAR(100),
#         IsCheckedIn BIT(1)
        
#     )
# ''')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('buttons.html')

@app.route('/visitor', methods=['GET', 'POST'])
def visitor():
    if request.method == 'POST':
        print(request.form)  # Debugging: Print all form data
        try:
            fname = request.form['fn']
            lname = request.form['ln']
            phone = request.form['ph']
            email = request.form.get('email', '')  # Handle missing email gracefully
            visitor = request.form.get('vc', '')  # Optional fields with default values
            purpose = request.form.get('pv', '')
            gender = request.form.get('gender', '')
            age = request.form.get('age', '')
            state = request.form.get('state', '')
            district = request.form.get('dis', '')
            cmt = request.form.get('cmt', '')
            
            # Generate a random UUID for the ID field
            random_id = str(uuid.uuid4())
            rt = 'VISITOR'
            
            if rt.upper() == 'VISITOR':
                prefix = 'VIS1'
            else:
                prefix = rt[:3].upper()  # First three letters, uppercase

            # Set ismorestall based on visitor category
            if visitor:
                ismorestall = 0
            else:
                ismorestall = 1
            
            createdate = datetime.now()

            # Fetch the current running number and increment it
            query = "SELECT MAX(RegistrationRunningNo) FROM registrationmaster WHERE RegitrationType = %s"
            cur.execute(query, (rt,))
            result = cur.fetchone()  # Fetch the result
            current_no = result[0] if result[0] else 0  # Start from 0 if none exists
            new_no = current_no + 1
            r_no = f"{prefix}{new_no:05}"  # Add leading zeros

            # Ensure age is valid
            if age and age.isdigit():
                age = int(age)  # Convert to integer if it's not empty and is a valid digit
            else:
                age = None  # Set to None (NULL in database) if empty or invalid

            # Insert into the database
            query = '''
                INSERT INTO registrationmaster (ID, RegitrationType, RegistrationNoPrefix, RegistrationNo, RegistrationRunningNo, FirstName, LastName, Gender, Age, Phone, Email, District, State, VisitorCategory, PurposeOfVisit, CreatedBy, CreatedByUserName, IsMoreStallsReq, CreatedDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            params = (random_id, rt, prefix, r_no, new_no, fname, lname, gender, age, phone, email, district, state, visitor, purpose, random_id, fname + " " + lname, ismorestall, createdate)
            cur.execute(query, params)
            conn.commit()
            
            return render_template('visitor.html', r_no=r_no, show_popup=True)

        except KeyError as e:
            print(f"Missing form field: {e}")
            return "Form submission error: Missing field.", 400

    return render_template('visitor.html')
@app.route('/seminar', methods=['GET','POST'])
def seminar():
    if request.method == 'POST':
        try:
            fname = request.form['fn']
            lname = request.form['ln']
            phone = request.form['ph']
            email = request.form.get('email','')
            sector = request.form.get('is','')
            semi = request.form.get('semi','')
            purpose = request.form.get('pv','')
            gender = request.form.get('gender','')
            age = request.form.get('age','')
            state = request.form.get('state','')
            district = request.form.get('dis','')
            cmt = request.form.get('cmt','')
 # Generate a random UUID for the ID field
            random_id = str(uuid.uuid4())
            rt='SEMINAR_ATTENDEE'
            if rt.upper()=='SEMINAR_ATTENDEE':
                prefix='SEM2'
            else:
                prefix = rt[:3].upper()  # First three letters, uppercase
            if visitor:
                ismorestall=0
            else:
                ismorestall=1
            createdate=datetime.now()
            # Fetch the current running number and increment it
            query = "SELECT MAX(RegistrationRunningNo) FROM registrationmaster WHERE RegitrationType = %s"
            cur.execute(query, (rt,))
            result = cur.fetchone()
            current_no = result[0] if result[0] else 0  # Start from 10000 if none exists
            new_no = current_no + 1
            r_no = f"{prefix}{new_no:05}"  # Add leading zeros

            # Insert into the database
            query = '''
                INSERT INTO registrationmaster (ID,RegitrationType,RegistrationNoPrefix,RegistrationNo,RegistrationRunningNo,FirstName,LastName,Gender,Age,Phone,Email,District,State,InterestedSector,PurposeOfParticipation,CreatedBy,CreatedByUserName,IsMoreStallsReq,CreatedDate,Seminars)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            params = (random_id,rt,prefix,r_no,new_no,fname,lname,gender,age,phone,email,district,state,sector,purpose,random_id,fname+" " +lname,ismorestall,createdate,semi)

            print("Executing Query:")
            print(query % params)  # Log the query with values

            cur.execute(query, params)
            conn.commit()
            return "Data inserted successfully!"
        except Exception as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data into the database", 500
    return render_template('seminar.html')

@app.route('/exhibitor', methods=['GET', 'POST'])
def exhibitor():
    if request.method == 'POST':
        try:
            # Capture form data with error handling
            fname = request.form['fn']
            lname = request.form['ln']
            phone = request.form['ph']
            email = request.form.get('email', '')
            company = request.form.get('cn', '')
            btype = request.form.get('ec', '')
            gender = request.form.get('gender', '')
            age = request.form.get('age', '')
            state = request.form.get('state', '')
            district = request.form.get('dis', '')
            category = request.form.get('na', '')
            year = request.form.get('ye', '')
            turnover = request.form.get('bt', '')
            udy = request.form.get('uri', '')
            gst = request.form.get('gst', '')
            des = request.form.get('des', '')
            cmt = request.form.get('cmt', '')

            # Generate random ID for the user
            random_id = str(uuid.uuid4())
            rt = 'EXHIBITOR'
            prefix = 'EXH3'  # Fixed prefix for EXHIBITOR

            # Determine ismorestallreq based on the selected category
            if category in ["buyer", "Entrepreneur"]:  # Assuming these categories require more stalls
                ismorestall = 0
            else:
                ismorestall = 1

            createdate = datetime.now()

            # Fetch the current running number and increment it
            query = "SELECT MAX(RegistrationRunningNo) FROM registrationmaster WHERE RegitrationType = %s"
            cur.execute(query, (rt,))
            result = cur.fetchone()
            current_no = result[0] if result[0] else 0  # Start from 10000 if none exists
            new_no = current_no + 1
            r_no = f"{prefix}{new_no:05}"  # Add leading zeros

            # Debugging: Print query and params before execution
            print(f"Executing Query: {query}")
            print(f"Params: {random_id}, {rt}, {prefix}, {r_no}, {new_no}, {fname}, {lname}, {gender}, {age}, {phone}, {email}, {district}, {state}, {company}, {btype}, {category}, {year}, {turnover}, {udy}, {gst}, {des}, {random_id}, {ismorestall}, {createdate}")

            # Insert into the database
            query = '''
                INSERT INTO registrationmaster (
                    ID, RegitrationType, RegistrationNoPrefix, RegistrationNo, 
                    RegistrationRunningNo, FirstName, LastName, Gender, Age, Phone, 
                    Email, District, State, CompanyName, BusinessCategory, BusinessType, 
                    YearEstablished, BusinessTurnOver, UdyogRegistrationId, GSTNumber, 
                    DescriptionOfProducts, CreatedBy, IsMoreStallsReq, CreatedDate
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            params = (random_id, rt, prefix, r_no, new_no, fname, lname, gender, age, phone, 
                      email, district, state, company, btype, category, year, turnover, 
                      udy, gst, des, random_id, ismorestall, createdate)
            
            # Execute the query and commit the transaction
            cur.execute(query, params)
            conn.commit()

            return "Data inserted successfully!"
        except Exception as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data into the database", 500
    return render_template('exhibitor.html')
@app.route('/others', methods=['GET', 'POST'])
def others():
    if request.method == 'POST':
        fname = request.form['fn']
        lname = request.form['ln']
        phone = request.form['ph']
        email = request.form.get('email', '')
        category = request.form.get('oc', '')
        gender = request.form['gender']
        age = request.form['age']
        state = request.form['state']
        district = request.form['dis']
       
        # Generate a random ID
        random_id = str(uuid.uuid4())

        # Check if the random ID already exists in the database
        query_check_id = "SELECT COUNT(*) FROM registrationmaster WHERE ID = %s"
        cur.execute(query_check_id, (random_id,))
        existing_id_count = cur.fetchone()[0]

        # If the ID already exists, regenerate the UUID
        while existing_id_count > 0:
            random_id = str(uuid.uuid4())
            cur.execute(query_check_id, (random_id,))
            existing_id_count = cur.fetchone()[0]
        
        rt = 'OTHERS'
        if rt.upper() == 'OTHERS':
            prefix = 'OTH4'
        else:
            prefix = rt[:3].upper()  # First three letters, uppercase

        # Handle the `ismorestall` variable
        ismorestall = 0 if visitor else 1
        
        createdate = datetime.now()
        
        # Fetch the current running number and increment it
        query = "SELECT MAX(RegistrationRunningNo) FROM registrationmaster WHERE RegitrationType = %s"
        cur.execute(query, (rt,))
        result = cur.fetchone()
        current_no = result[0] if result[0] else 0  # Start from 10000 if none exists
        new_no = current_no + 1
        r_no = f"{prefix}{new_no:05}"  # Add leading zeros

        # Insert into the database
        query_insert = '''
            INSERT INTO registrationmaster (ID, RegitrationType, RegistrationNoPrefix, RegistrationNo, RegistrationRunningNo, FirstName, LastName, Gender, Age, Phone, Email, District, State, OthersCategory, CreatedBy, CreatedByUserName, IsMoreStallsReq, CreatedDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (random_id, rt, prefix, r_no, new_no, fname, lname, gender, age, phone, email, district, state, category, random_id, fname + " " + lname, ismorestall, createdate)
        cur.execute(query_insert, params)
        conn.commit()

    return render_template('others.html')

# Make sure the static folder exists for saving the images
app.config['UPLOAD_FOLDER'] = 'static/images/'
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('ph')  # Get phone number from the form
        
        # Query the database to find the visitor with the given phone number
        query = """SELECT FirstName, LastName,Phone, Email, VisitorCategory, State, District, RegistrationNo
                   FROM registrationmaster WHERE Phone = %s and RegitrationType='VISITOR'"""
        cur.execute(query, (phone,))
        result = cur.fetchone()  # Get the first matching record
        
        if result:
            # If a record is found, extract the registration number
            registration_no = result[7]
            
            # Generate QR code for the RegistrationNo
            img = generate_qr_code(registration_no)

            # Prepare visitor data for rendering the template
            visitor_data = {
                'fname': result[0],  # Concatenate first and last name
                'lname': result[1],
                'phone': result[2],  # Correctly assign the phone number here
                'email': result[3],  # The email should be assigned to the correct index (usually 10th column)
                'category': result[4],
                'state': result[5],
                'district': result[6],
                'visitor_id': registration_no,  # Pass the registration number to the template
            }

            # Pass the visitor data and QR code image URL to the template
            return render_template('details.html', visitor=visitor_data, qr_code_img=img)
        else:
            flash("No visitor found with the given phone number.", "error")
            return redirect('/register')
    
    # Render the search form if no form submission
    return render_template('registration.html')
def generate_qr_code(registration_no):
    # Create the directory if it doesn't exist
    img_dir = 'vijay/static/images'
    
    # Debugging: Check if the directory exists and log it
    if not os.path.exists(img_dir):
        print(f"Directory {img_dir} does not exist. Creating it.")
        os.makedirs(img_dir)
    else:
        print(f"Directory {img_dir} already exists.")
    
    # Construct the path for saving the image
    img_path = os.path.join(img_dir, f'visitor_{registration_no}_qr.png')
    
    # Debugging: Log the path where the image will be saved
    print(f"Saving QR Code to: {img_path}")
    
    try:
        # Generate the QR code for the registration number
        img = qrcode.make(registration_no)
        
        # Save the generated image to the specified path
        img.save(img_path)
        
        print(f"QR Code successfully generated and saved at: {img_path}")  # Debugging print
    except Exception as e:
        print(f"Error generating QR code: {e}")  # Catch any errors and print them
    
    return img_path  # Return the path to the saved image

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    print('Login page accessed')
    if request.method == 'POST':
        print('Form submitted')
        username = request.form['username']
        password = request.form['password']
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session['admin_logged_in'] = True
            print('Login successful')
            return redirect(url_for('admin_dashboard'))
        else:
            print('Invalid credentials')
            flash('Invalid username or password', 'error')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))  # Redirect to login if not logged in

    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cursor = conn.cursor(dictionary=True)
        
        # Query data from the registrationmaster table
        cursor.execute("SELECT COUNT(*) AS total FROM registrationmaster")
        total_registrations = cursor.fetchone()['total']
        
        # Query breakdown of different categories
        cursor.execute("SELECT COUNT(*) AS total FROM registrationmaster WHERE RegitrationType = 'visitor'")
        visitors = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) AS total FROM registrationmaster WHERE RegitrationType = 'SEMINAR_ATTENDEE'")
        seminar_attendees = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) AS total FROM registrationmaster WHERE RegitrationType = 'EXHIBITORS'")
        exhibitors = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) AS total FROM registrationmaster WHERE RegitrationType = 'others'")
        others = cursor.fetchone()['total']

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"An error occurred while connecting to the database: {err}", 500
    finally:
        # Close database connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

    # Pass data to the template
    return render_template(
        'admin_dashboard.html',
        total_registrations=total_registrations,
        visitors=visitors,
        seminar_attendees=seminar_attendees,
        exhibitors=exhibitors,
        others=others
    )

@app.route('/data/registrations')
def registration_data():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cursor = conn.cursor(dictionary=True)  # Use dictionary for better readability

        # Query for registration counts grouped by type
        cursor.execute("""
            SELECT RegitrationType, COUNT(*) AS Count
            FROM registrationmaster
            GROUP BY RegitrationType
        """)
        result = cursor.fetchall()

        # Prepare data for the frontend
        labels = [row['RegitrationType'] for row in result]  # ['Visitor', 'Seminar Attendee', 'Exhibitor', 'Others']
        counts = [row['Count'] for row in result]  # [count1, count2, count3, count4]

        return jsonify({'labels': labels, 'counts': counts})
    except Exception as e:
        print(f"Error fetching registration data: {e}")
        return jsonify({'error': 'An error occurred while fetching registration data.'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()



@app.route('/data/gender')
def gender_data():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cur = conn.cursor()

        # Execute individual queries for each gender
        queries = {
            'Male': "SELECT COUNT(*) FROM registrationmaster WHERE Gender = 'e449de32-a931-11ee-a117-00155e1f5d07'",
            'Female': "SELECT COUNT(*) FROM registrationmaster WHERE Gender = 'e449dfed-a931-11ee-a117-00155e1f5d07'",
            'Transgender': "SELECT COUNT(*) FROM registrationmaster WHERE Gender = 'e449e0e8-a931-11ee-a117-00155e1f5d07'"
        }

        labels = []
        counts = []

        for gender, query in queries.items():
            cur.execute(query)
            count = cur.fetchone()[0]  # Get the count result from the query
            labels.append(gender)
            counts.append(count)

        # Return the data as JSON
        return jsonify({'labels': labels, 'counts': counts})

    except mysql.connector.Error as db_err:
        print(f"Database Error: {db_err}")  # Logs detailed database errors
        return jsonify({'error': 'Database error occurred.'}), 500
    except Exception as e:
        print(f"General Error: {e}")  # Logs general errors
        return jsonify({'error': 'An error occurred while fetching gender data.'}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()





@app.route('/data/exhibitor')
def get_exhibitor_data():
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cur = connection.cursor()

        # Query to fetch the status of exhibitors
        cur.execute("SELECT IsStallApprove FROM registrationmaster")
        statuses = [row[0] for row in cur.fetchall()]

        return jsonify({'IsStallApprove': statuses})

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': f'Database error: {err}'}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()



@app.route('/data/stall_booked_chart', methods=['GET'])
def get_stall_booked_chart():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
             host="tnbeat2025.pixoustech.in",
    user="hei3blcfx7yy",
    password="Pixoustech@2023",
    database= "tnbeatexpo_registration",
        )
        cur = conn.cursor(dictionary=True)
        
        # Query to get booked and total stalls
        query_booked = "SELECT COUNT(*) AS booked_stalls FROM slotmaster WHERE IsBooked = 1"
        query_total = "SELECT COUNT(*) AS total_stalls FROM slotmaster"
        
        cur.execute(query_booked)
        booked_result = cur.fetchone()
        
        cur.execute(query_total)
        total_result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        # Prepare labels and counts
        booked_stalls = booked_result['booked_stalls']
        total_stalls = total_result['total_stalls']
        available_stalls = total_stalls - booked_stalls

        labels = ["Booked", "Available"]
        counts = [booked_stalls, available_stalls]
        
        # Return data as JSON
        return jsonify({"labels": labels, "counts": counts})
    except Exception as e:
        print(f"Error fetching stall chart data: {e}")
        return jsonify({"error": "Failed to fetch stall chart data"}), 500




@app.route('/data/age_registration', methods=['GET'])
def get_age_registration():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
    host="tnbeat2025.pixoustech.in",
    user="hei3blcfx7yy",
    password="Pixoustech@2023",
    database= "tnbeatexpo_registration",
        )
        cur = conn.cursor(dictionary=True)

        # Query to calculate age-wise registration
        query = """
        SELECT 
            CASE
                WHEN age BETWEEN 0 AND 18 THEN '0-18'
                WHEN age BETWEEN 19 AND 25 THEN '19-25'
                WHEN age BETWEEN 26 AND 35 THEN '26-35'
                WHEN age BETWEEN 36 AND 50 THEN '36-50'
                ELSE '51+'
            END AS age_group,
            COUNT(*) AS count
        FROM registrationmaster
        GROUP BY age_group
        ORDER BY age_group
        """
        cur.execute(query)
        results = cur.fetchall()

        # Debugging: Print results in server logs
        print("Age-wise Data:", results)

        # Close the connection
        cur.close()
        conn.close()

        # Return JSON response
        return jsonify(results)
    except Exception as e:
        # Log and return error message
        print(f"Error fetching age-wise registration data: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500



@app.route('/data/new_registrations', methods=['GET'])
def get_new_registrations():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
    user="hei3blcfx7yy",
    password="Pixoustech@2023",
    database= "tnbeatexpo_registration",
        )
        cur = conn.cursor(dictionary=True)
        
        # Query to get new registrations
        query = """
        SELECT COUNT(*) AS new_registrations
        FROM registrationmaster
        WHERE DATE(CreatedDate) = CURDATE()
        """
        
        cur.execute(query)
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        # Prepare the data for response
        new_registrations = result['new_registrations']
        
        # Return data as JSON
        return jsonify({"new_registrations": new_registrations})
    
    except Exception as e:
        print(f"Error fetching new registrations: {e}")
        return jsonify({"error": "Failed to fetch new registrations"}), 500




@app.route('/registration', methods=['GET', 'POST'])
def registration():
    conn = None
    cur = None
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )

        # Create a cursor with dictionary results for easy access
        cur = conn.cursor(dictionary=True)

        # Fetch distinct registration types for the filter dropdown
        cur.execute("SELECT DISTINCT RegitrationType FROM registrationmaster")
        registrationtypes = cur.fetchall()

        # Fetch distinct states for the filter dropdown
        cur.execute("SELECT DropDownValue FROM dropdownmaster WHERE DropDownType='STATE'")
        states = cur.fetchall()

        # Fetch distinct districts for the filter dropdown
        cur.execute("SELECT DropDownValue FROM dropdownmaster WHERE DropDownType='DISTRICT'")
        districts = cur.fetchall()

        # SQL query to fetch registration data, joining with gender, state, and district values
        if request.method == 'POST':
            selected_type = request.form.get('registrationtype')
            selected_state = request.form.get('state')
            selected_district = request.form.get('district')

            # Create the dynamic query with joins to get values instead of IDs
            query = """
                SELECT 
                    r.FirstName, r.LastName, r.RegitrationNo, r.RegitrationType, 
                    r.Email, r.Phone, 
                    g.DropDownValue AS Gender,  -- Use DropDownValue for gender
                    s.DropDownValue AS State, 
                    d.DropDownValue AS District
                FROM 
                    registrationmaster r
                    LEFT JOIN dropdownmaster g ON r.Gender = g.ID AND g.DropDownType = 'GENDER'
                    LEFT JOIN dropdownmaster s ON r.State = s.ID AND s.DropDownType = 'STATE'
                    LEFT JOIN dropdownmaster d ON r.District = d.ID AND d.DropDownType = 'DISTRICT'
                WHERE 1=1
            """

            filters = []

            if selected_type:
                query += " AND r.RegitrationType = %s"
                filters.append(selected_type)
            if selected_state:
                query += " AND r.State = %s"
                filters.append(selected_state)
            if selected_district:
                query += " AND r.District = %s"
                filters.append(selected_district)

            cur.execute(query, tuple(filters))
        else:
            # Default query to fetch all registrations with actual values
            cur.execute("""
                SELECT 
                    r.FirstName, r.LastName, r.RegitrationNo, r.RegitrationType, 
                    r.Email, r.Phone, 
                    g.DropDownValue AS Gender, 
                    s.DropDownValue AS State, 
                    d.DropDownValue AS District
                FROM 
                    registrationmaster r
                    LEFT JOIN dropdownmaster g ON r.Gender = g.ID AND g.DropDownType = 'GENDER'
                    LEFT JOIN dropdownmaster s ON r.State = s.ID AND s.DropDownType = 'STATE'
                    LEFT JOIN dropdownmaster d ON r.District = d.ID AND d.DropDownType = 'DISTRICT'
            """)

        # Fetch all the registration data
        registrations = cur.fetchall()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return f"Database connection error: {err}"

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return f"An unexpected error occurred: {e}"

    finally:
        # Ensure the cursor and connection are closed, if they were opened
        if cur:
            cur.close()
        if conn:
            conn.close()

    # Return the template with the registration data and filter options
    return render_template(
        'registrations.html',
        registrations=registrations,
        registrationtypes=registrationtypes,
        states=states,
        districts=districts
    )





@app.route('/details/<registration_no>', methods=['GET'])
def visitor_details(registration_no):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
    user="hei3blcfx7yy",
    password="Pixoustech@2023",
    database= "tnbeatexpo_registration",
        )
        cur = conn.cursor(dictionary=True)

        # Fetch visitor details based on the registration number
        cur.execute("SELECT * FROM registrationmaster WHERE RegistrationNo = %s", (registration_no,))
        visitor = cur.fetchone()


        # If no record is found, return a 404 or error message
        if not visitor:
            return "Visitor not found", 404

        # Close the database connection
        cur.close()
        conn.close()

        # Render the template for visitor details and pass the visitor data
        return render_template('details.html', visitors=visitor)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Database connection error occurred. Please try again later."

logging.basicConfig(level=logging.DEBUG)
@app.route('/stall_allocation', methods=['GET'])
def stall_allocation():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        logging.info("Successfully connected to the database.")
        
        # Create a cursor with dictionary results for easy access
        cur = conn.cursor(dictionary=True)

        # Fetch distinct values for dropdowns
        dropdown_query = {
           "Gender": "SELECT id, dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'GENDER'",
    "BusinessCategory": "SELECT id, dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'BUSINESSCATEGORY'",
    "State": "SELECT id, dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'STATE'",
    "District": "SELECT id, dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'DISTRICT'"
        }

        dropdowns = {}
        for key, query in dropdown_query.items():
            cur.execute(query)
            dropdowns[key] = cur.fetchall()

        # Get filters from request arguments
        gender_filter = request.args.get('gender', None)
        status_filter = request.args.get('status', None)
        category_filter = request.args.get('category', None)
        state_filter = request.args.get('state', None)
        district_filter = request.args.get('district', None)

        logging.info(f"Received filters: gender={gender_filter}, status={status_filter}, category={category_filter}, state={state_filter}, district={district_filter}")

        # Build exhibitor query to show all EXHIBITOR data
        exhibitors_query = """
            SELECT 
                r.FirstName, 
                r.LastName, 
                r.RegitrationNo, 
                r.Email, 
                r.Phone, 
                g.dropdownvalue AS Gender, 
                s.dropdownvalue AS State, 
                d.dropdownvalue AS District, 
                bc.dropdownvalue AS BusinessCategory, 
                r.IsStallApprove
            FROM 
                registrationmaster r
            LEFT JOIN 
                dropdownmaster g ON r.Gender = g.id AND g.dropdowntype = 'GENDER'
            LEFT JOIN 
                dropdownmaster s ON r.State = s.id AND s.dropdowntype = 'STATE'
            LEFT JOIN 
                dropdownmaster d ON r.District = d.id AND d.dropdowntype = 'DISTRICT'
            LEFT JOIN 
                dropdownmaster bc ON r.BusinessCategory = bc.id AND bc.dropdowntype = 'BUSINESSCATEGORY'
            LEFT JOIN 
                slotmaster sm ON r.RegitrationNo = sm.RegistrationId  # Join with slotmaster to get stall booking status
            WHERE 
                r.RegitrationType = 'EXHIBITORS'  # Only exhibitors
        """

        filters = []
        parameters = []

        # Add filters based on the selected values (parameterized queries to avoid SQL injection)
        if gender_filter:
            filters.append("r.Gender = %s")
            parameters.append(gender_filter)
        
        if status_filter:
            if status_filter == "approved":
                filters.append("r.IsStallApprove = %s")
                parameters.append(1)  # Approved
            elif status_filter == "rejected":
                filters.append("r.IsStallApprove = %s")
                parameters.append(0)  # Rejected
            elif status_filter == "exhibitor":
                filters.append("r.IsStallApprove = %s")
                parameters.append(2)  # Exhibitor (pending)
            elif status_filter == "stall_booked":
                filters.append("sm.IsBooked = %s")  # Stall is booked
                parameters.append(1)  # IsBooked = 1 means booked

        if category_filter:
            filters.append("r.BusinessCategory = %s")
            parameters.append(category_filter)
        if state_filter:
            filters.append("r.State = %s")
            parameters.append(state_filter)
        if district_filter:
            filters.append("r.District = %s")
            parameters.append(district_filter)

        # Apply filters if any
        if filters:
            exhibitors_query += " AND " + " AND ".join(filters)

        # Log the final query and parameters to debug
        logging.info(f"Final SQL Query: {exhibitors_query}")
        logging.info(f"Parameters: {parameters}")

        # Execute the query with parameters to prevent SQL injection
        cur.execute(exhibitors_query, tuple(parameters))
        exhibitors = cur.fetchall()

        # Log the results to verify
        logging.info(f"Fetched exhibitors: {exhibitors}")

        # Close the cursor and the connection
        cur.close()
        conn.close()

        # Render the template with the fetched data
        return render_template(
            'stall_allocation.html',
            exhibitors=exhibitors,
            dropdowns=dropdowns,
            gender_filter=gender_filter,
            status_filter=status_filter,
            category_filter=category_filter,
            state_filter=state_filter,
            district_filter=district_filter,
        )

    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        return f"An error occurred while connecting to the database: {err}", 500
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return f"An unexpected error occurred: {e}", 500


@app.route('/stall_allocation/<action>', methods=['POST'])
def update_exhibitor_status(action):
    """Update the IsStallApprove status and handle redirection for approval."""
    connection = None
    cur = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cur = connection.cursor()

        # Get the Registration Number from the form
        registration_no = request.form.get('registration_no')
        if not registration_no:
            return jsonify({'success': False, 'message': 'Registration number is missing'}), 400

        if action == 'approve':
            # Update the exhibitor's status to approved
            cur.execute("""
                UPDATE registrationmaster 
                SET IsStallApprove = 1 
                WHERE RegitrationNo = %s
            """, (registration_no,))
        elif action == 'reject':
            # Update the exhibitor's status to rejected
            cur.execute("""
                UPDATE registrationmaster 
                SET IsStallApprove = 0 
                WHERE RegitrationNo = %s
            """, (registration_no,))
        else:
            return jsonify({'success': False, 'message': 'Invalid action'}), 400

        # Commit the transaction
        connection.commit()

        # Return success response for AJAX
        if action == 'approve':
            return jsonify({'success': True, 'redirect_url': url_for('book_stall_page', registration_no=registration_no)})
        return jsonify({'success': True})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Database error: {err}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()




@app.route('/stall_booking/<registration_no>')
def book_stall_page(registration_no):
    """Render the stall booking page with slot information."""
    connection = None
    cur = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cur = connection.cursor(dictionary=True)

        # Fetch all slots from the slotmaster table
        cur.execute("SELECT SlotNumber, IsBooked FROM slotmaster")
        slots = cur.fetchall()

        # Format slot data for easier frontend rendering
        for slot in slots:
            slot['id'] = f"{slot['SlotNumber']}"

        # Pass slot details and registration number to the template
        return render_template('book_stall.html', slots=slots, registration_no=registration_no)

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return f"Database error: {err}", 500
    except Exception as e:
        print(f"General Error: {e}")
        return f"An error occurred: {e}", 500
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()


@app.route('/book_stall', methods=['POST'])
def book_stall():
    """Handle stall booking and update the slotmaster table."""
    try:
        # Parse JSON data from the frontend
        data = request.json
        print("Received data:", data)  # Debug log

        # Validate required fields
        required_fields = ['stallId', 'registrationId', 'modifiedByUserName', 'modifiedBy']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Invalid data provided. Missing fields: {', '.join(missing_fields)}",
                "registrationId": data.get('registrationId')  # Return the provided registrationNo, if any
            }), 400

        # Extract data for processing
        stall_id = data['stallId']
        registration_no = data['registrationId']
        modified_by_username = data['modifiedByUserName']
        modified_by = data['modifiedBy']

        # Connect to the database
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cur = connection.cursor(dictionary=True)

        # Check if the stall exists
        cur.execute("SELECT * FROM slotmaster WHERE SlotNumber = %s", (stall_id,))
        result = cur.fetchone()

        if not result:
            return jsonify({
                "success": False,
                "message": f"Stall ID {stall_id} not found.",
                "registrationId": registration_no
            }), 404

        # Check if the stall is already booked
        if result['IsBooked']:
            return jsonify({
                "success": False,
                "message": f"Stall ID {stall_id} is already booked.",
                "registrationId": registration_no
            }), 400

        # Update the stall to mark it as booked
        cur.execute("""
            UPDATE slotmaster
            SET IsBooked = 1,
                RegistrationId = %s,
                ModifiedDate = NOW(),
                ModifiedByUserName = %s,
                ModifiedBy = %s
            WHERE SlotNumber = %s
        """, (registration_no, modified_by_username, modified_by, stall_id))
        connection.commit()

        # Return success response
        return jsonify({
            "success": True,
            "message": f"Stall {stall_id} successfully booked.",
            "registrationId": registration_no
        }), 200

    except mysql.connector.Error as db_error:
        print(f"Database Error: {db_error}")
        return jsonify({
            "success": False,
            "message": "A database error occurred.",
            "error": str(db_error),
            "registrationId": data.get('registrationId')
        }), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
            "error": str(e),
            "registrationId": data.get('registrationId')
        }), 500
    finally:
        try:
            if cur:
                cur.close()
            if connection:
                connection.close()
        except NameError:
            pass  # Handles the case where `connection` or `cur` doesn't exist


@app.route('/check_slot_status', methods=['GET'])
def check_slot_status():
    """Check the status of a specific slot (whether it is booked or available)."""
    
    # Get the slot number from the query parameter
    slot_number = request.args.get('slotNumber')
    
    if not slot_number:
        return jsonify({"success": False, "message": "Slot number is required."}), 400
    
    # Database connection
    try:
        connection = mysql.connector.connect(
          host="tnbeat2025.pixoustech.in",
    user="hei3blcfx7yy",
    password="Pixoustech@2023",
    database= "tnbeatexpo_registration",
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Query to check slot status
        cursor.execute("SELECT SlotNumber, IsBooked FROM slotmaster WHERE SlotNumber = %s", (slot_number,))
        result = cursor.fetchone()

        # If no slot found, return an error message
        if not result:
            return jsonify({"success": False, "message": f"Slot number {slot_number} not found"}), 404
        
        # Determine the status based on IsBooked value
        status = "Booked" if result['IsBooked'] else "Available"
        
        # Return the slot status in a JSON response
        return jsonify({
            "success": True, 
            "message": f"Slot {slot_number} is {status}",
            "status": status
        }), 200

    except mysql.connector.Error as err:
        # If there is a database error, return a 500 error
        return jsonify({"success": False, "message": "Database error", "error": str(err)}), 500
    except Exception as e:
        # Catch any other general exceptions
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500
    finally:
        # Clean up database resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/filter_slots', methods=['GET'])
def filter_slots():
    """Filter slots based on status (Available or Booked)."""
    status_filter = request.args.get('status')  # Get the filter type (e.g., "available", "booked", or "all")

    if status_filter not in ['available', 'booked', 'all']:
        return jsonify({"success": False, "message": "Invalid filter value. Use 'available', 'booked', or 'all'."}), 400

    try:
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
    user="hei3blcfx7yy",
    password="Pixoustech@2023",
    database= "tnbeatexpo_registration",
        )
        cursor = connection.cursor(dictionary=True)

        # Query based on filter
        if status_filter == 'available':
            cursor.execute("SELECT SlotNumber, IsBooked FROM slotmaster WHERE IsBooked = 0")
        elif status_filter == 'booked':
            cursor.execute("SELECT SlotNumber, IsBooked FROM slotmaster WHERE IsBooked = 1")
        else:  # status_filter == 'all'
            cursor.execute("SELECT SlotNumber, IsBooked FROM slotmaster")

        results = cursor.fetchall()

        # Format the response
        slots = [{"SlotNumber": row["SlotNumber"], "Status": "Booked" if row["IsBooked"] else "Available"} for row in results]

        return jsonify({"success": True, "slots": slots}), 200

    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": "Database error", "error": str(err)}), 500
    except Exception as e:
        return jsonify({"success": False, "message": "An error occurred", "error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
 

@app.route('/visitor_report')
def visitor_report():
    try:
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cursor = connection.cursor(dictionary=True)

        # Query to get all visitors and their visitor category
        query_visitors = """
            SELECT 
                r.FirstName, 
                r.LastName, 
                r.RegitrationNo, 
                vc.DropDownValue AS VisitorCategory,
                r.Email, 
                r.Phone, 
                g.DropDownValue AS Gender, 
                s.DropDownValue AS State, 
                d.DropDownValue AS District
            FROM 
                registrationmaster r
            LEFT JOIN dropdownmaster vc ON r.VisitorCategory = vc.ID AND vc.DropDownType = 'VISITORCATEGORY'
            LEFT JOIN dropdownmaster g ON r.Gender = g.ID AND g.DropDownType = 'GENDER'
            LEFT JOIN dropdownmaster s ON r.State = s.ID AND s.DropDownType = 'STATE'
            LEFT JOIN dropdownmaster d ON r.District = d.ID AND d.DropDownType = 'DISTRICT'
            WHERE 
                r.RegitrationType = 'VISITOR';
        """
        cursor.execute(query_visitors)
        visitors = cursor.fetchall()

        # Query to get all categories, genders, and states for filtering
        query_category = """
            SELECT DropDownValue 
            FROM dropdownmaster 
            WHERE DropDownType = 'VISITORCATEGORY';
        """
        cursor.execute(query_category)
        categories = cursor.fetchall()

        query_gender = """
            SELECT DropDownValue 
            FROM dropdownmaster 
            WHERE DropDownType = 'GENDER';
        """
        cursor.execute(query_gender)
        genders = cursor.fetchall()

        query_state = """
            SELECT DropDownValue 
            FROM dropdownmaster 
            WHERE DropDownType = 'STATE';
        """
        cursor.execute(query_state)
        states = cursor.fetchall()

        # Debugging output
        print("Visitors Data:", visitors)
        print("Categories Data:", categories)
        print("Genders Data:", genders)
        print("States Data:", states)

        cursor.close()
        connection.close()

        # Pass the data to the template
        return render_template('visitor_report.html', visitors=visitors, categories=categories, genders=genders, states=states)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error connecting to the database", 500





@app.route('/seminar_report')
def seminar_report():
    try:
        # Database connection
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cursor = connection.cursor(dictionary=True)
        
        # Fetch seminar attendees with dropdown values for categories
        query = """
            SELECT 
                r.FirstName, 
                r.LastName, 
                r.RegitrationNo, 
                sc.DropDownValue AS Seminars,
                r.Email, 
                r.Phone, 
                g.DropDownValue AS Gender, 
                s.DropDownValue AS State, 
                d.DropDownValue AS District
            FROM 
                registrationmaster r
            LEFT JOIN dropdownmaster sc ON r.Seminars = sc.ID AND sc.DropDownType = 'Seminars'
            LEFT JOIN dropdownmaster g ON r.Gender = g.ID AND g.DropDownType = 'GENDER'
            LEFT JOIN dropdownmaster s ON r.State = s.ID AND s.DropDownType = 'STATE'
            LEFT JOIN dropdownmaster d ON r.District = d.ID AND d.DropDownType = 'DISTRICT'
            WHERE 
                r.RegitrationType = 'SEMINAR_ATTENDEE';
        """
        
        cursor.execute(query)
        seminars = cursor.fetchall()

        # Fetch dropdown data for filters
        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'GENDER'")
        genders = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'STATE'")
        states = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'DISTRICT'")
        districts = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'Seminars'")
        categories = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Render the HTML template with data
        return render_template(
            'seminar_report.html',
            seminars=seminars,
            genders=genders,
            states=states,
            districts=districts,
            categories=categories
        )

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error connecting to the database", 500






@app.route('/exhibitor_report')
def exhibitor_report():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cursor = connection.cursor(dictionary=True)

        # Fetch dropdown values for Gender, State, District, and Categories
        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'GENDER'")
        genders = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'STATE'")
        states = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'DISTRICT'")
        districts = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'BUSINESSCATEGORY'")
        categories = cursor.fetchall()

        # Fetch exhibitor details with the values (not IDs)
        query = """
            SELECT 
                r.FirstName, 
                r.LastName, 
                r.RegitrationNo, 
                bc.DropDownValue AS BusinessCategory,
                r.Email, 
                r.Phone, 
                g.DropDownValue AS Gender, 
                s.DropDownValue AS State, 
                d.DropDownValue AS District
            FROM 
                registrationmaster r
            LEFT JOIN dropdownmaster bc ON r.BusinessCategory = bc.ID AND bc.DropDownType = 'BUSINESSCATEGORY'
            LEFT JOIN dropdownmaster g ON r.Gender = g.ID AND g.DropDownType = 'GENDER'
            LEFT JOIN dropdownmaster s ON r.State = s.ID AND s.DropDownType = 'STATE'
            LEFT JOIN dropdownmaster d ON r.District = d.ID AND d.DropDownType = 'DISTRICT'
            WHERE 
                r.RegitrationType = 'EXHIBITORS';
        """

        cursor.execute(query)
        exhibitors = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Pass the exhibitors and dropdown values to the HTML template
        return render_template('exhibitor_report.html', exhibitors=exhibitors, 
                               genders=genders, states=states, districts=districts, categories=categories)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error connecting to the database", 500




@app.route('/others_report')
def others_report():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="tnbeat2025.pixoustech.in",
            user="hei3blcfx7yy",
            password="Pixoustech@2023",
            database="tnbeatexpo_registration",
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch distinct dropdown values for Gender, State, District, and Others Category
        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'GENDER'")
        genders = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'STATE'")
        states = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'DISTRICT'")
        districts = cursor.fetchall()

        cursor.execute("SELECT DISTINCT dropdownvalue FROM dropdownmaster WHERE dropdowntype = 'OthersCategory'")
        categories = cursor.fetchall()

        # Query to fetch 'Others' data with Gender, State, District, and OthersCategory values
        query = """
            SELECT 
                r.FirstName, 
                r.LastName, 
                r.RegitrationNo, 
                oc.DropDownValue AS OthersCategory,
                r.Email, 
                r.Phone, 
                g.DropDownValue AS Gender, 
                s.DropDownValue AS State, 
                d.DropDownValue AS District
            FROM 
                registrationmaster r
            LEFT JOIN dropdownmaster oc ON r.OthersCategory = oc.ID AND oc.DropDownType = 'OthersCategory'
            LEFT JOIN dropdownmaster g ON r.Gender = g.ID AND g.DropDownType = 'GENDER'
            LEFT JOIN dropdownmaster s ON r.State = s.ID AND s.DropDownType = 'STATE'
            LEFT JOIN dropdownmaster d ON r.District = d.ID AND d.DropDownType = 'DISTRICT'
            WHERE 
                r.RegitrationType = 'OTHERS';
        """

        cursor.execute(query)
        others = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Pass the 'others', 'genders', 'states', 'districts', and 'categories' data to the template
        return render_template(
            'others_report.html', 
            others=others, 
            genders=genders, 
            states=states, 
            districts=districts, 
            categories=categories
        )

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error connecting to the database", 500






@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)  # Remove the session
    return redirect(url_for('admin_login'))  # Redirect to the login page


if __name__ == '__main__':
    app.run(debug=True, port=5001)