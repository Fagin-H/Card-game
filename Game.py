# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:24:32 2018

@author: fhales
"""

import yaml
import time
import random
import copy
import numpy as np



def play_turn(monster, hand):    
    
    print()
    print('Cards in hand:')
    print()
    
    for card in hand:
        print(card+': '+hand[card]['dcr'])
        print()
      
    crd, end = pick_card(hand, monster)
    
    if end == 1:
        return 0, monster, 0
    
    if crd != 'pass':
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
    print()
    if crd == '!halp':
        print('List of commands:')
        print('!show deck       --> shows cards in deck')
        print('!show hand       --> shows cards in hand')
        print('!show gold       --> shows current gold')
        print('!show health     --> shows current health')
        print('!show poison     --> shows current poison')
        print('!show monster    --> shows current monsters health')
        print('!save *filename* --> saves game')
        print('!end             --> quit game')
        print('pass             --> skips your turn')
        print()
    
    elif crd == '!show deck':
        for card in deck:
            print(card+': '+deck[card]['dcr'])
            print()
    elif crd == '!show hand':
        if hand == {}:
            print('You are not in combat')
            print()
        else:
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
    elif crd == '!show poison':
        print('Your poison is '+str(me['poison']))
        print()
    elif crd == '!show monster':
        if monster == {}:
            print('You are not in combat')
            print()
        else:
            print('Monsters health is '+str(monster['health']))
            print()
    elif len(crd) > 7:
        if crd[:6] == '!save ':
            if monster == {}:
                save_game((crd+ ' ')[6:-1], count)
                print('Game saved')
                print()
            else:
                print('Cant save in combat')
                print()
        else:
            print('Not a command')
            print()
    else:
        print('Not a command')
        print()
    return 0


def monster_turn(monster):
    if monster['health']<1:
        return monster
    else:
        mcard=monster_card(monster)
        
        poison_damage = me['poison']
        
        me['health'] -= poison_damage
          
        if poison_damage != 0:
            print('You take '+str(poison_damage)+' poison damage!')
            if me['health'] < 1:
                return monster
        
        if monster['health'] + mcard['heal'] > monster['maxhp']:
            heal = monster['maxhp'] - monster['health']
            monster['health'] = monster['maxhp']
        else:
            monster['health'] += mcard['heal']
            heal = mcard['heal']
                
        monster['health']+=-mcard['harm']
        
        monster['shield'] = mcard['shield']
        
        damages=mcard['attack']
        if damages > me['shield']:
            damages =me['shield']
        
        damagep=mcard['attack']-me['shield']
        if damagep < 0:
            damagep = 0
            
        me['health']+=-damagep
          
        poison_damage = monster['poison']
        
        monster['health'] -= poison_damage
               
        me['poison'] += mcard['poison']

        
        if mcard['attack'] != 0:
            print('Monster hits for '+str(mcard['attack'])+' damage!')
        
        if damages != 0:
            print('You block '+str(damages)+' damage')
        
        if mcard['poison'] != 0:
            print('You take  '+str(mcard['poison'])+' poison!')
            
        if mcard['heal'] != 0:
            print('Monster heals '+str(heal)+' health')
            
        if mcard['shield'] != 0:
            print('Monster gains '+str(mcard['shield'])+' shield')
            
        if mcard['harm'] != 0:
            print('Monster loses '+str(mcard['harm'])+' health')
            
        if poison_damage != 0:
            print('Monster takes '+str(poison_damage)+' poison damage!')
            
        print()
        return monster


def monster_card(monster):
    card_choices = list(monster['attacks'])
    probs = []
    for card_choice in card_choices:
        probs.append(monster['attacks'][card_choice]['freq'])
    probs = np.array(probs)
    probs = probs/(np.sum(probs))
        
    i=np.random.choice(card_choices, 1, p=probs)[0]
    return monster['attacks'][i]
    


def check_stats(monster):
    if me['health'] < 1 and monster['health'] > 0:
        return 2
    elif monster['health'] < 1 and me['health'] > 1:
        return 1
    elif monster['health'] < 1 and me['health'] < 1:
        return 3
    
    print('Your health is '+str(me['health']))
    print('Your poison is '+str(me['poison']))
    print('Monsters health is '+str(monster['health']))
    print('Monsters poison is '+str(monster['poison']))
    print('Your gold is '+str(me['money']))
    return 0


def play_card(crd, monster, hand):
    me['money'] -= hand[crd]['cost']
    
    h_gained = gain_health(hand[crd]['heal'])
        
    me['health'] -= hand[crd]['harm']
    
    me['shield'] = hand[crd]['shield']
    
    damages=hand[crd]['attack']
    if damages > monster['shield']:
        damages =monster['shield']
    
    damagep=hand[crd]['attack']-monster['shield']
    if damagep < 0:
        damagep = 0
        
    monster['health'] -= damagep
           
    monster['poison'] += hand[crd]['poison']
    
    if hand[crd]['attack'] != 0:
        print('You hit for '+str(hand[crd]['attack'])+' damage!')
        
    if damages != 0:
        print('Monster blocks '+str(damages)+' damage')
        
    if hand[crd]['poison'] != 0:
        print('Monster gets '+str(hand[crd]['poison'])+' poison!')
        
    if hand[crd]['heal'] != 0:
        print('You heal '+str(h_gained)+' health')
        
    if hand[crd]['harm'] != 0:
        print('You lose '+str(hand[crd]['harm'])+' health')
        
    if hand[crd]['shield'] != 0:
        print('You gain '+str(hand[crd]['shield'])+' shield')
        
    if hand[crd]['cost'] < 0:
        print('You find '+str(-hand[crd]['cost'])+' gold')
    print()
    return monster



def pick_card(hand, monster):
    crdpicked = 0
    
    while crdpicked == 0:
        pcard, end = get_input('Play a card: ', monster, hand)
        if end == 1:
            return '', 1
                
        for card in hand:
            if pcard == card or pcard == 'pass':
                crdpicked = 1
                if pcard == 'pass':
                    return pcard, 0
                if me['money'] < hand[pcard]['cost']:
                    print('Not enough money')
                    crdpicked = 0
                
        if crdpicked == 0:
            print('Card not in hand...')
            
    return pcard, 0


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
    still_on = 1
    
    print()
    print('A ' + monster['name'] + ' aproaches you')
    print()

    check_stats(monster)
    print()
    while still_on == 1:
        
        hand={}
        while len(hand) < hand_size:
            i=random.sample(list(deck),1)[0]
            hand[i] = deck[i]
        
        still_on, monster, result = play_turn(monster, hand)
    me['poison'] = 0

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
    print('==============================')
    print()
    print('Welcome')
    print()
    time.sleep(2)
    print('plz buy something')
    print()
    time.sleep(2)
    print('You have '+str(me['money'])+' gold')
    print()
    
    shop_cards = {}
    
    while len(shop_cards) < random.randrange(shop_items) + 1:
        card = random.sample(list(cardpool),1)[0]
        shop_cards[card] = cardpool[card]
    
    for card in shop_cards:
        print('Price ' + str(cardpool[card]['price']) + ' gold ----> ' + card + ': ' + cardpool[card]['dcr'])
        print()
    print()
    print('Services:')
    print()
    print('Price 10 gold ----> heal 10 health')
    choice = ''
    
    while choice != 'leave':
        choice, ext = get_input('Type *card*, heal, or leave: ', {}, {})
        
        if ext == 1:
            return 0
        
        if choice == 'leave':
            print()
            print('Goodbye...')
        elif choice == 'heal':
            print()
            if me['money'] < 10:
                print('You cant afford this...')
            else:
                h_gained = gain_health(10)
                me['money'] -= 10
                print('You gain ' + str(h_gained) + ' health')
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
    return 1

def gain_health(ammount):
    h_gain = int(ammount)
    if h_gain + me['health'] > me['maxhp']:
        h_gain = me['maxhp'] - me['health']
    me['health'] += h_gain  
    return h_gain


def loot(challange, count):
    haul = random.randrange(challange*5)
    me['money'] += haul
    count += 1
    print()
    print('You gain ' + str(haul) + ' gold')
    return count

def get_input(text, monster, hand):
    print()
    att_input = input(text)
    while att_input == '':
        print()
        att_input = input(text)
    if att_input[0] == '!':
        end = show_info(att_input, monster, hand)
        if end == 1:
            return att_input, 1
        att_input, misc = get_input(text, monster, hand)
        if misc == 1:
            return att_input, 1
    return att_input, 0
        

def rest():
    h_gain = gain_health(me['maxhp']/3)
    print()
    print('You rest at an makeshift campsite')
    print()
    print('You gain ' + str(h_gain) + ' health')
    print()
    time.sleep(2)



                
def play_game(me1 = '', deck1 = '', count1 = ''):
    me, cardpool, deck = start_game()
    alive = 1
    global count
    
    if me1 != '':
        me = me1
        deck = deck1
        count = count1
    else:
        count = 0
        print()
        print('Type !halp for help')
        print()
        current_monster = pick_monster(monsters)
        alive = fight(current_monster)
        if alive == 1:
            count = loot(current_monster['challange'], count)
    while alive == 1:    
        choice1, choice2 = np.random.choice(range(len(choices)), 2, p=prob_dist, replace = False)
        
        print()
        print('You see 2 paths ahead')
        print()
        print('Path 1: ' + choices[choice1] + ', path 2: ' + choices[choice2])
        print()
        
        choice, ext = get_input('Choose a path... ', {}, {})
        if ext == 1:
            return
        
        while choice != '1' and choice != '2':
            print()
            print('Not a valid choice')
            print()
            choice, ext = get_input('Choose a path... ', {}, {})
            if ext == 1:
                return
                    
        if choice == '1':
            choice = choice1
        elif choice == '2':
            choice = choice2
            
        
        if choice == 0:
            alive = shop(cardpool)
        elif choice == 1:
            current_monster = pick_monster(monsters)
            alive = fight(current_monster)
            if alive == 1:
                count = loot(current_monster['challange'], count)
        elif choice == 2:
            rest()
                
    print('You suvived ' + str(count) + ' battles')
    with open('highscore.yml', 'r+') as outfile:
        high_score = yaml.load(outfile)
    f = open('highscore.yml', 'w').close()
    with open('highscore.yml', 'r+') as outfile:
        if high_score < count:
            print()
            print('New high score!')
            yaml.dump(count, outfile, default_flow_style=False)
        else:
            print()
            print('High score: ' + str(high_score))
            yaml.dump(high_score, outfile, default_flow_style=False)
        

def save_game(save_name, score):
    
    save_data={'player': me, 'deck': deck, 'score': score}
    f = open('savegame/' + save_name + '.yml', 'w').close()
    with open('savegame/' + save_name + '.yml', 'w') as outfile:
        yaml.dump(save_data, outfile, default_flow_style=False)

def load_game(save_name):
    me, cardpool, deck = start_game()
    with open('savegame/' + save_name + '.yml') as outfile:
        save_data = yaml.load(outfile)
    deck = save_data['deck']
    me['health'] = save_data['player']['health']
    me['money'] = save_data['player']['money']
    score = save_data['score']
    play_game(me, deck, score)
       
        
with open('monster.yaml') as ymlfile:
    monsters = yaml.load(ymlfile)
        
choices = ['go to a shop', 'fight a monster', 'take a rest']
prob_dist = [0.3, 0.5, 0.2]

me, cardpool, deck = start_game()
hand_size = 3
hand={}
shop_items = 3



















