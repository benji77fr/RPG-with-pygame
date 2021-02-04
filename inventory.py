import pygame as pg
from settings import *

class Inventory:
    def __init__(self, player, totalSlots, row, col, isNew):
        self.player = player
        self.totalSlots = totalSlots
        self.row = row
        self.col = col
        self.inventorySlots = []
        self.displayInvetory = False
        self.isNew = isNew
        self.create_inventory()

        self.movingItem = None
        self.movingItemSlot = None

    
    def create_inventory(self):
        if self.isNew:
            for x in range(WIDTH // 2 - ((32 + 2) * self.col) // 2, WIDTH // 2 + ((32 + 2) * self.col) // 2, 32 + 2):
                for y in range(200, (200+32) * self.row, 32 + 2):
                    self.inventorySlots.append(InventorySlot(x,y))
    
    def draw(self, screen):
        if self.displayInvetory:
            for slot in self.inventorySlots:
                slot.draw(screen)
    
    def toggle_inventory(self):
        self.displayInvetory = not self.displayInvetory

class InventorySlot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None

    def draw(self, screen):
        return pg.draw.rect(screen, (255, 255, 255), (self.x, self.y, 32, 32))