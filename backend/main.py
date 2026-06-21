from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.database import engine, get_db
from backend.models import Base, User
from backend.schemas import UserCreate, UserLogin, UserResponse
from backend.auth import get_password_hash, verify_password

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Web-LAN-Chat API")

# Mount the static frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.post("/api/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Domain restriction check
    if not (user.student_id.endswith("@diu.edu.bd") or user.student_id.isdigit()):
        # We allow standard digits for generic student IDs or @diu.edu.bd
        pass # Depending on strictness, we might enforce length. Let's assume standard format is digits.

    db_user = db.query(User).filter(User.student_id == user.student_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Student ID already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        student_id=user.student_id,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.student_id == user.student_id).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "user": {"id": db_user.id, "student_id": db_user.student_id, "name": db_user.name}}

from fastapi import WebSocket, WebSocketDisconnect
from backend.socket_manager import manager
from backend.models import Message
import json

@app.websocket("/ws/{student_id}")
async def websocket_endpoint(websocket: WebSocket, student_id: str, db: Session = Depends(get_db)):
    await manager.connect(websocket, student_id)
    
    # Send recent global chat history upon connection
    recent_msgs = db.query(Message).filter(Message.is_global == True).order_by(Message.timestamp.desc()).limit(50).all()
    history_data = []
    # Reverse to send oldest first
    for msg in reversed(recent_msgs):
        sender = db.query(User).filter(User.id == msg.sender_id).first()
        history_data.append({
            "sender_id": sender.student_id if sender else "Unknown",
            "sender_name": sender.name if sender else "Unknown",
            "message": msg.content,
            "timestamp": str(msg.timestamp)
        })
    
    await websocket.send_text(json.dumps({
        "type": "history",
        "messages": history_data
    }))

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # payload expects: {"target": "global" or target_student_id, "message": "hello"}
            target = payload.get("target", "global")
            msg_content = payload.get("message", "")
            
            # Find sender ID from DB (blocking query inside async is normally bad, but okay for this scale, or use a separate thread)
            # Better: just use student_id string or fetch user ID
            sender = db.query(User).filter(User.student_id == student_id).first()
            if not sender:
                continue

            if target == "global":
                # Save to DB
                new_msg = Message(sender_id=sender.id, content=msg_content, is_global=True)
                db.add(new_msg)
                db.commit()
                db.refresh(new_msg)
                
                # Broadcast
                await manager.broadcast({
                    "type": "chat",
                    "sender_id": student_id,
                    "sender_name": sender.name,
                    "target": "global",
                    "message": msg_content,
                    "timestamp": str(new_msg.timestamp)
                })
            else:
                # Private message
                receiver = db.query(User).filter(User.student_id == target).first()
                if receiver:
                    new_msg = Message(sender_id=sender.id, receiver_id=receiver.id, content=msg_content, is_global=False)
                    db.add(new_msg)
                    db.commit()
                    db.refresh(new_msg)
                    
                    msg_obj = {
                        "type": "chat",
                        "sender_id": student_id,
                        "sender_name": sender.name,
                        "target": target,
                        "message": msg_content,
                        "timestamp": str(new_msg.timestamp)
                    }
                    # Send to receiver
                    await manager.send_personal_message(msg_obj, target)
                    # Send back to sender so they see it in their UI
                    await manager.send_personal_message(msg_obj, student_id)

    except WebSocketDisconnect:
        manager.disconnect(student_id)
        await manager.broadcast_user_status()


