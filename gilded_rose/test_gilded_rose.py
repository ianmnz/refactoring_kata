# Test file for gilded rose kata

import io
import pytest
import random
from itertools import product
from pathlib import Path

from gilded_rose.refactored import (
    Item,
    GildedRose,
    AGED_BRIE_STR,
    SULFURAS_STR,
    BACKSTAGE_PASS_STR,
    QUALITY_UPPER_THRESHOLD,
    SELL_IN_MIDDLE_THRESHOLD,
    SELL_IN_UPPER_THRESHOLD,
)

ANY_VALUE = 100
random.seed(13)


@pytest.mark.skip(reason="Used only for creating a reference before code refactoring")
def test_golden_master():
    golden_master_file = Path('gilded_rose/golden_master.txt')

    name_values = ["",
                   AGED_BRIE_STR,
                   BACKSTAGE_PASS_STR,
                   SULFURAS_STR,
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
    sell_in = random.randint(-ANY_VALUE, ANY_VALUE)
    quality = random.randint(-ANY_VALUE, ANY_VALUE)
    items = [Item(SULFURAS_STR, sell_in, quality)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(Item(SULFURAS_STR, sell_in, quality) == items[0])


def test_any_name_item_decrements_sell_in():
    quality = random.randint(-ANY_VALUE, ANY_VALUE)
    sell_in = random.randint(-ANY_VALUE, ANY_VALUE)
    items = [
        Item(AGED_BRIE_STR, sell_in, quality),
        Item(BACKSTAGE_PASS_STR, sell_in, quality),
        Item("Foo", sell_in, quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].sell_in == sell_in - 1)
    assert(items[1].sell_in == sell_in - 1)
    assert(items[2].sell_in == sell_in - 1)


def test_backstage_named_item_with_sell_in_leq_0():
    items = [
        Item(BACKSTAGE_PASS_STR,
             random.randint(-ANY_VALUE, 0),
             random.randint(-ANY_VALUE, ANY_VALUE))
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == 0)


def test_backstage_named_item_with_quality_eq_49():
    items = [
        Item(BACKSTAGE_PASS_STR,
             random.randint(1, ANY_VALUE),
             QUALITY_UPPER_THRESHOLD - 1),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == QUALITY_UPPER_THRESHOLD)


def test_backstage_named_item_with_sell_in_gt_0_and_quality_lt_49():
    quality = random.randint(-ANY_VALUE, QUALITY_UPPER_THRESHOLD - 2)
    small_sell_in = random.randint(1, SELL_IN_MIDDLE_THRESHOLD)
    avg_sell_in = random.randint(SELL_IN_MIDDLE_THRESHOLD + 1, SELL_IN_UPPER_THRESHOLD)
    big_sell_in = random.randint(SELL_IN_UPPER_THRESHOLD + 1, ANY_VALUE)
    items = [
        Item(BACKSTAGE_PASS_STR, small_sell_in, quality),
        Item(BACKSTAGE_PASS_STR, avg_sell_in, quality),
        Item(BACKSTAGE_PASS_STR, big_sell_in, quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality + 3)
    assert(items[1].quality == quality + 2)
    assert(items[2].quality == quality + 1)


def test_backstage_named_item_with_quality_geq_50():
    quality = random.randint(QUALITY_UPPER_THRESHOLD, ANY_VALUE)
    items = [
        Item(BACKSTAGE_PASS_STR, random.randint(1, ANY_VALUE), quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality)


def test_aged_brie_named_item_with_quality_eq_49():
    items = [
        Item(AGED_BRIE_STR,
             random.randint(-ANY_VALUE, ANY_VALUE),
             QUALITY_UPPER_THRESHOLD - 1),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == QUALITY_UPPER_THRESHOLD)


def test_aged_brie_named_item_with_quality_lt_49():
    quality = random.randint(-ANY_VALUE, QUALITY_UPPER_THRESHOLD - 2)
    items = [
        Item(AGED_BRIE_STR, random.randint(-ANY_VALUE, 0), quality),
        Item(AGED_BRIE_STR, random.randint(1, ANY_VALUE), quality)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality + 2)
    assert(items[1].quality == quality + 1)


def test_aged_brie_named_item_with_quality_geq_50():
    quality = random.randint(QUALITY_UPPER_THRESHOLD, ANY_VALUE)
    items = [
        Item(AGED_BRIE_STR,
             random.randint(-ANY_VALUE, ANY_VALUE),
             quality),
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality)


def test_other_named_item_with_quality_eq_1():
    items = [
        Item("Foo", random.randint(-ANY_VALUE, 0), 1),
        Item("Bar", random.randint(1, ANY_VALUE), 1)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == 0)
    assert(items[1].quality == 0)


def test_other_named_item_with_quality_gt_1():
    quality = random.randint(2, ANY_VALUE)
    items = [
        Item("Foo", random.randint(-ANY_VALUE, 0), quality),
        Item("Bar", random.randint(1, ANY_VALUE), quality)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality - 2)
    assert(items[1].quality == quality - 1)


def test_other_named_item_with_quality_leq_0():
    quality = random.randint(-ANY_VALUE, 0)
    sell_in = random.randint(-ANY_VALUE, ANY_VALUE)
    items = [
        Item("Foo", sell_in, quality),
        Item("Bar", sell_in, quality)
    ]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert(items[0].quality == quality)
    assert(items[1].quality == quality)
