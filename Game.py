# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:24:32 2018

@author: fhales
"""

import yaml
import time
import random
import copy


def play_turn(monster, hand):
    global me
    
    me['shield']=0
    
    print()
    print('Cards in hand:')
    print()
    
    for card in hand:
        print(card+': '+hand[card]['dcr'])
        print()
      
    crd=pick_card(hand)
    
    while crd[0] == '!':
        if show_info(crd, monster, hand) == 1:
            return 0, monster, 0
        crd=pick_card(hand)
    
    if crd != 'pass':
        crd=check_price(crd, hand)
        monster = play_card(crd, monster, hand)
        time.sleep(2)
        monster = monster_turn(monster)
        time.sleep(2)
    status = check_stats(monster)
    time.sleep(2)
    if status == 0:
        return 1, monster, status
    else:
        return 0, monster, status


def show_info(crd, monster, hand):
    global me
    if crd == '!halp':
        print()
        print('List of commands:')
        print('!show deck    --> shows cards in deck')
        print('!show hand    --> shows cards in hand')
        print('!show gold    --> shows current gold')
        print('!show health  --> shows current health')
        print('!show monster --> shows current monsters health')
        print('!end          --> quit game')
        print('pass          --> skips your turn')
        print()
    
    elif crd == '!show deck':
        for card in deck:
            print(card+': '+deck[card]['dcr'])
            print()
    elif crd == '!show hand':
        for card in hand:
            print(card+': '+hand[card]['dcr'])
            print()
    elif crd == '!end':
        return 1
    elif crd == '!show gold':
        print('You have '+str(me['money'])+' gold')
        print()
    elif crd == '!show health':
        print('Your health is '+str(me['health']))
        print()
    elif crd == '!show monster':
        print('Monsters health is '+str(monster['health']))
        print()
    else:
        print('Not a command')
        print()
    return 0


def monster_turn(monster):
    global me
    if monster['health']<1:
        return monster
    else:
        mcard=monster_card(monster)
        
        if monster['health'] + mcard['heal'] > monster['maxhp']:
            heal = monster['maxhp'] - monster['health']
            monster['health'] = monster['maxhp']
        else:
            monster['health'] += mcard['heal']
            heal = mcard['heal']
                
        monster['health']+=-mcard['harm']
        
        monster['shield'] += mcard['shield']
        
        damages=mcard['attack']
        if damages > me['shield']:
            damages =me['shield']
        
        damagep=mcard['attack']-me['shield']
        if damagep < 0:
            damagep = 0
            
        me['health']+=-damagep
        
        if mcard['attack'] != 0:
            print('Monster hits for '+str(mcard['attack'])+' damage!')
        
        if damages != 0:
            print('You block '+str(damages)+' damage')
            
        if mcard['heal'] != 0:
            print('Monster heals '+str(heal)+' health')
            
        if mcard['shield'] != 0:
            print('Monster gains '+str(mcard['shield'])+' shield')
            
        if mcard['harm'] != 0:
            print('Monster loses '+str(mcard['harm'])+' health')
            
        print()
        return monster


def monster_card(monster):
    i=random.sample(list(monster['attacks']),1)[0]
    return monster['attacks'][i]
    


def check_stats(monster):
    global me

    if me['health'] < 1 and monster['health'] > 0:
        return 2
    elif monster['health'] < 1 and me['health'] > 1:
        return 1
    elif monster['health'] < 1 and me['health'] < 1:
        return 3
    
    print('Your health is '+str(me['health']))
    print('Monsters health is '+str(monster['health']))
    print('Your gold is '+str(me['money']))
    return 0


def play_card(crd, monster, hand):
    global me
    me['money']+=-hand[crd]['cost']
    
    if me['health'] + hand[crd]['heal'] > me['maxhp']:
        heal = me['maxhp'] - me['health']        
        me['health'] = me['maxhp']
    else:
        me['health'] += hand[crd]['heal']
        heal = hand[crd]['heal']
        
    me['health'] += -hand[crd]['harm']
    
    me['shield'] += hand[crd]['shield']
    
    damages=hand[crd]['attack']
    if damages > monster['shield']:
        damages =monster['shield']
    
    damagep=hand[crd]['attack']-monster['shield']
    if damagep < 0:
        damagep = 0
        
    monster['health']+=-damagep
    
    if hand[crd]['attack'] != 0:
        print('You hit for '+str(hand[crd]['attack'])+' damage!')
        
    if damages != 0:
        print('Monster blocks '+str(damages)+' damage')
        
    if hand[crd]['heal'] != 0:
        print('You heal '+str(heal)+' health')
        
    if hand[crd]['harm'] != 0:
        print('You lose '+str(hand[crd]['harm'])+' health')
        
    if hand[crd]['shield'] != 0:
        print('You gain '+str(hand[crd]['shield'])+' shield')
        
    if hand[crd]['cost'] < 0:
        print('You find '+str(-hand[crd]['cost'])+' gold')
    print()
    return monster


def check_price(crd, hand):
    while me['money'] < hand[crd]['cost']:
        print('Not enough money')
        crd=pick_card()
    return crd


def pick_card(hand):
    crdpicked = 0
    
    while crdpicked == 0:
        pcard=input('Play a card: ')
        
        if pcard[0] == '!':
            return pcard
        
        for card in hand:
            if pcard == card or pcard == 'pass':
                crdpicked = 1
                
        if crdpicked == 0:
            print('Card not in hand...')
            
    return pcard


def start_game():
    
    with open('card.yaml') as ymlfile:
        cards = yaml.load(ymlfile)
    cardpool=cards
    
    with open('player.yaml') as ymlfile:
        player = yaml.load(ymlfile)
        
    me=player['me']
    
    deck = {}
    
    for card in me['deck']:
        deck[card] = cardpool[card]
    
    return me, cardpool, deck


def fight(monster):
    global me
    global deck
    still_on = 1

    check_stats(monster)
    print()
    while still_on == 1:
        
        hand={}
        while len(hand) < hand_size:
            i=random.sample(list(deck),1)[0]
            hand[i] = deck[i]
        
        still_on, monster, result = play_turn(monster, hand)

    if result == 1:
        print('You win')
        return 1
    elif result == 2:
        print('You dead')
        return 0
    elif result == 3:
        print('Its a draw')
        print('Boring...')
        return 0
    else:
        return 0






 
def pick_monster(monster_list):
    i=random.sample(list(monsters),1)[0]
    return copy.deepcopy(monsters[i])


def shop(cardpool):
    global me
    global deck
    print('==============================')
    print()
    print('Welcome')
    print()
    time.sleep(2)
    print('plz buy something')
    print()
    time.sleep(2)
    
    shop_cards = {}
    
    while len(shop_cards) < random.randrange(shop_items) + 1:
        card = random.sample(list(cardpool),1)[0]
        shop_cards[card] = cardpool[card]
    
    for card in shop_cards:
        print('Price ' + str(cardpool[card]['price']) + ' gold ----> ' + card + ': ' + cardpool[card]['dcr'])
        print()
    
    choice = ''
    
    while choice != 'leave':
        choice = input('Type buy *card* or leave: ')
        
        while choice[0] == '!':
            if show_info(choice, {'health' 'n/a'}, hand) == 1:
                return 0
            choice = input('Type buy *card* or leave: ')
        
        if choice == 'leave':
            print()
            print('Goodbye...')
        elif choice not in shop_cards:
            print()
            print('Card not in stock')
        else:
            print()
            if choice in deck:
                print('You already have this card...')
            elif cardpool[choice]['price'] > me['money']:
                print('You cant afford this card...')
            else:
                print('Enjoy...')
                me['money'] = me['money'] - cardpool[choice]['price']
                deck[choice] = cardpool[choice]
                

def loot(challange):
    global me
    haul = random.randrange(challange*5)
    me['money'] += haul
    print()
    print('You gain ' + str(haul) + ' gold')
    return me


                
def play_game():
    global me
    global deck
    alive = 1
    count = 0
    print('A monster aproaches you')
    print()
    print('Type !halp for help')
    print()
    current_monster = pick_monster(monsters)
    alive = fight(current_monster)
    if alive == 1:
        count += 1
        me = loot(current_monster['challange'])
    while alive == 1:    
        count += 1
        choice0 = random.randrange(2)
        choice1 = random.randrange(2)
        
        print()
        print('You see 2 paths ahead')
        print()
        print('Path 1: ' + choices[choice0] + ', path 2: ' + choices[choice1])
        print()
        
        choice = input('Choose a path... ')
        
        while choice[0] == '!':
            if show_info(choice, {'health' 'n/a'}, hand) == 1:
                return
            choice = input('Choose a path... ')
        
        while choice != '1' and choice != '2':
            print()
            print('Not a valid choice')
            print()
            choice = input('Choose a path... ')
        
        if choice == '1':
            if choice0 == 0:
                if shop(cardpool) == 0:
                    return
            else:
                print()
                print('A monster aproaches you')
                print()
                current_monster = pick_monster(monsters)
                alive = fight(current_monster)
                if alive == 1:
                    loot(current_monster['challange'])
        else:
            if choice1 == 0:
                if shop(cardpool) == 0:
                    return
            else:
                print()
                print('A monster aproaches you')
                print()
                current_monster = pick_monster(monsters)
                alive = fight(current_monster)
                if alive == 1:
                 loot(current_monster['challange'])
                
    print('You suvived ' + str(count) + ' rounds')
        
        
        
with open('monster.yaml') as ymlfile:
    monsters = yaml.load(ymlfile)
        
choices = ['go to a shop', 'fight a monster']
me, cardpool, deck = start_game()
hand_size = 3
hand={}
shop_items = 3


















