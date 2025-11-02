🧠 Criminal Detection System

AI-Powered Real-Time Criminal Recognition and Alert System

<p align="center"> <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python"> <img src="https://img.shields.io/badge/OpenCV-4.0+-green?logo=opencv"> <img src="https://img.shields.io/badge/face_recognition-latest-orange"> <img src="https://img.shields.io/badge/Telegram%20Bot-active-success?logo=telegram"> </p>
🚨 Overview

The Criminal Detection System is an AI-based security application that identifies known criminals from live video feeds using facial recognition.
When a match is detected, it automatically sends an alert via Telegram, saves the snapshot locally, and logs the event — enabling fast, intelligent responses in real-world surveillance setups.

Built entirely in Python, this project demonstrates how AI, Computer Vision, and IoT integration can be combined to create a next-generation smart monitoring system.

🔍 Key Features
Feature	Description
🧑‍💻 Real-Time Recognition	Detects and recognizes faces using live webcam feed
⚙️ AI-Based Face Encoding	Uses dlib models from the face_recognition library
📲 Instant Telegram Alerts	Sends text alerts instantly when a criminal is detected
🧾 Event Logging	Saves every detection with timestamp, name, and confidence score
🖼️ Snapshot Saving	Automatically crops and stores the detected face locally
🔐 Secure Configuration	API keys and chat IDs stored safely in .env
🧩 Modular Code Design	Each module handles one specific responsibility
🌍 Extensible System	Can integrate GPS, cloud, or police databases in the future
🧠 System Architecture
         +---------------------------+
         |     Webcam / CCTV Feed    |
         +-------------+-------------+
                       |
                       v
        +--------------+--------------+
        |   Face Detection (OpenCV)   |
        +--------------+--------------+
                       |
                       v
     +-----------------+-----------------+
     | Face Encoding & Matching (dlib)   |
     +-----------------+-----------------+
                       |
        +--------------+--------------+
        |  Match Found?               |
        +--------------+--------------+
                       | YES
                       v
     +--------------------------------------+
     | Alert via Telegram + Save Snapshot   |
     +--------------------------------------+
                       |
                       v
     +--------------------------------------+
     | Log Event (Name, Time, Confidence)   |
     +--------------------------------------+

🧩 Project Structure
Criminal-Detection-System/
│
├── main.py               # Main runner for the entire program
├── recognizer.py         # Face detection and recognition logic
├── telegram_bot.py       # Handles Telegram alerts
├── logger.py             # Logs all detection events
├── snapshot.py           # Captures and stores snapshots
├── criminals/            # Known criminal images
├── logs/                 # Detection logs (auto-created)
├── snapshots/            # Cropped detection images
├── .env                  # Secure credentials
├── requirements.txt      # Dependencies list
└── README.md             # Project documentation

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/Karan-Solanki8695/Criminal-Detection-System.git
cd Criminal-Detection-System

2️⃣ Install dependencies

Before installing the Python libraries, install required C/C++ build tools needed for dlib:

🪟 Windows Users

Install Visual Studio Build Tools (with C++ workload)

Install CMake: Download Here

Install Boost (optional but recommended)

🐧 Linux Users
sudo apt update
sudo apt install build-essential cmake
sudo apt install libboost-all-dev

🍎 Mac Users
brew install cmake boost


Then install Python dependencies:

pip install -r requirements.txt

3️⃣ Add known criminal images

Put face images inside the criminals/ folder.

Image name = Person’s name (e.g., john_doe.jpg)

You can add multiple images for the same person for higher accuracy.

4️⃣ Configure .env file

Create a .env file in the main folder and add:

TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

5️⃣ Run the system
python main.py


It will open your webcam and start detecting faces in real time.

💬 Telegram Bot Commands
Command	Description
/start	Start the bot
/help	List all available commands
/snapshot	Get the latest detection snapshot info
/status	Check system status
/alerts	Show number of total detections
/setalert	Trigger a manual alert for testing
📊 Example Output

Console Log Example

[INFO] Starting Criminal Detection System...
[INFO] Loaded 5 known faces.
[ALERT] Criminal detected: John Doe
[INFO] Snapshot saved: snapshots/john_doe_2025-11-02_16-20.png
[INFO] Alert sent to Telegram successfully!


Telegram Message Example

🚨 Criminal Detected!
Name: John Doe
Time: 2025-11-02 16:20:15

🌐 Future Enhancements

✅ Send Snapshot in Telegram Alerts — (planned feature)
✅ Cloud Database Integration — Link to police or missing-persons database
✅ GPS Tagging — Capture camera location for mobile systems
✅ Multi-Camera Support — Manage multiple live feeds simultaneously
✅ Dashboard Interface — Add real-time GUI using Flask or Streamlit
✅ Raspberry Pi Version — Low-cost portable surveillance device

🧾 Requirements
Library	Version	Description
Python	3.8+	Core language
face_recognition	latest	Face encoding and comparison
dlib	latest	Deep metric learning for face recognition
opencv-python	4.x	Image and video processing
numpy	latest	Matrix operations
python-telegram-bot	20+	Telegram bot API
python-dotenv	latest	For environment variables
cmake / boost / C++ tools	latest	Required for building dlib
🧑‍💻 Author

👤 Karan Solanki

“Building AI that protects society.”
A passionate AI & Tech innovator from Maharashtra, India — working on real-time AI systems for public safety, surveillance, and smart automation.

📫 GitHub: Karan-Solanki8695

💬 Telegram: @Karanthestudent

⚖️ License

This project is released under the MIT License.
You are free to use, modify, and distribute it with proper credit to the author.
