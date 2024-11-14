from dataclasses import dataclass
from typing import List


SULFURAS_STR = "Sulfuras, Hand of Ragnaros"
AGED_BRIE_STR = "Aged Brie"
BACKSTAGE_PASS_STR = "Backstage passes to a TAFKAL80ETC concert"

QUALITY_UPPER_THRESHOLD = 50
SELL_IN_MIDDLE_THRESHOLD = 5
SELL_IN_UPPER_THRESHOLD = 10


@dataclass
class Item:
    name: str
    sell_in: int
    quality: int

    def __repr__(self) -> str:
        return f"{self.name}, {self.sell_in}, {self.quality}"


class GildedRose(object):

    def __init__(self, items: List[Item]) -> None:
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            self.update_item_quality(item)

    def update_item_quality(self, item: Item) -> None:
        if item.name == SULFURAS_STR:
            return

        item.sell_in -= 1

        if item.name == AGED_BRIE_STR:
            if item.quality < QUALITY_UPPER_THRESHOLD:
                item.quality += 1

                if item.sell_in < 0:
                    item.quality = min(QUALITY_UPPER_THRESHOLD, item.quality + 1)

        elif item.name == BACKSTAGE_PASS_STR:
            if item.sell_in < 0:
                item.quality = 0

            elif item.quality < QUALITY_UPPER_THRESHOLD:
                item.quality += 1

                d_quality = 0
                if item.sell_in < SELL_IN_MIDDLE_THRESHOLD:
                    d_quality = 2

                elif item.sell_in < SELL_IN_UPPER_THRESHOLD:
                    d_quality = 1

                item.quality = min(QUALITY_UPPER_THRESHOLD, item.quality + d_quality)

        else:   # Any other name
            if item.quality > 0:
                item.quality -= 1

                if item.sell_in < 0:
                    item.quality = max(0, item.quality - 1)
