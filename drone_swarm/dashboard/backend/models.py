from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database import Base

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"

    id = Column(Integer, primary_key=True, index=True)
    drone_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    battery = Column(Integer)
    altitude = Column(Float)
    pitch = Column(Integer)
    roll = Column(Integer)
    yaw = Column(Integer)
    temperature = Column(Float)