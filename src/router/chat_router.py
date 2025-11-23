# import socketio
# from datetime import timedelta,datetime

# # Create a Socket.IO instance
# sio = socketio.AsyncServer(
#     async_mode='asgi',
#     cors_allowed_origins="*",
#     logger=True,
#     engineio_logger=True
# )

# # Store connected users
# connected_users = {}


# @sio.event
# async def connect(sid, environ):
#     print(f"Client connected: {sid}")

# @sio.event
# async def join(sid, data):
#     username = data.get('username')
#     if username:
#         connected_users[sid] = username
#         print(f"User {username} joined with SID: {sid}")
        
#         # Send welcome message to the user
#         await sio.emit('chat_message', {
#             'username': 'System',
#             'message': f'Welcome to the grouped chat, {username}!',
#             'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
#         }, room=sid)
        
#         # Notify others that a new user joined
#         await sio.emit('chat_message', {
#             'username': 'System',
#             'message': f'{username} has joined the chat',
#             'timestamp': datetime.now().strftime('%I:%M:%S %p')
#         }, skip_sid=sid)
        
#         # Send updated user list to all clients
#         await sio.emit('user_list', {
#             'users': list(connected_users.values())
#         })

# @sio.event
# async def chat_message(sid, data):
#     username = connected_users.get(sid)
#     if username:
#         # Broadcast the message to all clients
#         await sio.emit('chat_message', data)

# @sio.event
# async def disconnect(sid):
#     username = connected_users.pop(sid, None)
#     if username:
#         print(f"User {username} disconnected")
        
#         # Notify others that a user left
#         await sio.emit('chat_message', {
#             'username': 'System',
#             'message': f'{username} has left the chat',
#             'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
#         })
        
#         # Send updated user list to all clients
#         await sio.emit('user_list', {
#             'users': list(connected_users.values())
#         })

import socketio
from datetime import datetime
from cryptography.fernet import Fernet
import base64
import os

# Create a Socket.IO instance
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

# Store connected users and encryption keys
connected_users = {}
session_keys = {}  # Store encryption keys per session

# Generate or load master encryption key
# In production, load this from environment variable
MASTER_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(MASTER_KEY)


def encrypt_message(message: str) -> str:
    """Encrypt a text message"""
    try:
        encrypted = cipher_suite.encrypt(message.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return message


def decrypt_message(encrypted_message: str) -> str:
    """Decrypt a text message"""
    try:
        decoded = base64.urlsafe_b64decode(encrypted_message.encode())
        decrypted = cipher_suite.decrypt(decoded)
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return encrypted_message


def encrypt_file_data(file_data: str) -> str:
    """Encrypt file data (base64 encoded)"""
    try:
        # File data is already base64, encode it again after encryption
        encrypted = cipher_suite.encrypt(file_data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        print(f"File encryption error: {e}")
        return file_data


def decrypt_file_data(encrypted_data: str) -> str:
    """Decrypt file data"""
    try:
        decoded = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = cipher_suite.decrypt(decoded)
        return decrypted.decode()
    except Exception as e:
        print(f"File decryption error: {e}")
        return encrypted_data


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    # Generate a unique session key for this connection
    session_keys[sid] = Fernet.generate_key()
    print(f"Session key generated for {sid}")


@sio.event
async def join(sid, data):
    username = data.get('username')
    if username:
        # Encrypt username before storing
        encrypted_username = encrypt_message(username)
        connected_users[sid] = username  # Store plain for display
        
        print(f"User {username} joined with SID: {sid}")
        
        # Send welcome message to the user
        welcome_msg = f'Welcome to the encrypted group chat, {username}!'
        await sio.emit('chat_message', {
            'username': 'System',
            'message': welcome_msg,
            'encrypted': False,  # System messages not encrypted
            'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        }, room=sid)
        
        # Notify others that a new user joined
        join_msg = f'{username} has joined the chat'
        await sio.emit('chat_message', {
            'username': 'System',
            'message': join_msg,
            'encrypted': False,
            'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        }, skip_sid=sid)
        
        # Send updated user list to all clients
        await sio.emit('user_list', {
            'users': list(connected_users.values())
        })


@sio.event
async def chat_message(sid, data):
    username = connected_users.get(sid)
    if username:
        try:
            # Encrypt the message
            original_message = data.get('message', '')
            encrypted_msg = encrypt_message(original_message) if original_message else ''
            
            # Encrypt file data if present
            file_data = data.get('fileData')
            encrypted_file = None
            if file_data:
                print(f"Encrypting file from {username}")
                encrypted_file = encrypt_file_data(file_data)
            
            # Prepare encrypted data packet
            encrypted_data = {
                'username': username,
                'message': encrypted_msg,
                'encrypted': True,
                'timestamp': data.get('timestamp', datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))
            }
            
            # Add encrypted file data if present
            if encrypted_file:
                encrypted_data['fileData'] = encrypted_file
                encrypted_data['fileType'] = data.get('fileType')
                encrypted_data['fileName'] = data.get('fileName')
            
            # Broadcast the encrypted message to all clients
            await sio.emit('chat_message', encrypted_data)
            
            print(f"Encrypted message from {username} broadcasted")
            
        except Exception as e:
            print(f"Error processing message: {e}")
            # Send error notification
            await sio.emit('chat_message', {
                'username': 'System',
                'message': 'Error: Failed to encrypt message',
                'encrypted': False,
                'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
            }, room=sid)


@sio.event
async def decrypt_request(sid, data):
    """Handle client-side decryption requests"""
    try:
        encrypted_msg = data.get('encrypted_message')
        decrypted = decrypt_message(encrypted_msg)
        
        await sio.emit('decrypted_message', {
            'decrypted': decrypted
        }, room=sid)
    except Exception as e:
        print(f"Decryption request error: {e}")


@sio.event
async def disconnect(sid):
    username = connected_users.pop(sid, None)
    session_keys.pop(sid, None)  # Remove session key
    
    if username:
        print(f"User {username} disconnected")
        
        # Notify others that a user left
        leave_msg = f'{username} has left the chat'
        await sio.emit('chat_message', {
            'username': 'System',
            'message': leave_msg,
            'encrypted': False,
            'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        })
        
        # Send updated user list to all clients
        await sio.emit('user_list', {
            'users': list(connected_users.values())
        })


# Utility function for testing encryption
def test_encryption():
    """Test encryption/decryption"""
    test_msg = "Hello, this is a secret message!"
    encrypted = encrypt_message(test_msg)
    decrypted = decrypt_message(encrypted)
    
    print(f"Original: {test_msg}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_msg == decrypted}")


if __name__ == "__main__":
    test_encryption()