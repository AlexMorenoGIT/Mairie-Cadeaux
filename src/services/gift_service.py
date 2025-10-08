from typing import List, Dict, Optional

from src.models.gifts import GiftModel


class GiftsService:
    @staticmethod
    def get_all_gifts() -> List[Dict]:
        return GiftModel.get_all()

    @staticmethod
    def get_gift_by_id(giftid: int) -> Optional[Dict]:
        return GiftModel.get_by_id(giftid)

    @staticmethod
    def get_gift_by_age(age:int) -> Optional[Dict]:
        return GiftModel.get_by_age(age)