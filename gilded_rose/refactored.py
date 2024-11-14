from dataclasses import dataclass
from typing import List


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
        if item.name == "Sulfuras, Hand of Ragnaros":
            return

        item.sell_in -= 1

        if item.name == "Aged Brie":
            if item.quality < 50:
                item.quality += 1

                if item.sell_in < 0:
                    item.quality = min(50, item.quality + 1)

        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            if item.sell_in < 0:
                item.quality = 0

            elif item.quality < 50:
                item.quality += 1

                d_quality = 0
                if item.sell_in < 5:
                    d_quality = 2

                elif item.sell_in < 10:
                    d_quality = 1

                item.quality = min(50, item.quality + d_quality)

        else:   # Any other name
            if item.quality > 0:
                item.quality -= 1

                if item.sell_in < 0:
                    item.quality = max(0, item.quality - 1)
