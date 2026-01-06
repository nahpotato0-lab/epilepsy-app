import mysql.connector
import hashlib
import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import lzma
from django.db import models
import time
def write_to_file(bigdata):
    with open("D:/testvid.mp4", 'wb') as f:
        f.write(bigdata)
        print("data written")

# Configuration for MySQL connection
DB_CONFIG = {
    'user': 'root',
    'password': 'sql123',
    'host': '127.0.0.1',
    'database': 'darsh',
    'raise_on_warnings': True,
    # buffer_result is often needed when fetching large BLOBs
    # ensuring the connector doesn't timeout or run OOM easily
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def index(request):
    """
    Renders the list of videos. 
    Note: We do NOT fetch the 'movie' BLOB here to save bandwidth.
    """
    videos = []
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)
        
        # Select only metadata, not the heavy blob
        query = "SELECT hash, title, time_uploaded FROM epilepsy ORDER BY time_uploaded DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Transform data for the template
        for row in rows:
            videos.append({
                'title': row['title'],
                'uploaded_at': row['time_uploaded'],
                # We generate a virtual URL that points to our stream_video view
                'file_path': f"/stream/{int(row['hash'])}"
            })
            
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        
    return render(request, 'player.html', {'videos': videos})

def stream_video(request, video_hash):
    """
    Retrieves the binary BLOB from MySQL and streams it to the client.
    """
    print("stream called with hash- ", video_hash)   
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(buffered=True)
        
        # Fetch the actual video binary
        query = "SELECT movie FROM epilepsy WHERE hash = %s"
        print("Ive been called")
        cursor.execute(query, (video_hash,))
        row = cursor.fetchall()
        print("called, fetched")
        cursor.close()
        cnx.close()
        print(type(row))
        if row:
            rows = [x for x in row]
            print(type(rows[0][0]))
            write_to_file(rows[0][0])
            video_data = bytes(rows[0][0])
            # Return the binary data with video MIME type
            return HttpResponse(video_data, content_type='video/mp4')
        else:
            raise Http404("Video not found")
            
    except mysql.connector.Error:
        return HttpResponse("Database Error", status=500)

def upload_video(request):
    """
    Handles file upload and insertion into the new schema format.
    """
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']
        title = request.POST.get('title', 'Untitled')
        
        # 1. Read file into memory (binary)
        # Note: Large files might require chunking or stream reading in production
        movie_blob = video_file.read()
        assert movie_blob is not None
        

        # 2. Generate Metadata
        now = datetime.datetime.now()
        
        # Generate UNSIGNED BIGINT hash from title + time
        # We use SHA256 and convert the first 15 chars to an int to fit in BIGINT
        hash_input = f"{title}{now}".encode('utf-8')
        hash_val = int(hashlib.sha256(hash_input).hexdigest()[:15], 16)
        

        movie_blob=str(movie_blob).encode('utf-8')
        # 3. Insert into MySQL
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor(buffered=True)
            with open("D:/out.mp4", 'wb') as f:
                f.write(movie_blob)
            
            query = """
                INSERT INTO epilepsy (hash, time_uploaded, title, movie) 
                VALUES (%s, %s, %s, %s)
            """.encode('utf-8')
            vals = (hash_val, now, title, movie_blob)
            
            cursor.execute(query, vals)
            cnx.commit()
            time.sleep(5)
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            return HttpResponse(f"Database Insert Error: {err}", status=500)

        return redirect('index')
    
    return redirect('index')

# ---------------------------------------------------------
# DATABASE SETUP INSTRUCTIONS
# ---------------------------------------------------------
# Run this SQL in your MySQL client to match the requested schema:
#
# CREATE TABLE videos (
#     hash BIGINT UNSIGNED PRIMARY KEY,
#     time_uploaded DATETIME NOT NULL,
#     title TEXT NOT NULL,
#     lenjson LONGTEXT,
#     movie LONGBLOB
# );
#
# IMPORTANT:
# Storing videos requires a large `max_allowed_packet` in MySQL.
# You may need to run: SET GLOBAL max_allowed_packet = 1073741824; -- (1GB)