# Test file for gilded rose kata

import io
from itertools import product
from pathlib import Path

from gilded_rose.refactored import Item, GildedRose


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


def test_random_named_item_with_quality_gt_0():
    items = [Item("Foo", 0, 10)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Foo", -1, 8) == items[0])


def test_item_repr():
    item = Item("bar", 1, 2)

    assert("bar, 1, 2" == str(item))


def test_aged_brie_named_item_with_quality_eq_50():
    items = [Item("Aged Brie", 0, 50)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Aged Brie", -1, 50) == items[0])


def test_aged_brie_named_item_with_quality_gt_50():
    items = [Item("Aged Brie", 0, 51)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Aged Brie", -1, 51) == items[0])


def test_aged_brie_named_item_with_quality_lt_50():
    items = [Item("Aged Brie", 0, 45)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Aged Brie", -1, 47) == items[0])


def test_backstage_named_item_with_quality_lt_50():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 47)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Backstage passes to a TAFKAL80ETC concert", 4, 50) == items[0])


def test_backstage_named_item_with_sell_in_eq_0():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 100)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Backstage passes to a TAFKAL80ETC concert", -1, 0) == items[0])


def test_sulfuras_named_item():
    items = [Item("Sulfuras, Hand of Ragnaros", 0, 0)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Sulfuras, Hand of Ragnaros", 0, 0) == items[0])


def test_sulfuras_named_item_with_quality_gt_0():
    items = [Item("Sulfuras, Hand of Ragnaros", 0, 5)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item("Sulfuras, Hand of Ragnaros", 0, 5) == items[0])

