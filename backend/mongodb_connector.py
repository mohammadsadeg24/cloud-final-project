# backend/mongodb_connector.py  (سازگار با کد فعلی پروژه)
import os
import time
from urllib.parse import urlparse
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, AutoReconnect

def _extract_db_name(uri: str, fallback: str = "honey") -> str:
    try:
        # اگر در URI بعد از / یک نام دیتابیس هست، همونو بردار
        # مثال: mongodb://host:27017/honey?retryWrites=true
        path = urlparse(uri).path or ""
        name = path.lstrip("/")
        if name and name not in ("admin",):
            return name
    except Exception:
        pass
    return fallback

class MongoDBConnection:
    """
    کانکشن سازگار با کد پروژه:
      - ویژگی های public:
          .client   -> MongoClient
          .database -> Database
      - از ENV ها استفاده می‌کند:
          MONGO_URI (پیش‌فرض: mongodb://mongo:27017/honey)
          MONGO_DB_NAME (اختیاری؛ اگر در URI نباشد)
          MONGO_CONNECT_TIMEOUT (اختیاری، ثانیه؛ پیش‌فرض 5)
    """
    def __init__(self):
        self.uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/honey")
        self.connect_timeout = float(os.getenv("MONGO_CONNECT_TIMEOUT", "5"))
        self.db_name = os.getenv("MONGO_DB_NAME", _extract_db_name(self.uri, "honey"))

        self.client = None
        self.database = None
        self._connect_with_retry()

    def _connect_with_retry(self, retries: int = 12, delay: float = 2.5):
        last_err = None
        for _ in range(retries):
            try:
                self.client = MongoClient(self.uri, serverSelectionTimeoutMS=int(self.connect_timeout * 1000))
                # تست اتصال
                self.client.server_info()
                self.database = self.client[self.db_name]
                return
            except (ServerSelectionTimeoutError, AutoReconnect) as e:
                last_err = e
                print(f"[mongodb_connector] Failed to connect to MongoDB at {self.uri}: {e}. Retrying in {delay}s...")
                time.sleep(delay)
        raise RuntimeError(f"[mongodb_connector] MongoDB connection failed after retries. Last error: {last_err}")

    def get_collection(self, name: str):
        if self.database is None:
            self._connect_with_retry()
        return self.database[name]

# singleton سازگار با import موجود در پروژه
mongodb = MongoDBConnection()