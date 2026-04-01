from src.database import Database
from src.Device import Device
import time

class MotionCamera(Device):
    def __init__(self, id):
        super().__init__(id)
        self._type = "mcamera"
        self.db = Database.get_connection()
    
    def save_capture(self, file_id, faccess):
        self.db.motion_capture.insert_one({
            "file_id": file_id,
            "time": time.time(),
            "device_id": self.id,
            "owner": self.collection.user,
            "faccess": faccess
        })
        