# Test file for gilded rose kata

import io
import pytest
import random
from itertools import product
from pathlib import Path

from gilded_rose.refactored import Item, GildedRose


# @pytest.mark.skip(reason="")
def test_golden_master():
    golden_master_file = Path('gilded_rose/golden_master.txt')

    name_values = ["",
                   "Aged Brie",
                   "Backstage passes to a TAFKAL80ETC concert",
                   "Sulfuras, Hand of Ragnaros",
                   "Foo"]

    sell_in_values = range(-10, 20, 5)
    quality_values = range(-10, 60, 5)

    items = [Item(name, sell_in, quality)
             for name, sell_in, quality in product(name_values, sell_in_values, quality_values)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    if (WRITE_GOLDEN_MASTER := False):
        with open(golden_master_file, 'w') as file:
            for item in items:
                file.write(f"{item}\n")

        assert(False)
    else:
        buffer = io.StringIO()
        for item in gilded_rose.items:
            buffer.write(f"{item}\n")

        with open(golden_master_file, 'r') as file:
            reference = file.read()

        assert(buffer.getvalue() == reference)


def test_null_item():
    items = [Item("", 0, 0)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("", -1, 0) == items[0])


def test_item_repr():
    item = Item("bar", 1, 2)

    assert("bar, 1, 2" == str(item))


def test_sulfuras_named_item_dont_change():
    random.seed(1)
    sell_in = random.randint(-100, 100)
    quality = random.randint(-100, 100)
    items = [Item("Sulfuras, Hand of Ragnaros", sell_in, quality)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Sulfuras, Hand of Ragnaros", sell_in, quality) == items[0])


def test_any_name_item_decrements_sell_in():
    random.seed(2)
    quality = random.randint(-100, 100)
    sell_in = random.randint(-100, 100)
    items = [
        Item("Aged Brie", sell_in, quality),
        Item("Backstage passes to a TAFKAL80ETC concert", sell_in, quality),
        Item("Foo", sell_in, quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].sell_in == sell_in - 1)
    assert(items[1].sell_in == sell_in - 1)
    assert(items[2].sell_in == sell_in - 1)


def test_backstage_named_item_with_sell_in_leq_0():
    random.seed(3)
    items = [
        Item("Backstage passes to a TAFKAL80ETC concert",
             random.randint(-100, 0),
             random.randint(-100, 100))
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == 0)


def test_backstage_named_item_with_quality_eq_49():
    random.seed(4)
    items = [
        Item("Backstage passes to a TAFKAL80ETC concert", random.randint(1, 100), 49),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == 50)


def test_backstage_named_item_with_sell_in_gt_0_and_quality_lt_49():
    random.seed(4)
    quality = random.randint(-100, 48)
    small_sell_in = random.randint(1, 5)
    avg_sell_in = random.randint(6, 10)
    big_sell_in = random.randint(11, 100)
    items = [
        Item("Backstage passes to a TAFKAL80ETC concert", small_sell_in, quality),
        Item("Backstage passes to a TAFKAL80ETC concert", avg_sell_in, quality),
        Item("Backstage passes to a TAFKAL80ETC concert", big_sell_in, quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality + 3)
    assert(items[1].quality == quality + 2)
    assert(items[2].quality == quality + 1)


def test_backstage_named_item_with_quality_geq_50():
    random.seed(4)
    quality = random.randint(50, 100)
    items = [
        Item("Backstage passes to a TAFKAL80ETC concert", random.randint(1, 100), quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality)


def test_aged_brie_named_item_with_quality_eq_49():
    random.seed(5)
    items = [
        Item("Aged Brie", random.randint(-100, 100), 49),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == 50)


def test_aged_brie_named_item_with_quality_lt_49():
    random.seed(5)
    quality = random.randint(-100, 48)
    items = [
        Item("Aged Brie", random.randint(-100, 0), quality),
        Item("Aged Brie", random.randint(1, 100), quality)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality + 2)
    assert(items[1].quality == quality + 1)


def test_aged_brie_named_item_with_quality_geq_50():
    random.seed(5)
    quality = random.randint(50, 100)
    items = [
        Item("Aged Brie", random.randint(-100, 100), quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality)


def test_other_named_item_with_quality_eq_1():
    random.seed(6)
    items = [
        Item("Foo", random.randint(-100, 0), 1),
        Item("Bar", random.randint(1, 100), 1)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == 0)
    assert(items[1].quality == 0)


def test_other_named_item_with_quality_gt_1():
    random.seed(6)
    quality = random.randint(2, 100)
    items = [
        Item("Foo", random.randint(-100, 0), quality),
        Item("Bar", random.randint(1, 100), quality)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality - 2)
    assert(items[1].quality == quality - 1)


def test_other_named_item_with_quality_leq_0():
    random.seed(7)
    quality = random.randint(-100, 0)
    sell_in = random.randint(-100, 100)
    items = [
        Item("Foo", sell_in, quality),
        Item("Bar", sell_in, quality)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality)
    assert(items[1].quality == quality)
