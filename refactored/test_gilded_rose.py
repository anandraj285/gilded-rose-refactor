import unittest
import timeit

from .gilded_rose import GildedRose, Item

class TestGildedRose(unittest.TestCase):

    def test_standard_item_quality_degradation(self):
        # Test that a normal item's quality degrades by 1 at the end of the day
        items = [Item("Standard Item", sell_in=5, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 4)
        self.assertEqual(items[0].quality, 9)

    def test_quality_never_negative(self):
        # Test quality is never negative
        items = [Item("Standard Item", sell_in=5, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 0)

    def test_quality_never_more_than_50(self):
        # Test that an item's quality is never more than 50
        items = [Item("Aged Brie", sell_in=5, quality=80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 50)

    def test_aged_brie_quality_increase(self):
        # Test that "Aged Brie" increases in quality as it gets older
        items = [Item("Aged Brie", sell_in=5, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 4)
        self.assertEqual(items[0].quality, 11)

    def test_sell_in_passed_quality_degrades_twice(self):
        # Test that quality degrades twice as fast once sell-in has passed
        items = [Item("Standard Item", sell_in=0, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 8)

    def test_sulfuras_quality_never_changes(self):
        # Test that "Sulfuras" quality never changes
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 5)
        self.assertEqual(items[0].quality, 80)

    def test_backstage_passes_quality_increase(self):
        # Test "Backstage passes" quality increase
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 14)
        self.assertEqual(items[0].quality, 21)

    def test_backstage_passes_quality_increase_10_days_or_less(self):
        # Test "Backstage passes" quality increase by 2 when there are 10 days or less
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 22)

    def test_backstage_passes_quality_increase_5_days_or_less(self):
        # Test "Backstage passes" quality increase by 3 when there are 5 days or less
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 4)
        self.assertEqual(items[0].quality, 23)

    def test_backstage_passes_quality_drops_to_zero(self):
        # Test "Backstage passes" quality drops to 0 after the concert
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 0)

    def test_conjured_items_quality_degradation(self):
        # Test that "Conjured" items degrade in quality twice as fast as normal items
        items = [Item("Conjured Mana Cake", sell_in=5, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 4)
        self.assertEqual(items[0].quality, 8)

    def test_conjured_items_quality_degradation_t(self):
        # Test that "Conjured" items degrade in quality twice as fast as normal items
        items = [Item("Conjured Mana Cake", sell_in=0, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 6)


    def test_negative_sell_in(self):
        # Test how items behave when their sell_in values are already negative
        items = [Item("Standard Item", sell_in=-1, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -2)
        self.assertEqual(items[0].quality, 8)  # Quality degrades twice as fast

    def test_starting_quality_above_50(self):
        # Test items with starting qualities above 50 to ensure they are capped at 50
        items = [Item("Standard Item", sell_in=5, quality=55)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 4)
        self.assertEqual(items[0].quality, 50)  # Quality is capped at 50


    def test_mixed_item_types(self):
        # Test a mixture of different item types in the same list
        items = [
            Item("Normal Item", sell_in=5, quality=10),
            Item("Aged Brie", sell_in=3, quality=30),
            Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        # Validate the behavior of each item type
        self.assertEqual(items[0].quality, 9)  # Normal Item
        self.assertEqual(items[1].quality, 31)  # Aged Brie
        self.assertEqual(items[2].quality, 80)  # Sulfuras    

    def test_performance(self):
        # Test the performance
        num_items = [10, 100, 1000, 10000]  # Test with different numbers of items
        for n in num_items:
            items = [Item("Normal Item", sell_in=5, quality=10) for _ in range(n)]
            gilded_rose = GildedRose(items)
            # Measure the execution time for updating quality
            execution_time = timeit.timeit(lambda: gilded_rose.update_quality(), number=10)
            print(f"Number of items: {n}, Execution time: {execution_time} seconds")


if __name__ == '__main__':
    unittest.main()


