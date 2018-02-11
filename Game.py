# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:24:32 2018

@author: fhales
"""

import yaml
import time
import random


def play_turn():
    
    me['shield']=0
    
    crd=pick_card()
    
    while crd[0] == '!':
        if show_info(crd) == 1:
            return 1
        crd=pick_card()
    
    if crd != 'pass':
        crd=check_price(crd)
        play_card(crd)
        time.sleep(2)
    if monster_turn() == 1:
        time.sleep(2)
        return 1
    time.sleep(2)
    return check_stats()


def show_info(crd):
    if crd == '!halp':
        print()
        print('List of commands:')
        print('!show deck    --> shows cards in deck')
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
    elif crd == '!end':
        return 1
    elif crd == '!show gold':
        print('You have '+str(me['money'])+' gold')
        print()
    elif crd == '!show health':
        print('Your health is '+str(me['health']))
        print()
    elif crd == '!show monster':
        print('Monsters health is '+str(monster1['health']))
        print()
    else:
        print('Not a command')
        print()
    return 0


def monster_turn():
    if monster1['health']<1:
        print('You win')
        return 1
    else:
        mcard=monster_card()
        
        if monster1['health'] + mcard['heal'] > monster1['maxhp']:
            heal = monster1['maxhp'] - monster1['health']
            monster1['health'] = monster1['maxhp']
        else:
            monster1['health'] += mcard['heal']
            heal = mcard['heal']
                
        monster1['health']+=-mcard['harm']
        
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
            
        if mcard['harm'] != 0:
            print('Monster loses '+str(mcard['harm'])+' health')
            
        print()
        
        if monster1['health']<1 and me['health']>1:
            print('You win')
            return 1
        elif monster1['health']<1 and me['health']<1:
            print('Its a draw')
            print('Boring...')
            return 1            
        return 0


def monster_card():
    i=random.sample(list(monster1['attacks']),1)[0]
    return monster1['attacks'][i]
    


def check_stats():
    if me['health']<1:
        print('You dead')
        return 1
    print('Your health is '+str(me['health']))
    print('Monsters health is '+str(monster1['health']))
    print('Your gold is '+str(me['money']))
    return 0


def play_card(crd):
    me['money']+=-deck[crd]['cost']
    
    if me['health'] + deck[crd]['heal'] > me['maxhp']:
        heal = me['maxhp'] - me['health']        
        me['health'] = me['maxhp']
    else:
        me['health'] += deck[crd]['heal']
        heal = deck[crd]['heal']
        
    me['health'] += -deck[crd]['harm']
    
    me['shield'] += deck[crd]['shield']
    
    monster1['health']+=-deck[crd]['attack']
    
    if deck[crd]['attack'] != 0:
        print('You hit for '+str(deck[crd]['attack'])+' damage!')
        
    if deck[crd]['heal'] != 0:
        print('You heal '+str(heal)+' health')
        
    if deck[crd]['harm'] != 0:
        print('You lose '+str(deck[crd]['harm'])+' health')
        
    if deck[crd]['shield'] != 0:
        print('You gain '+str(deck[crd]['shield'])+' shield')
        
    if deck[crd]['cost'] < 0:
        print('You find '+str(-deck[crd]['cost'])+' gold')
    print()


def check_price(crd):
    while me['money']<deck[crd]['cost']:
        print('Not enough money')
        crd=pick_card()
    return crd


def pick_card():
    crdpicked = 0
    
    while crdpicked == 0:
        pcard=input('Play a card: ')
        
        if pcard[0] == '!':
            return pcard
        
        for card in deck:
            if pcard == card or pcard == 'pass':
                crdpicked = 1
                
        if crdpicked == 0:
            print('Card not in deck...')
            
    return pcard


def start_game():
    with open('monster.yaml') as ymlfile:
        monsters = yaml.load(ymlfile)
        
    monster1=monsters['bad_guy']
    
    with open('card.yaml') as ymlfile:
        cards = yaml.load(ymlfile)
    deck=cards
    
    with open('player.yaml') as ymlfile:
        player = yaml.load(ymlfile)
        
    me=player['me']
    
    return me, deck, monster1



me, deck, monster1 = start_game()


print('A monster aproaches you')
print()
print('Type !halp for help')

dead=0
while dead == 0:
    dead=play_turn()


























