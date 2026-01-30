# **Acknowledgement**

We am grateful for this opportunity given to us by our principal, Shefali
Ma'am, which has given real-world experience.

Working with
Python and SOL to build this website has provided us with a platform to express our in-depth knowledge in a user-friendly and approachable manner.

We would like to express our heartfelt thanks to Nimi Ma'am and Sumathi Ma'am, who have been incredible guides and have supported us throughout this project from day
zero. They have always been willing to help us overcome challenges and have provided us with the means to commit to this unconventional idea.

We would like to express our eternal gratitude to our parents, being the light that shines no matter what we set our minds to. Their emotional and *financial* support.  

Lastly, We thank our friends and classmates. They have been invaluable in providing suggestions, assistance, and support when needed, as as well as in helping us test the project.

---

# **Why choose Python?**


## According to the creators
    Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python’s elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.

## A short note on its history
Python was created in the early 1990s by Guido van Rossum at CWI in the Netherlands as a successor to ABC. The name "Python" comes from Guido's love of Monty Python's Flying Circus, not the snake. In 1995, he continued development at CNRI in Virginia. In 2000, Guido and the core team moved to BeOpen.com, then to Digital Creations (later Zope Corporation). The Python Software Foundation, a non-profit managing Python's intellectual property, was formed in 2001.

## Why did we choose Python 3.12?
- Highly readable
- One of the most extensible languages
- Compatible with many other languages.
- Portable across ABIs (Application Binary Interface)
- Open-Source under the PSF licencse (similar to BSD/GPL)

## Where else is Python used?
- Python has become the premier language for any kind of machine learning algrothm due to the massive popularity of libraries like PyTorch and TensorFlow
- Due to libraries like pandas, Python is also used extensively in the cyberfinancing regime.
- For task automation
- Used extensively in one-off research tasks due to the ease of writing code.

### We are using Python 3.13.11

---

# Project Synopsis

Epilepscreen is a website deisgned to help those with photosensitive epilepsy (which for the purposes of this document will  henceforth be reffered to by the general term epliepsy) watch media owned by them in a safe environment. This is acheived via reducing the contrast as well as the birghtness of the video on screen if a bright flash is detected.

Users can simply open the web app and upload videos to the the database and later retreive them and watch them through the desensitized video player. 

### Features- 
- The video player runs a script to detect the flashes and supresses them by lowering the contrast and the birghtness in an easily configurable way. 
- The videos are stored within the SQL database and are persistent across sessions and devices.
- The video player is very light and runs blazingly fast even on poorly capable hardware.
- Videos can be deleted form the database.

### Conclusion- 
Epilepscreen is a one-of-a-kind anti-strobe media player that allows for any epileptic person to watch media without any physical aids.

---

# System Requirements

- Python 3.10.x or higher
- Relevant modules should be installed
- MySQL database connection \ installation
- 60 KB of storage
- 5GB RAM or more
- Browser of choice

---

# Modules and functions

- Django==5.1.7
- mysql_connector_repackaged==0.3.1

---

# User Manual

### To run the application, do the following- 
- If the modules are yet to be installed, run the following command- 
    ```sh
    pip install -r requirements.txt
    ```
- For the first startup, run the sql.py file to create the databses in the expected format.
- Run the command- 
    ```sh 
    python manage.py runserver
    ```
- Access the server at the provided IP, usually 127.0.0.01:8000

---

# Structure and Functions

## Working Tree

```
epilepsy-app/
├── manage.py
├── sql.py
├── requirements.txt
├── db.sqlite3
├── mysite/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── settings.py
│   └── urls.py
├── epilepscreen/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
└── templates/
    └── player.html
```

## Module and Function Documentation

### epilepscreen/views.py
Core application logic for video management and streaming.

**Functions:**
- `get_db_connection()` - Establishes MySQL connection using configured credentials
- `index(request)` - Renders list of videos from database without loading heavy BLOBs for performance
- `stream_video(request, video_hash)` - Retrieves and streams compressed video BLOB to client as MP4
- `upload_video(request)` - Handles file uploads, generates hash IDs, compresses with LZMA, inserts into MySQL

### epilepscreen/models.py
Database schema definition using Django ORM.

**Classes:**
- `GitHub` - Model representing GitHub repository metadata with fields: hash_id (primary key), time_uploaded, filename, repo_id, repo_name, time_modified, modified_by

### epilepscreen/urls.py
URL routing configuration for the epilepscreen app.

**Routes:**
- `""` → `index` - Display video list
- `"upload/"` → `upload_video` - Handle video uploads
- `"stream/"` → `stream_video` - Stream video by hash

### epilepscreen/admin.py
Django admin interface configuration (currently empty, no models registered).

### mysite/urls.py
Main project URL dispatcher that includes epilepscreen routes and admin panel.

**Routes:**
- `""` → includes epilepscreen.urls
- `"admin/"` → Django admin interface

### mysite/settings.py
Django project configuration including database, templates, middleware, and security settings.

**Key Settings:**
- DEBUG mode enabled for development
- SQLite database configured as default
- Template directory: `BASE_DIR/templates`
- INSTALLED_APPS includes contrib and epilepscreen

### sql.py
Database initialization utility for creating MySQL tables outside of Django migrations.

**Functionality:**
- Creates `epilepsy` table with schema: hash_id (BIGINT), time_uploaded (DATETIME), filename (TEXT), repo_id (INT), repo_name (TEXT), time_modified (DATETIME), modified_by (BIGINT)

### manage.py
Django's command-line management utility (auto-generated).

**Functionality:**
- Entry point for `python manage.py` commands (runserver, makemigrations, migrate, etc.) 

---
# Code
epilepsy-app/manage.py

```python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()```

epilepsy-app/sql.py

```python 
import mysql.connector
import sys



# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="sql123"
# )
# cursor = mydb.cursor(buffered=True)
# query = "CREATE DATABASE darsh"
# cursor.execute(query)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sql123",
  database="darsh"
)
cursor = mydb.cursor(buffered=True)

# query = "TRUNCATE TABLE epilepsy"
# video_hash = 580580433826171209
# cursor.execute(query)
# # row = cursor.fetchall()
# # print(row)
# cursor.close()
# mydb.close()
# # print(row)
# # if row:
# #     rows = [x for x in row]
# #     # write_to_file(lzma.decompress(rows[0]))
# #     video_data = bytes((rows[0]))
# #     print(video_data.__sizeof__())
query = """CREATE TABLE epilepsy (
  hash BIGINT UNSIGNED PRIMARY KEY, 
  time_uploaded DATETIME NOT NULL, 
  title TEXT, 
  movie LONGBLOB
  )
"""

cursor.execute(query)
# '''
# TYPING- 
# UNSIGNED BIGINT hash // unique ID, hash of title and time uploaded
# DATETIME time_uploaded 
# TEXT title
# LONGBLOB movie // movie being accessed
# '''
```
epilepsy-app/mysite/asgi.py
```python
"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_asgi_application()
```
epilepsy-app/mysite/settings.py
```python
"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("epilepscreen.urls")),
    path("admin/", admin.site.urls),
]
```

epilepsy-app/wsgi.py
```python
"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
```
epilepsy-app/epilepscreen/apps.py
```python
from django.apps import AppConfig


class EpilepscreenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'epilepscreen'
```
epilepsy-app/epilepscreen/urls.py
```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_video, name="upload"),
    path("stream/<int:video_hash>/", views.stream_video, name="stream"),
    path("delete/<int:video_hash>/", views.truncate, name="delete")
] 
```
epilepsy-app/epilepscreen/views.py
```python
import mysql.connector
import hashlib
import datetime
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import lzma
from django.db import models
import time
import base64

def write_to_file(bigdata):
    pass

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
                'file_path': f"/stream/{int(row['hash'])}", 
                'delpath':f"/delete/{int(row['hash'])}"
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

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(buffered=True)
        
        # Fetch the actual video binary
        query = "SELECT movie FROM epilepsy WHERE hash = %s"
        cursor.execute(query, (video_hash,))
        row = cursor.fetchall()
        cursor.close()
        cnx.close()
        if row:
            rows = [x for x in row]
            write_to_file(rows[0][0])
            video_data = bytes(rows[0][0])
            video_data=base64.b64decode(video_data)
            assert video_data is not None
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
        

        movie_blob=base64.b64encode(movie_blob)
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

def truncate(request, video_hash):

        # 3. Insert into MySQL
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor()

            
            query = "DELETE FROM epilepsy WHERE hash=%s"
            vals = (video_hash, )
            
            cursor.execute(query, vals)
            cnx.commit()
            time.sleep(1)
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            return HttpResponse(f"Database Insert Error: {err}", status=500)

        return redirect('index')
    
    # return redirect('index')
# ---------------------------------------------------------
# DATABASE SETUP INSTRUCTIONS
# ---------------------------------------------------------
# Run this SQL in your MySQL client to match the requested schema:
#
# CREATE TABLE videos (
#     hash BIGINT UNSIGNED PRIMARY KEY,
#     time_uploaded DATETIME NOT NULL,
#     title TEXT NOT NULL,
#     movie LONGBLOB
# );
#
# IMPORTANT:
# Storing videos requires a large `max_allowed_packet` in MySQL.
# You may need to run: SET GLOBAL max_allowed_packet = 1073741824; -- (1GB) 
 ```

epilepsy-app/epilepscreen/templates
```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Epilepscreen</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js">
    </script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js">
    </script>
    <style>
        :root {
            --bg-color: #121212;
            --text-color: #e0e0e0;
            --accent: #bb86fc;
            --danger: #cf6679;
        }

        #light{
            color: white !important;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        h1 { margin-bottom: 20px; }

        .container {
            width: 100%;
            max-width: 800px;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        /* Video Container */
        .video-wrapper {
            position: relative;
            width: 100%;
            padding-top: 56.25%; /* 16:9 Aspect Ratio */
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            transition: filter 0.3s ease; /* Smooth dimming transition */
        }

        /* Safety Overlay Message */
        .safety-indicator {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: rgba(0, 0, 0, 0.7);
            color: var(--accent);
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            display: none;
            z-index: 10;
            border: 1px solid var(--accent);
        }

        .safety-active {
            color: var(--danger);
            border-color: var(--danger);
        }

        /* Upload Form */
        .upload-section {
            border-top: 1px solid #333;
            padding-top: 20px;
            margin-top: 20px;
        }

        input[type="text"], input[type="file"] {
            padding: 10px;
            margin-bottom: 10px;
            background: #2c2c2c;
            border: 1px solid #333;
            color: white;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
        }

        button {
            background-color: var(--accent);
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
        }

        button:hover { opacity: 0.9; }

        /* Video List */
        .video-list {
            margin-top: 20px;
            list-style: none;
            padding: 0;
        }

        .video-item {
            background: #2c2c2c;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .video-item:hover { background: #3c3c3c; }

        /* Hidden canvas for processing */
        #analysisCanvas { display: none; }

        #heading{
            width: 20%;
            text-align: left;
            align-self: left;
        }
        
        #light{
            align-self: right;
            width: fit-content;
            background-color: black;
        }

        #main_heading{
            background-color: #1e1e1e;
            width: 100% !important;
            top: 0px;
            left: 0px;
            right: 0px;
            display: inline-block;
            text-align: left;
        }

        #clear-database{
            width: 100%;
            height: 100%;
        }

        #deleter{
            width: 20%;
        }

    </style>
</head>
<body id="b">
    <span id = "main-heading"><h1 id="heading">Epilepscreen</h1><button id="light" onclick="change_colour()" class="glyphicon glyphicon-adjust">Light Mode</button></span>
      <hr style="width: 100%;">  
    <div class="container" id = "second-entire">
        <h1>SafeView Player</h1>

        <div class="video-wrapper">
            <div id="safetyBadge" class="safety-indicator">Photosensitive Guard Active</div>

            <video id="mainPlayer" controls crossorigin="anonymous">
                <source src="" type="video/mp4" id="videoSource">
                Your browser does not support the video tag.
            </video>
        </div>

        <div class="upload-section" id="uploader">
            <h3>Upload New Video</h3>
            <form action="/upload/" method="POST" enctype="multipart/form-data">
                {% csrf_token %}
                <input type="text" name="title" placeholder="Video Title" required class="inp">
                <input type="file" name="video_file" accept="video/*" required class="inp">
                <button type="submit">Upload to Database</button>
            </form>
        </div>

        <h3>Library</h3>
        <ul class="video-list">
            {% for video in videos %}
            <li class="video-item" onclick="playVideo('{{ video.file_path }}')">
                <span>{{ video.title }}</span>
                <small>{{ video.uploaded_at }}</small>
                <form action='{{ video.delpath }}' method="POST" id="deleter">
                    <button id="clear-database" type="submit">Delete Video</button>
                </form>
                
            </li>
            {% empty %}
            <li class="video-item">No videos found. Upload one!</li>
            {% endfor %}
        </ul>
    </div>

    <!-- Hidden canvas for image analysis -->
    <canvas id="analysisCanvas"></canvas>

    <script>
        const video = document.getElementById('mainPlayer');
        const canvas = document.getElementById('analysisCanvas');
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        const safetyBadge = document.getElementById('safetyBadge');
        const source = document.getElementById('videoSource');

        // Configuration for sensitivity
        const CONFIG = {
            sampleRate: 20, // Check every 100ms (10fps analysis)
            flashThreshold: 20, // Difference in brightness to consider a "flash" (0-255)
            maxFlashCount: 2, // How many flashes in a row trigger dimming
            dimLevel: 'brightness(30%) sepia(20%) contrast(50%)', // CSS filter when protecting
            normalLevel: 'brightness(100%)',
            recoverySpeed: 2000 // Time ms to recover after flashing stops
        };

        let lastBrightness = -1;
        let flashCounter = 0;
        let isDimmed = false;
        let recoveryTimeout = null;
        let processingInterval = null;

        // Function to change video source dynamically
        function playVideo(path) {
            source.src = path;
            video.load();
            video.play();
        }

        // Main Analysis Loop
        function startAnalysis() {
            // Set canvas size small for performance (we don't need HD for brightness check)
            canvas.width = 64;
            canvas.height = 64;

            processingInterval = setInterval(() => {
                if (video.paused || video.ended) return;

                // Draw current video frame to canvas
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                // Get pixel data
                const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = frame.data;
                let r, g, b, avg;
                let colorSum = 0;

                // Calculate average brightness
                // Loop through pixels (data is [r, g, b, a, r, g, b, a...])
                // We step by 4 * 10 to sample fewer pixels for performance
                let pixelCount = 0;
                for (let i = 0; i < data.length; i += 40) {
                    r = data[i];
                    g = data[i+1];
                    b = data[i+2];
                    
                    // Perceived brightness formula
                    avg = Math.floor(0.299*r + 0.587*g + 0.114*b);
                    colorSum += avg;
                    pixelCount++;
                }

                const currentBrightness = Math.floor(colorSum / pixelCount);

                if (lastBrightness !== -1) {
                    const diff = Math.abs(currentBrightness - lastBrightness);

                    // Check for rapid flash (strobe effect)
                    if (diff > CONFIG.flashThreshold) {
                        flashCounter++;
                    } else {
                        // Decay counter slowly
                        if(flashCounter > 0) flashCounter--;
                    }

                    // Trigger Protection
                    if (flashCounter >= CONFIG.maxFlashCount) {
                        engageProtection();
                    } 
                }

                lastBrightness = currentBrightness;

            }, CONFIG.sampleRate);
        }

        function engageProtection() {
            if (isDimmed) return; // Already protected
            
            isDimmed = true;
            video.style.filter = CONFIG.dimLevel;
            safetyBadge.style.display = 'block';
            safetyBadge.textContent = 'High Contrast/Flash Detected - Dimming';
            safetyBadge.classList.add('safety-active');

            // Reset recovery timer
            if (recoveryTimeout) clearTimeout(recoveryTimeout);
            
            // Try to recover after X seconds
            recoveryTimeout = setTimeout(disengageProtection, CONFIG.recoverySpeed);
        }

        function disengageProtection() {
            // If we are still flashing, don't recover yet
            if (flashCounter > 0) {
                recoveryTimeout = setTimeout(disengageProtection, 1000);
                return;
            }

            isDimmed = false;
            video.style.filter = CONFIG.normalLevel;
            safetyBadge.style.display = 'none';
            safetyBadge.classList.remove('safety-active');
        }

        // Event Listeners
        video.addEventListener('play', () => {
            if (!processingInterval) startAnalysis();
        });

        video.addEventListener('pause', () => {
            clearInterval(processingInterval);
            processingInterval = null;
        });

        video.addEventListener('ended', () => {
            clearInterval(processingInterval);
            processingInterval = null;
            disengageProtection();
        });
        dark_mode = true
        function change_colour(){
            if (dark_mode){
                document.getElementById("b").style.backgroundColor = 'white';
                document.getElementById("main-heading").style.backgroundColor = '#dadada';
                document.getElementById("second-entire").style.backgroundColor = 'white';
                document.getElementById("second-entire").style.color = 'black';
                document.getElementById("light").innerHTML='Dark Mode';
                document.getElementById("heading").style.color = 'black';
                dark_mode = false;
                console.log(dark_mode)
            } else if(dark_mode==false){
                document.getElementById("b").style.backgroundColor = 'black';
                document.getElementById("heading").style.color = 'white';
                document.getElementById("second-entire").style.backgroundColor = '#2c2c2c';
                document.getElementById("second-entire").style.color = 'white';
                document.getElementById("light").innerHTML='Light Mode';
                document.getElementById("main-heading").style.backgroundColor = 'black';
                dark_mode = true;
            }
            
        }
    </script>
</body>
</html>
```
---

# Output


---
# Limitations- 
- Yet to add personal, user database; currently all videos are stored globally.
- More operations like video renaming and such to be added.
- Boring GUI; can be improved.
- Support for streaming platforms like Netflix.

---
# Future Implementions- 
- Better DB operations like renaming
- A user system, with logins and personal video lists
- A clear demarcation between global video lists and perosnal video list, with global lists having authors mentioned and such

---

# Bibliography

### Python Documentation
- Python Software Foundation. (2024). *Python 3.13 Documentation*. https://docs.python.org/3.13/
- Python Software Foundation. (2024). *The Python Standard Library*. https://docs.python.org/3.13/library/
- Python Software Foundation. (2024). *Python Tutorial*. https://docs.python.org/3.13/tutorial/

### Django Framework
- Django Software Foundation. (2024). *Django 5.1 Documentation*. https://docs.djangoproject.com/en/5.1/
- Django Software Foundation. (2024). *Django Models*. https://docs.djangoproject.com/en/5.1/topics/db/models/
- Django Software Foundation. (2024). *Django Views and URL Dispatcher*. https://docs.djangoproject.com/en/5.1/topics/http/urls/
- Django Software Foundation. (2024). *Django Templates*. https://docs.djangoproject.com/en/5.1/topics/templates/

### Database and MySQL
- Oracle Corporation. (2024). *MySQL Connector/Python Documentation*. https://dev.mysql.com/doc/connector-python/en/
- MySQL. (2024). *MySQL 8.0 Reference Manual*. https://dev.mysql.com/doc/refman/8.0/en/

### Video Processing and Compression
- Coffin, Stewart. (2024). *lzma - Compression using the LZMA algorithm*. Python Software Foundation. https://docs.python.org/3.13/library/lzma.html
- FFmpeg Project. (2024). *FFmpeg Documentation*. https://ffmpeg.org/documentation.html

### Web Development and Security
- OWASP. (2024). *OWASP Top 10 - 2021*. https://owasp.org/www-project-top-ten/
- Mozilla Developer Network. (2024). *HTTP/HTML Basics*. https://developer.mozilla.org/en-US/docs/Web/

### Health and Accessibility
- World Health Organization. (2023). *Epilepsy Fact Sheet*. https://www.who.int/news-room/fact-sheets/
- W3C Web Accessibility Initiative. (2024). *Web Content Accessibility Guidelines (WCAG)*. https://www.w3.org/WAI/WCAG21/quickref/

### Cryptography and Hashing
- Python Software Foundation. (2024). *hashlib - Secure hashes and message digests*. https://docs.python.org/3.13/library/hashlib.html


---
###By Ayan Tripathi, Aryan Khairnar and Darsh Gupta
