from src.utils.db_manager import DBManager


class BaseServiceLayer:
    """
    Чтобы не тянуть постоянно db, а брать из класса
    """
    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db