import socket
import random
import ClientBase
import Project_FHSHWA as pj


# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
#------------------------------------------------------------------
#-------------------------Inner Parameters-------------------------
#------------------------------------------------------------------

# Agent
#agent_type =  ['reflex', 'mem']
which_agent = ['reflex', 'mem'][1]
POKER_CLIENT_NAME = 'FHSHWA01'+which_agent
CURRENT_HAND = []
recent_bet = 0
current_ante = 0
save_all_data_in_file = True
wstuff = "Wierd_stuff.txt"

#------------------------------------------------------------------

#Opponents['Name']['round'] = ['Bet', 'hand_strength']
class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0
        
class _save_opponents_data(object):
    def __init__(self):
        self.rounds_data = dict()
        self.players_data = dict()
        self.players_chips = dict()
        self.players_bet = dict()
    def update_chips(self, player, chip):
        self.players_chips[player] = chip
    def update_bet(self, player, bet):
        self.players_bet[player] = bet
    def opponents_have_bet(self):
        return len(self.players_bet) != 0
    def get_opponents_bet(self, typ = 'max'):
        # typ = 'all', 'max' & 'first'
        print("Getting oppponent to analise...")
        if self.opponents_have_bet():
            alpha = 0
            opp = ''
            hole = ''
            for op in self.players_bet:
                if typ != 'all':
                    if alpha < self.players_bet[op]: 
                        alpha = self.players_bet[op]
                        opp = op
                    if typ == 'first': break
                else:
                    hole += str(self.players_bet[op])+'/'+str(self.players_chips[op])+';'+opp+"--"
            if typ != 'all': return str(alpha)+"/"+str(self.players_chips[opp])+';'+opp
            if hole[-2:] == "--": hole = hole[:-2]
            return hole
        else:
            return -1
    def add_hand(self, player, hand):
        if player in self.players_data:
            n = max(self.players_data[player])
        else:
            self.players_data[player] = [0]
            n = 0
        self.rounds_data[player+str(n)+'hand'] = hand
        if (player+str(n)+'bet') in self.rounds_data: 
            self.set_line_(player, n)
    def add_bet(self, player, bet):
        if player in self.players_data:
            n = max(self.players_data[player])+1
            self.players_data[player].append(n)
        else:
            self.players_data[player] = [0]
            n = 0
        if self.players_chips[player] > 0:
            self.rounds_data[player+str(n)+'bet'] = str(bet)+"/"+str(self.players_chips[player])#round(bet/self.players_chips[player], 8)
    def set_line_(self, player, n):
        _hand = self.rounds_data[player+str(n)+'hand']
        _bet = self.rounds_data[player+str(n)+'bet']
        _opp_bet = int(_bet.split('/')[0])/int(_bet.split('/')[1])
        if which_agent == 'mem': pj.EM_average.update(int(_hand), player, round(_opp_bet, 2))
        file = open('Opponents_data.txt', 'a')
        line = (player + ';' +
                str(_bet) + ';' +
                str(_hand) +
                '\n')
        print(_bet)
        file.writelines(line)
        file.close()
    def restart(self):
        self.rounds_data = dict()
        self.players_data = dict()
                
_sd = _save_opponents_data()

'''
* Gets the name of the player.
* @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
'''
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the anser must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips alrady put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")

    # Random Open Action
    def chooseOpenOrCheck():
        if (_playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen 
            and pj.bet_decesion(CURRENT_HAND, 'First-bet') == 'open'):
            #return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
            #•pj.reflex_bet(CURRENT_HAND, _playersRemainingChips, _minimumPotAfterOpen)
            return ClientBase.BettingAnswer.ACTION_OPEN,  (pj.reflex_bet(CURRENT_HAND, _playersRemainingChips, _minimumPotAfterOpen)) if _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else _minimumPotAfterOpen
        else:
            return ClientBase.BettingAnswer.ACTION_CHECK
    return chooseOpenOrCheck()
    # return {
    #     0: ClientBase.BettingAnswer.ACTION_CHECK,
    #     1: ClientBase.BettingAnswer.ACTION_CHECK,
    # }.get(random.randint(0, 2), chooseOpenOrCheck())

'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''


def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    
    #global which_agent
    print("Player requested to choose a call/raise action.")
    # Random Open Action
    print(CURRENT_HAND)
    #def chooseRaiseOrFold_reflex_agent():
    if which_agent == 'reflex':
        if ( _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo):
            print('Yipika yai')
            what = pj.bet_decesion(CURRENT_HAND, 'Second-bet')
            if what == 'raise':
                bet = pj.reflex_bet(CURRENT_HAND, _playersRemainingChips, _minimumAmountToRaiseTo, _maximumBet)
                if bet > _playersRemainingChips*0.5 and pj.hand_score(CURRENT_HAND) < 90: return ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
                return ClientBase.BettingAnswer.ACTION_RAISE, bet  if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
            elif what == 'call':
                return ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
            #elif what == 'all-in':
            #    return ClientBase.BettingAnswer.ACTION_ALLIN,  _playersRemainingChips if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
            else:
                return ClientBase.BettingAnswer.ACTION_FOLD
        else:
            
            return ClientBase.BettingAnswer.ACTION_FOLD
    #def chooseRaiseOrFold_mem_agent():
    elif which_agent == 'mem': #Mem agent
        if ( _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo):
            rel_opp_bet = _sd.get_opponents_bet()
            print('*** Memory agent ***')
            if rel_opp_bet == -1: return ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
            what = pj.mem_agent(CURRENT_HAND, rel_opp_bet, _playersRemainingChips, _minimumAmountToRaiseTo, _maximumBet)
            if what == -1:
                return ClientBase.BettingAnswer.ACTION_FOLD
            elif what == 0:
                return ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
            #elif what == 'all-in':
            #    return ClientBase.BettingAnswer.ACTION_ALLIN,  _playersRemainingChips if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
            else:
                if what > _playersRemainingChips*0.5 and pj.hand_score(CURRENT_HAND) < 90: return ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
                return ClientBase.BettingAnswer.ACTION_RAISE,   (what) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
        else:
            return ClientBase.BettingAnswer.ACTION_FOLD
    
    # else:
    #     print('Choose a correct agent. Could you??')
    #return {'reflex': chooseRaiseOrFold_reflex_agent(),
    #        'mem': chooseRaiseOrFold_mem_agent()}.get(which_agent)
    # return {
    #     0: ClientBase.BettingAnswer.ACTION_FOLD,
    #     1: ClientBase.BettingAnswer.ACTION_ALLIN,
    #     2: ClientBase.BettingAnswer.ACTION_FOLD,
    #     3: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
    # }.get(random.randint(0, 3), chooseRaiseOrFold())

'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    print("Requested information about what cards to throw")
    print(_hand)
    yn, _cards = pj.wanna_change(_hand)
    wstuff_record("throw card action "+str(yn)+" the cards to throw "+str(_cards))
    
    str_card = ''
    #print("_cards....", _cards)
    if yn:
        print("These cards are throwen: ", _cards)
        if len(_cards) > 1:
            for c in _cards:
                str_card += c+' '
                #print('str_card:', str_card)
                #print('c of cardsssssss', c)
            return str_card
        else:
            return _cards[-1]
    else:
        print("No cards are throwen!!")
        return ''

# InfoFunction:

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    #_nrTimeRaised = 0
    global Opponents
    # history=pj.ReadData("Opponents_data.txt")
    # for alpha in Opponents:
    #     bet = Opponents[alpha][0][0]
    #     print(pj.predict(history, int(bet), pj.hand_score(CURRENT_HAND)))
    _sd.restart()
    print('Starting Round: ' + _round )
    wstuff_record('\n Starting Round: ' + _round)

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    print('The game is over.')
    wstuff_record('The game is over.\n\n\n')
    if which_agent == "mem": pj.EM_average.save_parameters()

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')
    if _playerName != POKER_CLIENT_NAME: 
        _sd.update_chips(_playerName, int(_chips))
    wstuff_record('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    global current_ante
    current_ante = int(_ante)
    print('The ante is: ' + _ante)
    wstuff_record('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")
    global recent_bet
    recent_bet = int(_forcedBet)
    wstuff_record("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    global recent_bet
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")
    if _playerName != POKER_CLIENT_NAME: _sd.update_bet(_playerName, int(_openBet))
    recent_bet = int(_openBet)
    
    wstuff_record("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    print("Player "+ _playerName +" checked.")
    wstuff_record("Player "+ _playerName +" checked.")  

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    global recent_bet
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")
    if _playerName != POKER_CLIENT_NAME:
        _sd.update_bet(_playerName, int(_amountRaisedTo))
        _sd.add_bet(_playerName, int(_amountRaisedTo))
    recent_bet = int(_amountRaisedTo)
    wstuff_record("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    print("Player "+_playerName +" called.")
    if _playerName != POKER_CLIENT_NAME:
        _sd.update_bet(_playerName, recent_bet)
        _sd.add_bet(_playerName, recent_bet)
    wstuff_record("Player "+_playerName +" called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")
    wstuff_record("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")
    if _playerName != POKER_CLIENT_NAME:
        _sd.update_bet(_playerName, int(_allInChipCount))
        _sd.add_bet(_playerName, int(_allInChipCount))
    wstuff_record("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")
    wstuff_record("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    global CURRENT_HAND
    global Opponents
    print("Player "+ _playerName +" hand " + str(_hand))
    if _playerName == POKER_CLIENT_NAME: CURRENT_HAND = _hand
    else:
        _sd.add_hand(_playerName, str(pj.hand_score(_hand)))
    wstuff_record("Player "+ _playerName +" hand " + str(_hand))
            
'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")
    wstuff_record("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")
    if _playerName == POKER_CLIENT_NAME: pj.EM_average.update_what_to_do(True)
    else: pj.EM_average.update_what_to_do(False)

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    #global Opponents
    print("Player "+ _playerName +" won " + _winAmount + " chips.")
    wstuff_record("Player "+ _playerName +" won " + _winAmount + " chips.")
    if _playerName == POKER_CLIENT_NAME: pj.EM_average.update_what_to_do(True)
    else: pj.EM_average.update_what_to_do(False)


def wstuff_record(t):
    if save_all_data_in_file:
        al = open(wstuff, 'a')
        line = "\n" + t
        al.write(line)
        al.close()
    return
        

