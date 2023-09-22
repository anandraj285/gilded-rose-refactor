class GildedRose(object):
    
    MAX_ITEM_QUALITY = 50

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self.update_item_quality(item)
            self.update_sell_in(item)         

    def update_item_quality(self, item):
        if item.name == "Sulfuras, Hand of Ragnaros":
            return  # Legendary item, quality never changes
        if item.name == "Aged Brie":
            self.update_aged_brie_quality(item)            
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            self.update_backstage_pass_quality(item)            
        elif item.name == "Conjured Mana Cake":        
            self.update_conjured_quality(item)            
        else:
            self.update_standard_item_quality(item)            

    def update_aged_brie_quality(self, item):
        # "Aged Brie" actually increases in Quality the older it gets
        item.quality = min(50, item.quality + 1)        

    def update_backstage_pass_quality(self, item):
        if item.sell_in <= 0:
            # Quality drops to 0 after the concert
            item.quality = 0
        elif item.sell_in <= 5:
            # Quality increases by 3 when there are 5 days or less
            item.quality = min(50, item.quality + 3)
        elif item.sell_in <= 10:
            # Quality increases by 2 when there are 10 days or less
            item.quality = min(50, item.quality + 2)
        else:
            # Default
            item.quality = min(50, item.quality + 1)                

    def update_conjured_quality(self, item):
        #"Conjured" items degrade in Quality twice as fast as normal items            
        if item.sell_in <= 0:
            item.quality = min(50,max(0, item.quality - 4))  # Quality degrades by 4 after sell-by date
        else:
            item.quality = min(50,max(0, item.quality - 2))
        

    def update_standard_item_quality(self, item):
         # Regular items degrade quality twice as fast if sell_by date has passed        
        if item.sell_in <= 0:
            item.quality = min(50,max(0, item.quality - 2))
        else:
            item.quality = min(50,max(0, item.quality - 1))

    def update_sell_in(self, item):
        if item.name != "Sulfuras, Hand of Ragnaros":
            item.sell_in -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

