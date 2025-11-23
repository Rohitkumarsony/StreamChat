# StreamChat

A real-time, secure group chat application with end-to-end encryption, built using FastAPI, Socket.IO, Redis, and Kafka. No data is stored permanently - all messages exist only in memory during active sessions.

## 🚀 Features

- **Real-time Group Chat**: Instant messaging with WebSocket technology
- **End-to-End Encryption**: All messages are encrypted between users
- **No Data Storage**: Ephemeral messaging - no chat history is saved
- **User Presence**: Real-time notifications when users join or leave
- **Timestamp Display**: Every message shows date and time
- **System Alerts**: Automatic notifications for user activity
- **Encrypted File Sharing**: Share images and videos with encryption
- **Real-time Media Playback**: View images and play videos directly in chat
- **Secure Media Streaming**: All files encrypted before transmission
- **Scalable Architecture**: Redis and Kafka for high-performance messaging

## 🔒 Security & Privacy

- ✅ **Zero Data Persistence**: Messages are never stored in databases
- ✅ **Encrypted Communication**: All messages encrypted in transit using Fernet
- ✅ **Encrypted Files**: Images and videos encrypted before transmission
- ✅ **Anonymous Sessions**: No permanent user data collection
- ✅ **Session-based**: Chat history exists only during active session
- ✅ **Auto-cleanup**: Messages and files disappear when users leave
- ✅ **In-Memory Processing**: Files never saved to disk, only in memory

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** - Core programming language
- **FastAPI** - High-performance async web framework
- **Socket.IO** - Real-time bidirectional communication
- **Redis** - In-memory data store for session management
- **Kafka** - Distributed event streaming platform
- **cryptography** - Python encryption library for secure messaging
- **Fernet (Symmetric Encryption)** - File and message encryption

### Frontend
- **HTML5** - Structure and layout
- **CSS3** - Modern, responsive design
- **JavaScript** - Real-time WebSocket handling
- **Socket.IO Client** - Client-side real-time communication

## 📁 Project Structure

```
StreamChat/
│
├── main.py                     # FastAPI application entry point
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container configuration
│
├── src/                        # Backend source code
│   ├── router/                 # FastAPI routers
│   │   └── chat_router.py      # Chat WebSocket routes
│   │
│   └── uploads/                # Temporary file uploads
│
├── templates/                  # Frontend HTML templates
│   └── chat.html               # Group chat interface
│
├── uploads/                    # User uploaded files (temporary)
│
└── __pycache__/                # Python cache files
```

## 🚦 Getting Started

### Prerequisites

- Python 3.11 or higher
- Redis Server
- Apache Kafka (optional for distributed setup)
- Docker (optional)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Rohitkumarsony/StreamChat.git
cd StreamChat
```

2. **Create a virtual environment:**
```bash
python3 -m venv env
```

3. **Activate the virtual environment:**

**On Linux/macOS:**
```bash
source env/bin/activate
```

**On Windows:**
```bash
env\Scripts\activate
```

4. **Create a `.env` file in the project root:**
```bash
touch .env
```

Add the following configuration to your `.env` file:
```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=chat_messages

# Encryption Configuration
ENCRYPTION_KEY=your-secure-fernet-key-here
# Generate a key: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

5. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

6. **Start Redis Server:**
```bash
redis-server
```

7. **Start Kafka (if using distributed setup):**
```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Server
bin/kafka-server-start.sh config/server.properties
```

8. **Run the application:**

**Option 1: Using Python directly**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 2: Using Docker**
```bash
# Build the image
docker build -t streamchat .

# Run the container
docker run -d -p 8000:8000 --name streamchat_app streamchat

# Stop the container
docker stop streamchat_app

# Remove the container
docker rm streamchat_app
```

9. **Open your browser and navigate to:**
```
http://localhost:8000
```

## 💡 How to Use

1. **Join Chat**: Enter your username to join the group chat
2. **Send Messages**: Type your message and press Enter or click Send
3. **Upload Files**: Click the Upload button to share images or videos
4. **View Shared Media**: Images display inline, videos play directly in chat
5. **Real-time Playback**: Watch videos and view images without downloading
6. **Encrypted Transfer**: All media files are encrypted before sending
7. **Real-time Updates**: See when users join or leave with system alerts
8. **Encrypted Communication**: All messages are automatically encrypted
9. **Leave Chat**: Close the browser tab - no data is retained

## 📊 System Alerts

The application automatically displays system messages for:

- ✅ **User Joined**: "John joined the chat at 14:30:45 on 2024-01-15"
- ❌ **User Left**: "John left the chat at 14:35:20 on 2024-01-15"
- 📝 **Message Sent**: Each message displays timestamp and date
- 🔒 **Encryption Status**: "Messages are end-to-end encrypted"

## 🔐 Message & File Encryption

All messages and files are encrypted using the Python `cryptography` library with Fernet (symmetric encryption):

### Text Messages
```python
# Automatic encryption on send
plaintext_message → Fernet encryption → encrypted_message → sent to users

# Automatic decryption on receive
encrypted_message → Fernet decryption → plaintext_message → displayed
```

### File Encryption
```python
# File upload process
original_file → read as bytes → Fernet encryption → encrypted_data → transmitted

# File receive process
encrypted_data → Fernet decryption → original_bytes → displayed/played in chat
```

### Encryption Implementation
- **Algorithm**: Fernet (AES-128 in CBC mode with HMAC)
- **Key Generation**: Secure random key generation using `cryptography.fernet`
- **Session Keys**: Unique encryption keys per chat session
- **No Storage**: Encrypted files never saved to disk
- **In-Memory**: All encryption/decryption happens in memory

Users don't need to do anything - encryption happens automatically for both messages and files!

### Real-time Media Features
- **Images**: Display inline immediately after decryption
- **Videos**: Stream and play directly in chat interface
- **No Downloads**: View/play without downloading to device
- **Secure Streaming**: Encrypted during transmission
- **Format Support**: JPEG, PNG, MP4, WebM, and more

## 🌐 Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Client A  │ ←─────→ │   FastAPI    │ ←─────→ │   Redis     │
└─────────────┘         │   Socket.IO  │         │   (Cache)   │
                        └──────────────┘         └─────────────┘
┌─────────────┐                ↕                        ↕
│   Client B  │         ┌──────────────┐         ┌─────────────┐
└─────────────┘         │    Kafka     │ ←─────→ │  Encryption │
                        │  (Streaming) │         │   Service   │
┌─────────────┐         └──────────────┘         └─────────────┘
│   Client C  │
└─────────────┘
```

## 🎯 Key Features Explained

### Real-time Messaging
- WebSocket connection for instant message delivery
- No polling - push-based architecture
- Sub-second message latency

### Encrypted File Sharing
- Upload images and videos with one click
- Files encrypted using `cryptography` library (Fernet)
- Real-time decryption and display in chat
- Videos play directly in chat interface
- Images display inline without download
- Supports: JPG, PNG, GIF, MP4, WebM, AVI

### No Data Persistence
- Messages stored only in Redis (in-memory)
- Automatic cleanup on user disconnect
- No database storage - complete privacy

### User Presence
- Real-time tracking of online users
- Join/leave notifications with timestamps
- Active user list display

### Scalability
- Redis for session management
- Kafka for message distribution across servers
- Horizontal scaling support

## 🔧 Configuration

### Redis Configuration
```python
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True
}
```

### Kafka Configuration
```python
KAFKA_CONFIG = {
    'bootstrap_servers': ['localhost:9092'],
    'topic': 'chat_messages',
    'group_id': 'chat_group'
}
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Chat interface |
| `/chat_router` | WebSocket | Real-time chat connection |
| `/health` | GET | Health check endpoint |

## 🐛 Troubleshooting

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if not running
redis-server
```

### Kafka Connection Error
```bash
# Check Kafka status
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Create topic if needed
bin/kafka-topics.sh --create --topic chat_messages --bootstrap-server localhost:9092
```

### WebSocket Connection Failed
- Check firewall settings
- Ensure port 8000 is not blocked
- Verify CORS settings in main.py

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Developer

Built with Python, FastAPI, Socket.IO, Redis, and Kafka

## 📞 Support

For issues and questions, please open an issue in the GitHub repository.

## ⚠️ Important Notes

- **No Chat History**: Messages are not stored - this is by design for privacy
- **Session-based**: Each chat session is independent
- **Encryption**: All messages are encrypted in transit
- **Temporary Files**: Uploaded files are automatically cleaned up
- **Redis Required**: Redis must be running for the application to work
- **Production**: Use environment variables for sensitive configuration

---

**StreamChat** - Secure, Ephemeral, Real-time Group Communication