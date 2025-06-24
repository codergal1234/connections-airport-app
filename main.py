from flask import Flask, render_template_string, request, session, jsonify, redirect, url_for
import csv
import os
from datetime import datetime, timedelta
import random
import json
print("main.py is running!")

app = Flask(__name__)
app.secret_key = 'connections_airport_app_secret_key'

# CSV files
PROFILES_FILE = 'airport_profiles.csv'
MESSAGES_FILE = 'messages.csv'
VERIFICATIONS_FILE = 'verifications.csv'

# Icebreaker prompts
ICEBREAKERS = [
    "What's the most interesting place you've traveled to?",
    "Best airport food you've ever had?",
    "Window or aisle seat?",
    "What's your travel essential that others might find weird?",
    "If you could fly anywhere right now, where would you go?",
    "What's your airport routine?",
    "Coffee or tea person?",
    "What's the longest layover you've ever had?",
    "Do you prefer early morning or late night flights?",
    "What's your go-to travel playlist?"
]

# Create CSV files with headers if they don't exist
def init_csv():
    if not os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Age', 'Bio', 'Airport', 'Terminal', 'Gate', 'Flight_Number', 'Departure_Time', 'Destination', 'Travel_Purpose', 'Interests', 'Icebreaker_Response', 'Points', 'Is_Visible', 'Is_Verified', 'Timestamp'])
    
    if not os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['From_Name', 'To_Name', 'Message', 'Timestamp', 'Is_Read'])
    
    if not os.path.exists(VERIFICATIONS_FILE):
        with open(VERIFICATIONS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Verification_Type', 'Status', 'Timestamp'])

# Save profile to CSV file
def save_profile(name, age, bio, airport, terminal, gate, flight_number, departure_time, destination, travel_purpose, interests, icebreaker_response):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    points = 100  # Starting points
    is_visible = True
    is_verified = False
    with open(PROFILES_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, bio, airport, terminal, gate, flight_number, departure_time, destination, travel_purpose, interests, icebreaker_response, points, is_visible, is_verified, timestamp])

# Read all profiles from CSV file
def get_all_profiles():
    profiles = []
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                profiles.append(row)
    return profiles

# Get profiles by airport and terminal (location filtering)
def get_profiles_by_location(airport, terminal):
    profiles = get_all_profiles()
    return [p for p in profiles if p['Airport'] == airport and p['Terminal'] == terminal and p['Is_Visible'] == 'True']

# Get profiles by airport only
def get_profiles_by_airport(airport):
    profiles = get_all_profiles()
    return [p for p in profiles if p['Airport'] == airport and p['Is_Visible'] == 'True']

# Save message
def save_message(from_name, to_name, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    is_read = False
    with open(MESSAGES_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([from_name, to_name, message, timestamp, is_read])

# Get messages for a user
def get_messages_for_user(user_name):
    messages = []
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['To_Name'] == user_name or row['From_Name'] == user_name:
                    messages.append(row)
    return messages

# Mark message as read
def mark_message_as_read(from_name, to_name, timestamp):
    messages = []
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (row['From_Name'] == from_name and row['To_Name'] == to_name and 
                    row['Timestamp'] == timestamp):
                    row['Is_Read'] = True
                messages.append(row)
        
        # Rewrite file with updated read status
        with open(MESSAGES_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['From_Name', 'To_Name', 'Message', 'Timestamp', 'Is_Read'])
            for msg in messages:
                writer.writerow([msg['From_Name'], msg['To_Name'], msg['Message'], msg['Timestamp'], msg['Is_Read']])

# Save verification
def save_verification(name, verification_type):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'Pending'
    with open(VERIFICATIONS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, verification_type, status, timestamp])

# Get verification status
def get_verification_status(name):
    if os.path.exists(VERIFICATIONS_FILE):
        with open(VERIFICATIONS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Name'] == name:
                    return row['Status']
    return 'Not_Verified'

# Get random icebreaker
def get_random_icebreaker():
    return random.choice(ICEBREAKERS)

# Simulate flight status updates
def get_flight_status(flight_number):
    # Simulate real-time flight status
    statuses = ['On Time', 'Delayed 15 min', 'Delayed 30 min', 'Boarding', 'Departed']
    return random.choice(statuses)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Connections ✈️ - Airport Social & Dating</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 300;
            margin-bottom: 20px;
        }
        
        .tagline {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            font-size: 1rem;
            font-weight: 500;
        }
        
        .nav-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 5px;
        }
        
        .nav-tab {
            padding: 12px 24px;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
            margin: 0 5px;
        }
        
        .nav-tab.active {
            background: rgba(255,255,255,0.2);
            font-weight: 600;
        }
        
        .nav-tab:hover {
            background: rgba(255,255,255,0.15);
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            align-items: start;
        }
        
        .profile-form {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        
        .form-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 30px;
            color: #333;
            text-align: center;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #555;
            font-size: 0.95rem;
        }
        
        input[type="text"], input[type="number"], select, textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        input[type="text"]:focus, input[type="number"]:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .interests-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        
        .interest-option {
            display: flex;
            align-items: center;
            padding: 10px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .interest-option:hover {
            border-color: #667eea;
            background: #f0f2ff;
        }
        
        .interest-option input[type="checkbox"] {
            margin-right: 8px;
            transform: scale(1.2);
        }
        
        .submit-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .success-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 30px;
        }
        
        .success-icon {
            font-size: 4rem;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        
        .success-title {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }
        
        .success-text {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 25px;
        }
        
        .profile-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            position: relative;
        }
        
        .profile-card:hover {
            transform: translateY(-5px);
        }
        
        .profile-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .profile-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            font-weight: 600;
            margin-right: 15px;
        }
        
        .profile-info h3 {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 5px;
            color: #333;
        }
        
        .profile-info p {
            color: #666;
            font-size: 0.95rem;
        }
        
        .flight-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }
        
        .flight-info h4 {
            color: #333;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        
        .flight-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 0.9rem;
            color: #666;
        }
        
        .flight-status {
            background: #e8f5e8;
            color: #2d5a2d;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 10px;
            display: inline-block;
        }
        
        .profile-bio {
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .icebreaker-response {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
            font-style: italic;
        }
        
        .profile-interests {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }
        
        .interest-tag {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .profile-timestamp {
            color: #999;
            font-size: 0.85rem;
            margin-top: 15px;
        }
        
        .points-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #ffd700;
            color: #333;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .verification-badge {
            position: absolute;
            top: 15px;
            left: 15px;
            background: #4CAF50;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-secondary {
            background: #f8f9fa;
            color: #666;
            border: 1px solid #e1e5e9;
        }
        
        .btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .section-title {
            color: white;
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .new-profile-btn {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 2px solid rgba(255,255,255,0.3);
        }
        
        .new-profile-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        
        .safety-notice {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            padding: 15px;
            border-radius: 12px;
            margin: 20px 0;
            color: white;
            font-size: 0.9rem;
        }
        
        .safety-notice h4 {
            margin-bottom: 8px;
            font-size: 1rem;
        }
        
        .filter-section {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            color: white;
        }
        
        .filter-section h3 {
            margin-bottom: 15px;
            font-size: 1.2rem;
        }
        
        .filter-options {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .filter-option {
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .filter-option.active {
            background: rgba(255,255,255,0.3);
            font-weight: 600;
        }
        
        .messages-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .message-item {
            border-bottom: 1px solid #e1e5e9;
            padding: 15px 0;
        }
        
        .message-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .message-sender {
            font-weight: 600;
            color: #333;
        }
        
        .message-time {
            color: #999;
            font-size: 0.85rem;
        }
        
        .message-content {
            color: #555;
            line-height: 1.5;
        }
        
        .unread {
            background: #f0f2ff;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
                gap: 30px;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .profile-form {
                padding: 30px 20px;
            }
            
            .interests-grid {
                grid-template-columns: 1fr;
            }
            
            .flight-details {
                grid-template-columns: 1fr;
            }
            
            .filter-options {
                flex-direction: column;
            }
            
            .action-buttons {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-plane"></i> Connections ✈️</h1>
            <p>Turn "airport time" into "connection time"</p>
            <div class="tagline">
                <i class="fas fa-map-marker-alt"></i> Meet people at your airport • <i class="fas fa-clock"></i> Connect before you fly
            </div>
        </div>
        
        <div class="nav-tabs">
            <a href="#profiles" class="nav-tab active" onclick="showSection('profiles')">
                <i class="fas fa-users"></i> Profiles
            </a>
            <a href="#messages" class="nav-tab" onclick="showSection('messages')">
                <i class="fas fa-comments"></i> Messages
            </a>
            <a href="#create" class="nav-tab" onclick="showSection('create')">
                <i class="fas fa-plus"></i> Create Profile
            </a>
        </div>
        
        <div id="profiles-section" class="section">
            <div class="filter-section">
                <h3><i class="fas fa-filter"></i> Filter Travelers</h3>
                <div class="filter-options">
                    <div class="filter-option active" onclick="filterByLocation('all')">All Airports</div>
                    <div class="filter-option" onclick="filterByLocation('SFO')">SFO</div>
                    <div class="filter-option" onclick="filterByLocation('JFK')">JFK</div>
                    <div class="filter-option" onclick="filterByLocation('LAX')">LAX</div>
                    <div class="filter-option" onclick="filterByLocation('ORD')">ORD</div>
                </div>
            </div>
            
            <div class="section-title">
                <i class="fas fa-users"></i> Fellow Travelers
            </div>
            
            <div class="main-content" id="profiles-container">
                {% if checkins %}
                    {% for checkin in checkins %}
                    <div class="profile-card" data-airport="{{ checkin.Airport }}" data-terminal="{{ checkin.Terminal }}">
                        {% if checkin.Is_Verified == 'True' %}
                        <div class="verification-badge">
                            <i class="fas fa-check-circle"></i> Verified
                        </div>
                        {% endif %}
                        
                        <div class="points-badge">
                            <i class="fas fa-star"></i> {{ checkin.Points }} pts
                        </div>
                        
                        <div class="profile-header">
                            <div class="profile-avatar">
                                {{ checkin.Name[0] if checkin.Name else 'U' }}
                            </div>
                            <div class="profile-info">
                                <h3>{{ checkin.Name }}</h3>
                                <p><i class="fas fa-map-marker-alt"></i> {{ checkin.Airport }} - {{ checkin.Terminal }}</p>
                                <p><i class="fas fa-birthday-cake"></i> {{ checkin.Age }} years old</p>
                            </div>
                        </div>
                        
                        <div class="flight-info">
                            <h4><i class="fas fa-plane"></i> Flight Details</h4>
                            <div class="flight-details">
                                <div><strong>Flight:</strong> {{ checkin.Flight_Number }}</div>
                                <div><strong>Departure:</strong> {{ checkin.Departure_Time }}</div>
                                <div><strong>Destination:</strong> {{ checkin.Destination }}</div>
                                <div><strong>Purpose:</strong> {{ checkin.Travel_Purpose }}</div>
                            </div>
                            <div class="flight-status" id="status-{{ checkin.Flight_Number }}">
                                <i class="fas fa-clock"></i> Checking status...
                            </div>
                        </div>
                        
                        <div class="profile-bio">
                            "{{ checkin.Bio }}"
                        </div>
                        
                        {% if checkin.Icebreaker_Response %}
                        <div class="icebreaker-response">
                            <strong>💬 Icebreaker:</strong> {{ checkin.Icebreaker_Response }}
                        </div>
                        {% endif %}
                        
                        {% if checkin.Interests %}
                        <div class="profile-interests">
                            {% for interest in checkin.Interests.split(', ') %}
                            <span class="interest-tag">{{ interest }}</span>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="action-buttons">
                            <button class="btn btn-primary" onclick="sendMessage('{{ checkin.Name }}')">
                                <i class="fas fa-comment"></i> Message
                            </button>
                            <button class="btn btn-secondary" onclick="viewProfile('{{ checkin.Name }}')">
                                <i class="fas fa-eye"></i> View Profile
                            </button>
                        </div>
                        
                        <div class="profile-timestamp">
                            <i class="fas fa-clock"></i> Joined {{ checkin.Timestamp }}
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="profile-card" style="text-align: center; grid-column: 1 / -1;">
                        <div class="success-icon" style="color: #667eea;">
                            <i class="fas fa-users"></i>
                        </div>
                        <h3 style="margin-bottom: 10px;">No travelers yet</h3>
                        <p style="color: #666;">Be the first to create a profile and start connecting with fellow travelers!</p>
                    </div>
                {% endif %}
            </div>
        </div>
        
        <div id="messages-section" class="section" style="display: none;">
            <div class="messages-section">
                <h2 class="section-title" style="color: #333;">Messages</h2>
                {% if messages %}
                    {% for message in messages %}
                    <div class="message-item {% if message.Is_Read == 'False' %}unread{% endif %}">
                        <div class="message-header">
                            <span class="message-sender">{{ message.From_Name }}</span>
                            <span class="message-time">{{ message.Timestamp }}</span>
                        </div>
                        <div class="message-content">{{ message.Message }}</div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="text-align: center; color: #666; padding: 40px;">No messages yet. Start connecting with fellow travelers!</p>
                {% endif %}
            </div>
        </div>
        
        <div id="create-section" class="section" style="display: none;">
            {% if not checked_in %}
                <div class="profile-form">
                    <h2 class="form-title">Create Your Airport Profile</h2>
                    <form method="post">
                        <div class="form-group">
                            <label for="name"><i class="fas fa-user"></i> Full Name</label>
                            <input type="text" id="name" name="name" required placeholder="Enter your full name">
                        </div>
                        
                        <div class="form-group">
                            <label for="age"><i class="fas fa-birthday-cake"></i> Age</label>
                            <input type="number" id="age" name="age" required min="18" max="100" placeholder="Your age">
                        </div>
                        
                        <div class="form-group">
                            <label for="bio"><i class="fas fa-quote-left"></i> Bio</label>
                            <textarea id="bio" name="bio" required placeholder="Tell us about yourself, why you're traveling, and what you're looking for..."></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="airport"><i class="fas fa-plane-departure"></i> Airport</label>
                            <select id="airport" name="airport" required>
                                <option value="">Select your airport</option>
                                <option value="SFO">San Francisco International (SFO)</option>
                                <option value="JFK">John F. Kennedy (JFK)</option>
                                <option value="LAX">Los Angeles International (LAX)</option>
                                <option value="ORD">O'Hare International (ORD)</option>
                                <option value="MIA">Miami International (MIA)</option>
                                <option value="ATL">Hartsfield-Jackson Atlanta (ATL)</option>
                                <option value="DFW">Dallas/Fort Worth (DFW)</option>
                                <option value="DEN">Denver International (DEN)</option>
                                <option value="SEA">Seattle-Tacoma International (SEA)</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="terminal"><i class="fas fa-building"></i> Terminal</label>
                            <select id="terminal" name="terminal" required>
                                <option value="">Select terminal</option>
                                <option value="Terminal 1">Terminal 1</option>
                                <option value="Terminal 2">Terminal 2</option>
                                <option value="Terminal 3">Terminal 3</option>
                                <option value="Terminal 4">Terminal 4</option>
                                <option value="Terminal 5">Terminal 5</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="gate"><i class="fas fa-door-open"></i> Gate (Optional)</label>
                            <input type="text" id="gate" name="gate" placeholder="e.g., A12, B5">
                        </div>
                        
                        <div class="form-group">
                            <label for="flight_number"><i class="fas fa-plane"></i> Flight Number</label>
                            <input type="text" id="flight_number" name="flight_number" required placeholder="e.g., AA123, DL456">
                        </div>
                        
                        <div class="form-group">
                            <label for="departure_time"><i class="fas fa-clock"></i> Departure Time</label>
                            <input type="time" id="departure_time" name="departure_time" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="destination"><i class="fas fa-map-marker-alt"></i> Destination</label>
                            <input type="text" id="destination" name="destination" required placeholder="e.g., New York, London, Tokyo">
                        </div>
                        
                        <div class="form-group">
                            <label for="travel_purpose"><i class="fas fa-briefcase"></i> Travel Purpose</label>
                            <select id="travel_purpose" name="travel_purpose" required>
                                <option value="">Select purpose</option>
                                <option value="Business">Business</option>
                                <option value="Leisure">Leisure</option>
                                <option value="Family Visit">Family Visit</option>
                                <option value="Study Abroad">Study Abroad</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label><i class="fas fa-tags"></i> Interests (Select all that apply)</label>
                            <div class="interests-grid">
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Travel" id="travel">
                                    <label for="travel">Travel</label>
                                </div>
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Business" id="business">
                                    <label for="business">Business</label>
                                </div>
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Food & Dining" id="food">
                                    <label for="food">Food & Dining</label>
                                </div>
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Technology" id="tech">
                                    <label for="tech">Technology</label>
                                </div>
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Sports" id="sports">
                                    <label for="sports">Sports</label>
                                </div>
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Music" id="music">
                                    <label for="music">Music</label>
                                </div>
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Art & Culture" id="art">
                                    <label for="art">Art & Culture</label>
                                </div>
                                <div class="interest-option">
                                    <input type="checkbox" name="interests" value="Reading" id="reading">
                                    <label for="reading">Reading</label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="icebreaker_response"><i class="fas fa-comments"></i> Icebreaker Response</label>
                            <textarea id="icebreaker_response" name="icebreaker_response" required placeholder="Answer this icebreaker: {{ icebreaker }}"></textarea>
                        </div>
                        
                        <button type="submit" class="submit-btn">
                            <i class="fas fa-plane"></i> Create Airport Profile
                        </button>
                    </form>
                </div>
            {% else %}
                <div class="success-card">
                    <div class="success-icon">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <h2 class="success-title">Welcome to Connections, {{ name }}!</h2>
                    <p class="success-text">Your airport profile has been created successfully. Start connecting with fellow travelers!</p>
                    <a href="/" class="new-profile-btn">
                        <i class="fas fa-plus"></i> Create Another Profile
                    </a>
                </div>
            {% endif %}
        </div>
        
        <div class="safety-notice">
            <h4><i class="fas fa-shield-alt"></i> Safety First</h4>
            <p>Always meet in public airport spaces, never share personal travel details, and trust your instincts. Use the block/report features if needed.</p>
        </div>
    </div>
    
    <script>
        function showSection(sectionName) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Show selected section
            document.getElementById(sectionName + '-section').style.display = 'block';
            
            // Update active tab
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        function filterByLocation(airport) {
            const profiles = document.querySelectorAll('.profile-card');
            const filterOptions = document.querySelectorAll('.filter-option');
            
            // Update active filter
            filterOptions.forEach(option => {
                option.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Filter profiles
            profiles.forEach(profile => {
                if (airport === 'all' || profile.dataset.airport === airport) {
                    profile.style.display = 'block';
                } else {
                    profile.style.display = 'none';
                }
            });
        }
        
        function sendMessage(toName) {
            const message = prompt('Enter your message to ' + toName + ':');
            if (message) {
                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        to_name: toName,
                        message: message
                    })
                }).then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Message sent successfully!');
                        location.reload();
                    } else {
                        alert('Error sending message: ' + data.error);
                    }
                });
            }
        }
        
        function viewProfile(name) {
            alert('Viewing profile of ' + name + ' (Feature coming soon!)');
        }
        
        // Update flight statuses every 30 seconds
        setInterval(() => {
            document.querySelectorAll('.flight-status').forEach(statusElement => {
                const flightNumber = statusElement.id.replace('status-', '');
                fetch('/flight_status/' + flightNumber)
                .then(response => response.json())
                .then(data => {
                    statusElement.innerHTML = '<i class="fas fa-clock"></i> ' + data.status;
                });
            });
        }, 30000);
        
        // Initial flight status update
        setTimeout(() => {
            document.querySelectorAll('.flight-status').forEach(statusElement => {
                const flightNumber = statusElement.id.replace('status-', '');
                fetch('/flight_status/' + flightNumber)
                .then(response => response.json())
                .then(data => {
                    statusElement.innerHTML = '<i class="fas fa-clock"></i> ' + data.status;
                });
            });
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def checkin():
    # Initialize CSV files
    init_csv()
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        bio = request.form['bio']
        airport = request.form['airport']
        terminal = request.form['terminal']
        gate = request.form['gate']
        flight_number = request.form['flight_number']
        departure_time = request.form['departure_time']
        destination = request.form['destination']
        travel_purpose = request.form['travel_purpose']
        interests = ', '.join(request.form.getlist('interests'))
        icebreaker_response = request.form['icebreaker_response']
        
        # Save profile to CSV
        save_profile(name, age, bio, airport, terminal, gate, flight_number, departure_time, destination, travel_purpose, interests, icebreaker_response)
        
        # Get all profiles for display
        checkins = get_all_profiles()
        messages = get_messages_for_user(name)
        
        return render_template_string(TEMPLATE, 
                                    checked_in=True, 
                                    name=name,
                                    checkins=checkins,
                                    messages=messages)
    
    # Get random icebreaker for the form
    icebreaker = get_random_icebreaker()
    
    # Get all profiles for display
    checkins = get_all_profiles()
    messages = []
    
    return render_template_string(TEMPLATE, checked_in=False, checkins=checkins, messages=messages, icebreaker=icebreaker)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    from_name = "You"  # In a real app, this would be the logged-in user
    to_name = data['to_name']
    message = data['message']
    
    try:
        save_message(from_name, to_name, message)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/flight_status/<flight_number>')
def flight_status(flight_number):
    status = get_flight_status(flight_number)
    return jsonify({'status': status})

@app.route('/verify_profile', methods=['POST'])
def verify_profile():
    data = request.get_json()
    name = data['name']
    verification_type = data['type']
    
    try:
        save_verification(name, verification_type)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
