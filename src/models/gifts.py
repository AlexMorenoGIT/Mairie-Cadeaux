from typing import List, Dict, Optional

from src.utils import execute_query


class GiftModel:
    @staticmethod
    def get_all() -> List[Dict]:
        query = "SELECT * FROM gifts"
        return execute_query(query)

    @staticmethod
    def get_by_id(id: int) -> Optional[Dict]:
        query = "SELECT * FROM gifts WHERE gift_id = ?"
        results = execute_query(query, (id,))
        return results[0] if results else None

    @staticmethod
    def get_by_age(age: int) -> Optional[Dict]:
        query = "SELECT * FROM gifts WHERE min_age <= ? AND max_age >= ? ORDER BY quantity DESC LIMIT 1;"
        results = execute_query(query, (age,age))
        print(results)
        return results[0] if results else None
