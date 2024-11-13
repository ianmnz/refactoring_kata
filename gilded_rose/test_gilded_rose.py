from gilded_rose.refactored import Item, GildedRose

def test_null():
    items = [Item("", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert("" == items[0].name)
    assert(0 == items[0].quality)
    assert(-1 == items[0].sell_in)


def test_foo():
    items = [Item("foo", 0, 10)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert("foo" == items[0].name)
    assert(8 == items[0].quality)
    assert(-1 == items[0].sell_in)

def test_item():
    item = Item("bar", 1, 2)
    assert("bar, 1, 2" == str(item))

def test_aged_brie_51():
    items = [Item("Aged Brie", 0, 51)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert("Aged Brie" == items[0].name)
    assert(51 == items[0].quality)
    assert(-1 == items[0].sell_in)

def test_aged_brie_48():
    items = [Item("Aged Brie", 0, 48)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert("Aged Brie" == items[0].name)
    assert(50 == items[0].quality)
    assert(-1 == items[0].sell_in)

def test_backstage():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 47)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert("Backstage passes to a TAFKAL80ETC concert" == items[0].name)
    assert(50 == items[0].quality)
    assert(4 == items[0].sell_in)

def test_backstage_sell_in():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 100)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert("Backstage passes to a TAFKAL80ETC concert" == items[0].name)
    assert(0 == items[0].quality)
    assert(-1 == items[0].sell_in)

def test_sulfuras():
    items = [Item("Sulfuras, Hand of Ragnaros", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert("Sulfuras, Hand of Ragnaros" == items[0].name)
    assert(0 == items[0].quality)
    assert(0 == items[0].sell_in)

