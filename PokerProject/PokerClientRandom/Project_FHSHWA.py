# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:24:16 2020

@author: FHassan
"""

import numpy as np
from operator import itemgetter, attrgetter
import random
import math
#import pandas as pd
#import bnlearn as bn
#import tabulate
save_all_data_in_file = True
wstuff = "Wierd_stuff.txt"
opp_data_memory = "Opponents_data.txt"
prediction_parameters_file = "prediction_parameters.txt"




Ranks = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

Suits = {
    'd': 1,
    'c': 2,
    'h': 3,
    's': 4
}



Types = {
    'HighCard':      1,
    'OnePair':       2,
    'TwoPairs':      3,
    '3OfAKind':      4,
    'Straight':      5,
    'Flush':         6,
    'FullHouse':     7,
    '4OfAKind':      8,
    'StraightFlush': 9
}
        

#·······························································································#
# ·······················Function got from lab 2 (designed by Yuntao Fan)·······················#
#·······························································································#
def identify_hand(Hand_):

    # Get the type of Hand
    def evaluateHand(Hand_):
        count = 0
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    count += 1
        return count

    # Use the "count" to analyse hand
    count_ = evaluateHand(Hand_)

    sub1 = 0
    score = [' ', ' ', ' ']

    if count_ == 12:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 3:
                score = ['4OfAKind', card1[0], card1[1]]
                break

    elif count_ == 8:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 1:
                sub1 = 0
            if sub1 == 2:
                score = ['FullHouse', card1[0], card1[1]]
                break

    elif count_ == 6:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 2:
                score = ['3OfAKind', card1[0], card1[1]]
                break

    elif count_ == 4:
        needCard1 = ['', '']
        needCard2 = ['', '']
        for card1 in Hand_:
            for card2 in Hand_:
                # card1 keep the first hand card, card1 use every card to compare the card1
                if card1[0] == card2[0] and card1[1] != card2[1]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard1 == ['', '']:
                            needCard1 = card1
                    else:
                        if needCard1 == ['', '']:
                            needCard1 = card2
                if card1[0] == card2[0] and card1[1] != card2[1] \
                        and card1[0] != needCard1[0] and card2[0] != needCard1[0]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard2 == ['', '']:
                            needCard2 = card1
                    else:
                        if needCard2 == ['', '']:
                            needCard2 = card2
        if Ranks[needCard1[0]] > Ranks[needCard2[0]]:
            score = ['TwoPairs', needCard1[0], needCard1[1]]
        else:
            score = ['TwoPairs', needCard2[0], needCard2[1]]

    elif count_ == 2:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] > card2[1]):
                    sub1 += 1
            if sub1 == 1:
                score = ['OnePair', card1[0], card1[1]]
                break

    elif count_ == 0:
        def sortHand(Hand_):
            hand_sorted_ = sorted([[card_, Ranks[card_[0]]] for card_ in Hand_], key=itemgetter(1))[:]
            return [card_[0] for card_ in hand_sorted_]

        Hand_ = sortHand(Hand_)
        score = ['HighCard', Hand_[4][0], Hand_[4][1]]

        if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
            score = ['Flush', Hand_[4][0], Hand_[4][1]]

        if (Ranks[Hand_[4][0]] - Ranks[Hand_[3][0]] == 1) \
                and (Ranks[Hand_[3][0]] - Ranks[Hand_[2][0]] == 1) \
                and (Ranks[Hand_[2][0]] - Ranks[Hand_[1][0]] == 1) \
                and (Ranks[Hand_[1][0]] - Ranks[Hand_[0][0]] == 1):
            score = ['Straight', Hand_[4][0], Hand_[4][1]]

            if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
                score = ['StraightFlush', Hand_[4][0], Hand_[4][1]]
    else:
        exit(5664)
    return score


def _sortHand(Hand_):
    hand_sorted_ = sorted([[card_, Ranks[card_[0]]] for card_ in Hand_], key=itemgetter(1))[:]
    return [card_[0] for card_ in hand_sorted_]


#·······························································································#


def _which_card_change(hand, stren):
    least = ""         
    if stren[0] == 'TwoPairs':
        hand_ = []
        for card in hand:
            if card[0] != stren[1]:
                hand_.append(card)
        if hand_[0][0] == hand_[1][0]:
            least = hand_[2]
        elif hand_[0][0] == hand_[2][0]:
            least = hand_[1]
        else:
            least = hand_[0]
    else:
        hand_ = []
        for card in hand:
            if card[0] != stren[1]:
                hand_.append(card)
                if least != "" and Ranks[card[0]] < Ranks[least[0]]:
                    least = card
                elif least != "" and Ranks[card[0]] == Ranks[least[0]]:
                    if Suits[card[1]] < Suits[least[1]]:
                        least = card
                elif least == "":
                    least = card
    if stren[0] == "3OfAKind" or stren[0] == "OnePair" or stren[0] == "HighCard":
        return (hand_)
    return least


def wanna_change(hand):
    hand = _sortHand(hand)
    strength = identify_hand(hand)
    stren = strength[0]
    if stren == "4OfAKind" or stren == "TwoPairs":
        return (True, [_which_card_change(hand, strength)])
    elif stren == "3OfAKind":
        l = _which_card_change(hand, strength)
        n = random.randint(1, len(l))
        return (True, l[0:])
    elif stren == "OnePair" or stren == "HighCard":
        c = 0
        hand_ = []
        for h_ in range(len(hand)):
            if h_ < len(hand)-2:
                if Ranks[hand[h_][0]] +1 == Ranks[hand[h_+1][0]]:
                    c += 1
                    if not hand[h_] in hand_: hand_.append(hand[h_])
                    if not hand[h_+1] in hand_: 
                        hand_.append(hand[h_+1])
                elif c > 1:
                    break
                else:
                    c = 0
                    hand_ = []
        if c > 2:
            l = []
            for h in hand:
                if not h in hand_:
                    l.append(h)
            return (True, l)
        elif c ==2 and stren == "HighCard":
            l = []
            for h in hand:
                if not h in hand_ and h != strength[1]+strength[2] and stren == "HighCard":
                    l.append(h)
#                elif not h in hand_ and h[0] != strength[1] and stren == "OnePair":
#                    l.append(h)
            if len(l) != 0: return (True, l)
            else:
                l = _which_card_change(hand, strength)
                #n = random.randint(1, len(l))
                return (True, l[0:])
        else:
            l = _which_card_change(hand, strength)
            #n = random.randint(1, len(l))
            return (True, l[0:])
    else:
    #if stren == "StraightFlush" or stren == "FullHouse" or stren == "Flush" or stren == "Straight":
        return (False, " ")


def hand_score(_hand):
    type_h = identify_hand(_hand)
    return Types[type_h[0]]*13 + Ranks[type_h[1]]

def bet_decesion(_hand, phase):
    score = hand_score(_hand)
    if phase == 'First-bet':        
        if score < 15: return 'check'
        else: return 'open'
    else:
        if score < 18: return 'fold'
        elif score < 35: return 'call' 
        #elif score > 115: return 'all-in'        # if our hand is bigger than 4OfKind of J
        else: return 'raise'
     
# def reflex_bet(hand, amount, min_bet, max_bet=50):
#     strength = hand_score(hand)
#     if amount <= 50:
#         return min_bet
#     else:
#         mpb = max_bet
#         alpha = 0
#         if strength <= 24:
#             alpha = mpb*0.1
#         elif strength > 24 and strength <= 43:
#             alpha =  mpb*0.15
#         elif strength > 43 and strength <= 72:
#             alpha = mpb*0.2
#         elif strength > 72 and strength <= 101:
#             alpha = mpb*0.25
#         elif strength > 120:
#             alpha = mpb*0.5
#         else:
#             alpha = mpb*0.3
#         alpha = int(alpha) 
#         if alpha < min_bet: return min_bet
#         elif alpha >= max_bet: return max_bet-1
#         else: return alpha        
     
        
     
def reflex_bet(hand, amount, min_bet, max_bet=50):
    strength = hand_score(hand)
    if amount <= 50:
        return min_bet
    else:
        value = 0
        mpb = max_bet
        if strength <= 24:
            value = mpb*(random.randint(8,14))/100
        elif strength > 24 and strength <= 43:
            value = mpb*(random.randint(15, 19))/100
        elif strength > 43 and strength <= 72:
            value = mpb*(random.randint(20, 24))/100
        elif strength > 72 and strength <= 101:
            value = mpb*(random.randint(25, 29))/100
        elif strength > 120:
            value = mpb*(random.randint(46, 50))/100
        else:
            value = mpb*(random.randint(30, 34))/100
        value = int(value)
        if value < min_bet: return min_bet
        elif value > max_bet: return max_bet
        else: return value
        
        

#········································Memo Agent········································#

#NORMAL DISTRIBUTION FUNCTION
def mean(values):
    j=0
    for i in values:
        j+=float(i)
    return j/len(values)

def stand_dev(values,mean):
    mm=0
    for i in values:
        mm+=((float(i)-mean)**2)
    return math.sqrt(mm/(len(values)-1))
    
def dist_f(x,values):
    mean_val=mean(values)
    dev = (stand_dev(values,mean_val))
    print('Mean_Value', mean_val)
    print('standard', dev)
    return (1/(dev*math.sqrt(2*math.pi)))*math.exp(-(((x-mean_val)**2)/(2*(dev**2))))


def ReadData(file, _n_lines = 200):
    playerinfo=[]
    f= open(file,"r")
    data = f.read().split('\n')
    c = 0
    for line in data[1:-1]:
        if len(line.split(';')) == 3:
            ele=line.split(";")
            x = []
            for j in range(len(ele)):
                if j == 0:
                    x.append(ele[j])
                elif j == 1:
                    x.append(int(ele[j].split('/')[0]))
                    x.append(int(ele[j].split('/')[1]))
                else:
                    x.append(int(ele[j]))
            playerinfo.append(x)
            c += 1
            if c > _n_lines: break
    f.close
    return playerinfo  

def sort_data(playerinfo,myscore,amountofplayers):#delimiter =";"
    players=createplayers(amountofplayers)
    for i in range(len(playerinfo)):
        info=playerinfo[i]
        players[playerinfo[i]+(i%len(players))]=info
    
    return players

def createplayers(amountofplayers):
    players=dict()
    for i in range(amountofplayers):
        #Playerinfo=list of lists for each player and their result
        players[i]=[[],[]]
    return players
             
# def predict(player,opp_bet,myscore):
#     higher=[]
#     lower=[]
#     hi = 0
#     lo = 0
    
#     for i in player:
#         s= int(i[2])
#         if s<=myscore:
#             lower.append(float(i[1]))
#         else:
#             higher.append(float(i[1]))
#     print("In predict", opp_bet)
#     if len(lower) < 2:
#         print('In-predict-lower')
#     if len(higher) < 2: 
#         return ('VMdS')   #not so lucky with the hands (Vaya suerte)    
#         print('In-predict-higher')
#         return ('TBR') # having a good luck (Teniendo buena racha)
    
#     print('In predict-second')
#     #print(lower,'\n\n')
#     #print(higher)
#     #print(len(higher),len(lower))
    
#     print("Opp_bet", opp_bet)
    
#     hi=dist_f(opp_bet,higher)
#     lo=dist_f(opp_bet,lower)
    
#     print("Opponents category (high, low): (", hi, ",", lo, ")")
    
#     if hi>lo: return ('eOVC')    #The oppoenet probably has a good cards (El oponente va cargado)
#     else: return ('VCC')        #Your card is probably higher than the oppoents (Ve con cuidado)
    
def predict(data, opp_bet_total, myscore):
    error = 0.10
    er_score = 0.5
    opp_bet = int(opp_bet_total.split('/')[0])/(int(opp_bet_total.split('/')[1])+0.01)
    opp_bet_min = opp_bet*(1-error)
    opp_bet_max = opp_bet*(1+error)
    
    bet = []
    hand = dict()
    for i in data:
        s= i[1]/(i[2]+0.01)
        if s <= opp_bet_max and s >= opp_bet_min:
            bet.append(s)
            hand[s] = int(i[3]) 
        
    if len(bet) > 0:
        bet_np = np.asarray(bet)
        mv = np.mean(bet_np)
        idx = (np.abs(bet_np - mv)).argmin()
        opp_hand = hand[bet_np[idx]]
    else:
        data_np = np.matrix(data)
        data_np = np.matrix(data_np[:,1:])
        data_np = data_np.astype(int)
        ind_1 = (np.abs(np.divide(data_np[:,0],data_np[:,1]) - opp_bet)).argmin()
        opp_hand = data_np[ind_1, 3]

    if myscore > opp_hand*(1+er_score):
        return ('TBR') # having a good luck (Teniendo buena racha)
    elif opp_hand > myscore:
        return ('eOVC')       #The oppoenet probably has a good cards (El oponente va cargado)
    else:
        return ('VCC')        #Your card is probably higher than the oppoents (Ve con cuidado)


class ex_moving_average(object):
    def __init__(self):
        self.n_previous = 12
        self.n_alphas = int(self.n_previous//3)
        self.alphas = dict()
        self.previous = dict()
        self.choose = dict()
        self.bool_choose = False
        self._dict_names = ['alphas', 'previous', 'chooses']
        self.chosen = ''
        f = open(prediction_parameters_file, 'r')
        data = f.read().split('\n')
        f.close()
        if len(data) > 1:
            d = [self.alphas, self.previous, self.choose]
            for _line in data:
                d1 = _line.split("---")
                d[self._dict_names.index(d1[0])] = eval(d1[1])
    def _limits(self, k, _type):
        if _type == 'alpha':
            if len(self.alphas[k]) > self.n_alphas: self.alphas[k] = self.alphas[k][-self.n_alphas:]
        else:
            if len(self.previous[k]) > self.n_previous: self.previous[k] = self.previous[k][-self.n_previous:]
    def update(self, x, name, bet):
        if not bet in self.previous: return
        print("Alpha updating...")
        ## x = x_0*alpha + (1-alpha)*x_1 + (1-alpha)^2*x_2 + ...
        ## 0 = ... + beta^2*x_2 + beta*(x_1 - x_0) + (x_0 - x); beta = 1 - alpha
        l = self.previous[bet]
        if len(l) < 2:  return
        if not name in self.alphas: self.alphas[name] = [0.5]
        if (len(self.alphas[name]) >= len(l)): return
        
        print("Previous means: ", l)
        
        s1 = 0
        s2 = 0
        l1 = []
        alpha = self.alphas[name]
        for i in range(len(self.previous[bet])):
            a = i//self.n_alphas + 1
            if a >= len(alpha) -1:
                l1 += [self.previous[bet][i]]
            else:
                a_n = (1-alpha[a])**(len(self.previous[bet])-i-1)
                s1 += a_n*self.previous[bet][i]
                s2 += a_n
        if not len(l1) > 1: return
        s = s1 - s2*x
        l1[-1] += s
        coeff = np.asarray(l1)-x
        roots = np.roots(coeff)
        beta = math.inf
        for root_ in roots:
            if not np.iscomplex(root_):
                root_ = float(root_)
                if root_ >= 0 and root_ < beta:
                    beta = root_
        print("Roots: ", roots)
        if beta != math.inf:
            self.alphas[name] += [1-beta]
            self._limits(name, 'alpha')
            if 'ALL' in self.alphas:
                a = self.alphas['ALL'][-1]
                self.alphas['ALL'] += [(a+(1-beta))/2]
            else:
                self.alphas['ALL'] = [1-beta]
            self._limits('ALL', 'alpha')
    def get_x(self, x1, name, bet):
        print("Calculating the ex-moving-mean... ")
        if not name in self.alphas: self.alphas[name] = [0.5]
        if not bet in self.previous:
            self.previous[bet] = [x1]
            return x1
        num = x1
        den = 1
        alpha = self.alphas[name]
        for i in range(len(self.previous[bet])):
            a = i//self.n_alphas
            if a > len(alpha)-1: a = -1
            a_n = (1-alpha[a])**(len(self.previous[bet])-i-1)
            num += a_n*self.previous[bet][i]
            den += a_n 
        self.previous[bet] += [num/den]
        self._limits(bet, 'pre')
        return int(num/den)
    def what_to_do(self, name, bet, myscore):
        print("What are the chances??? :|")
        self.bool_choose = True
        k = str(name)+'-'+str(round(bet, 3))+'-'+str(myscore)
        self.chosen = k
        if not k in self.choose:
            self.choose[k] = 0.6
        return self.choose[k]
    def update_what_to_do(self, had_won):
        print("Updating the chances...")
        if self.bool_choose:
            a = self.choose[self.chosen]
            if had_won: self.choose[self.chosen] = a*1.01
            else: self.choose[self.chosen] = a*0.95
            #self.bool_choose = False
    def save_parameters(self):
        d = ["", "", ""]
        d[0] = self._dict_names[0] + "---" + str(self.alphas.copy()) + "\n"
        d[1] = self._dict_names[1] + "---" + str(self.previous.copy()) + "\n"
        d[2] = self._dict_names[2] + "---" + str(self.choose.copy())
        f = open(prediction_parameters_file, 'w')
        f.writelines(d)
        f.close()
    
EM_average = ex_moving_average()



def predict1(data, opp_bet_total, myscore, opp_name = 'ALL', n_elements = 30):
    print("Let's get to work... ")
    error = 0.10
    opp_bet = int(opp_bet_total.split('/')[0])/(int(opp_bet_total.split('/')[1])+0.1)
    opp_bet_min = opp_bet*(1-error)
    opp_bet_max = opp_bet*(1+error)
    
    data.reverse()
    bet_esp = []
    hand_esp = dict()
    bet_all = []
    hand_all = dict()
    c = 0.0
    for _line in data:
        s= _line[1]/(_line[2]+0.1)
        if s <= opp_bet_max and s >= opp_bet_min:
            bet_all.append(s)
            hand_all[s]=_line[3]
            if opp_name == 'ALL': c += 1/2
            if opp_name != 'ALL' and opp_name == _line[0]:
                bet_esp.append(s)
                hand_esp[s]= _line[3]
                c += 1
        if c >= n_elements: break
    
    if len(hand_all) < 1:
        print("Oh oh!!! No data found ")
        return "No bet registerd", opp_bet
    if opp_name != 'ALL' and len(hand_esp) > 1:
        bet = np.asarray(bet_esp)
        hand = hand_esp.copy()
    else:
        bet = np.asarray(bet_all)
        hand = hand_all.copy()
    
    mv = np.mean(bet)
    idx = (np.abs(bet - mv)).argmin()
    x_av = hand[bet[idx]]
    opp_av_hand = EM_average.get_x(x_av, opp_name, round(opp_bet, 2))
    
    wstuff_record("Opponents predicted hand: " + str(opp_av_hand))
    wstuff_record("My hand: " + str(myscore))
    print("Opponents predicted hand: ", opp_av_hand)
    print("My hand: ", myscore)
    
    if myscore > opp_av_hand*1.5:
        return 'TBR', opp_bet # having a good luck (Teniendo buena racha)
    elif myscore*1.5 < opp_av_hand:
        return 'VMDS', opp_bet       #The opponents hand is much bigger than ours (Vaya mierda de suerte)
    elif opp_av_hand > myscore:
        return 'eOVC', opp_bet       #The oppoenet probably has a good cards (El oponente va cargado)
    else:
        return 'VCC', opp_bet        #Your card is probably higher than the oppoents (Ve con cuidado)
    
    
    
def mem_agent(_hand, opponents_bet_name, amount, min_bet, max_bet=100):
    print("What to do??? What to do??? ")
    score = hand_score(_hand)
    history = ReadData(opp_data_memory)
    if len(opponents_bet_name.split("--")) > 1:
        ans = []
        for k in opponents_bet_name.split("--"):
            opponents_bet, name = k.split(';')
            x = predict1(history, opponents_bet, score, name)
            ans += x[0]
            _bet = x[1]
        if not 'eOVC' in ans:
            if 'TBR' in ans:
                answer = 'TBR'
            else:
                answer = 'VCC'
        else:
            answer = 'eOVC'
    else:
        opponents_bet, name = opponents_bet_name.split(';')
        answer, _bet = predict1(history, opponents_bet, score, name)
        
    print(answer, " I choose youuu!!!!")
    
    if answer == 'TBR':
        if (amount*0.3) > min_bet:
            return int(amount*0.3)
        else:
            return amount
    elif answer == 'VMdS':
        return -1
    elif answer == 'VCC':
        return reflex_bet(_hand, amount, min_bet, max_bet*1.2)
    else:
        per = EM_average.what_to_do(name, _bet, score)
        if round(per, 2) != 0:
            val = reflex_bet(_hand, amount, min_bet, max_bet*per)
            if val != min_bet:
                return val
        return 0 #reflex_bet(_hand, amount, min_bet, max_bet*0.7)

def wstuff_record(t):
    if save_all_data_in_file:
        al = open(wstuff, 'a')
        line = "\n" + t
        al.write(line)
        al.close()
    return

def _delete_memories(wh = 'ALL'):
    _names = [opp_data_memory, wstuff, prediction_parameters_file]
    if wh != 1 and wh != 2:
        f= open(opp_data_memory,"r")
        data = f.readlines()
        if len(data) > 201:
            data = [data[0]] + data[-200:]
    if wh == 'ALL':
        for _name in _names[:2]:
            open(_name, "w").close()
    elif wh == 'ALL+':
        for _name in _names:
            open(_name, "w").close()
    elif isinstance(wh, int):
        open(_names[wh]).close()
    if wh != 1 and wh != 2:
        f = open(opp_data_memory, "a")
        f.writelines(data)
        f.close()


    
        


