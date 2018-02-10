# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 15:56:45 2018

@author: fhales
"""

class player:
    def __init__(self, health, money, deck, items):
        self.health = health
        self.money = money
        self.deck = deck
        self.items = items

class deck:
    def __init__(self, cards):
        self.cards = cards

class card:
    def __init__(self, name, cost, effect, rarity):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.rarity = rarity

class monster:
    def __init__(self, health, attacks, challange):
        self.health = health
        self.attacks = attacks
        self.challange = challange

class attack:
    def __init__(self, effect, power):
        self.effect = effect
        self.power = power