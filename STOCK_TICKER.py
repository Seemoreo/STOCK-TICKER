# Globals

# Tuple
STOCKS = ("Industrial", "Grain", "Oil", "Bonds", "Gold", "Tech")

# STOCKS = ("MickeySoft","FarmCo","TMX_Pipe")

# maximum rolls
MAX_ROLLS = 20
# Maximum turns
MAX_TURNS = 200


### Just for the Jupyter Notebook
##from IPython.display import clear_output


class Stock():
    '''
    Stock object - attributes: name, price, split, offmkt
                    methods: up, down, div
    '''

    def __init__(self, name, price=100):
        self.name = name
        self.price = price
        self.split = 0
        self.offmkt = 0

    def __str__(self):
        return f'{self.name} - ${self.price / 100:1.2f}'

    def up(self, delta, ref, player):

        msg = ''
        if (self.price + delta) < 200:
            self.price += delta
        else:
            # Split Event
            msg = (f"{self.name} SPLITS! Share holdings DOUBLED! \n")
            # double all players holding of the stock
            for each in player:
                each.shares[ref] = 2 * each.shares[ref];
            self.offmkt += 1
            # Set it back to par
            self.price = 100
        return msg

    def down(self, delta, ref, player):
        msg = ''
        if (self.price - delta) > 0:
            self.price -= delta
        else:
            # Taken Off Market
            msg = (f"{self.name} $0.00 - taken off market\n")
            # Players holding of this stock goes to zero
            # loop through all players and set ref to zero
            for each in player:
                each.shares[ref] = 0
            self.offmkt += 1
            # Back to PAR
            self.price = 100
        return msg

    def div(self):
        # If dividends are payable (True/False)
        return (self.price >= 100)


import random


class Die():
    '''
    Die is a class for a multi-sided die
    "name" is a name for the die
    "sides" is a list of all possible values on the die
    "showing" is the current side that is face up
    '''

    def __init__(self, name, sides, showing=0):
        # list of values
        self.name = name
        self.sides = sides
        self.showing = showing

    def __str__(self):
        return (f'{self.name} \nPossible: {self.sides} \nCurrent Value: {self.sides[self.showing]}')

    def roll(self):
        rolled_side = random.randint(0, len(self.sides) - 1)
        self.showing = rolled_side
        return self.sides[rolled_side]


class Player():
    '''
    Player class and buy/sell/bankruptcy methods
    '''

    def __init__(self, name, cash=5000):
        self.name = name
        self.cash = cash
        self.shares = [0] * len(STOCKS)
        self.loan = 0

    def __str__(self):
        output = (f'Player: {self.name}\n')
        output += '\tCurrent Portfolio:\n'
        output += (f'\tCash:\t\t${self.cash:1.2f}\n')
        for i in range(0, len(self.shares)):
            if self.shares[i] != 0:
                output += (f'\t{STOCKS[i]}:\t\t{self.shares[i]}\n')
        output += (f'Total Value:\t\t${self.value(market):1.2f}\n')
        return output

    def value(self, market):
        value = self.cash
        for i in range(0, len(self.shares)):
            value += self.shares[i] * market[i].price / 100
        return value

    def buy(self, stock_ref, amount):
        # stock price * amount = $
        self.cash -= (market[stock_ref].price / 100 * amount)
        self.shares[stock_ref] += amount
        return

    def sell(self, stock_ref, amount):
        # stock price * amount = $
        self.cash += (market[stock_ref].price / 100 * amount)
        self.shares[stock_ref] -= amount
        return

    def bankruptcy(self):
        self.loan += 1
        self.cash = 1000
        self.shares = [0] * len(STOCKS)


def display_market(market):
    '''
    Create & Return a Ticker with all of the stocks in "market"
    '''
    ticker = '| '
    for stock in market:
        ticker += (f'{stock.__str__()}') + " | "

    hdiv = "+" + ("-" * int(len(ticker) - 3)) + "+"

    return hdiv + "\n" + ticker + "\n" + hdiv + "\n"


def setup_market(stocks):
    '''
    Create & return a list of Stock objects
    based on the list of Stocks passed in
    '''
    market = []
    for each in stocks:
        market.append(Stock(each, 100))
    return market


def setup_dice():
    '''
    Create & return a list of die objects that will be the dice
    '''
    dice = []
    dice.append(Die("Stock", STOCKS))
    dice.append(Die("Action", ("UP", "DOWN", "DIV", "UP", "DOWN", "DIV")))
    dice.append(Die("Amount", (5, 10, 20, 5, 10, 20)))
    return dice


def dice_roll(dice):
    '''
    Roll each die in a list of Die objects
    '''
    for die in dice:
        die.roll()
    return


def get_number_of_players():
    # How many players?
    number = 0
    while number not in range(1, 9):
        try:
            number = int(input("How many players? (1-8): "))
        except:
            print("=> Invalid entry! <=")
        if number not in range(1, 9):
            print(f"Sorry but {number} is not in the range (1-8). Please try again")
    return number


def player_setup(number):
    '''
    Get names & return a list of Player objects
    '''
    player = []
    prev_names = []
    for i in range(1, number + 1):
        input_loop = True
        while input_loop:
            try:
                # What is your name player '#'?
                name = str(input(f"Name of player {i}: "))
            except:
                print("Some Error occurred!!")
            else:
                if name in prev_names:
                    print(f'Sorry. {name} has already been used. Please try again.')
                else:
                    # We have a good name
                    prev_names.append(name)
                    player.append(Player(name))
                    input_loop = False
    return player


def choose_stock(trade):
    '''
    Return a single valid stock index to Stock tuple
    trade is a string of buy or sell for the prompt
    '''
    help_string = ''
    # Set choice to be more than the possible indexes for STOCKS tuple
    choice = len(STOCKS)
    while not choice in range(len(STOCKS)):
        try:
            stock_name = ''
            print(f'\nChoose one of {", ".join(STOCKS)}')
            while stock_name == '':
                # Input Stock to trade
                stock_name = str(input(f"{help_string}Which stock would you like to {trade}?: ")).capitalize()
            # check if we can match the entered string to stocks in the tuple
            index = [x for x, s in enumerate(list(STOCKS)) if stock_name in s]

            # Test - show the stock matched
            # This is my test error if player picked something that can't be matched
            int(index[0])

        except:
            print(f"I can't figure out what {stock_name} is. Please Try Again")
            help_string = "First letter or two please\n"
        else:
            # More than one match
            if len(index) > 1:
                matches = []
                for each in index:
                    matches.append(STOCKS[each])
                match_string = ", ".join(matches)
                print(f"That matches more than one stock: {match_string}")
                help_string = "\nCan you give me enough letters to figure it out please?\n"
            else:
                choice = index[0];

    return choice


def trade(current_player, market, initial=False):
    '''
    trade() gives each player a chance to buy or sell
    if initial is True, continues until player has made at least one purchase i.e. cash < 5000
    '''
    print(display_market(market))
    print(current_player)

    action = "unset"
    choice = "x"
    turn = 'subsequent'
    buy = False

    while 'q' not in action:
        # if initial
        if initial:
            print(f"\n\nLet's get started!\n\n{current_player.name} *must* buy at least one stock to begin\n")

            # it's buy
            turn = 'first'

            action = 'buy'
        else:
            while choice not in 'BSQ':
                # Player wants to buy or sell or quit?
                try:
                    choice = str(input("Buy/Sell/Quit (b/s/q)?").capitalize())
                except:
                    print("Some Error. Please try again")
                else:
                    if 'B' in choice:
                        action = 'buy'
                        print(display_market(market))
                    elif 'S' in choice:
                        if turn == 'first':
                            print("Sorry. You can\'t sell on the set up turn.")
                            action = "invalid"
                            choice = "x"
                        else:
                            action = 'sell'
                    elif 'Q' in choice:
                        if turn == 'first' and not buy:
                            print("Sorry. You to buy at least once on the set up turn.")
                            action = 'invalid'
                            choice = "x"
                        else:
                            action = 'quit'
                            return
                    else:
                        action = "invalid"
                        choice = 'x'

        # which stock
        stock_ref = choose_stock(action)
        # how much
        prompt_str = (f'How much {STOCKS[stock_ref]} (multiple of 500 shares) would you like to {action}?: ')
        amount = -1
        # valid (multiple of 500?)
        while amount % 500 != 0:
            try:
                amount = int(input(f"{prompt_str}"))
            except:
                print("Invalid entry. Must be an integer.")
            else:
                # it's valid int but...
                if amount % 500 == 0:
                    # It's a multiple of 500
                    # buy or sell?
                    if action == 'buy':
                        # Does player have enough cash?
                        if current_player.cash >= (market[stock_ref].price / 100 * amount):
                            # Player can afford the purchase
                            current_player.buy(stock_ref, amount)
                            print(f'\t{current_player.name} bought {amount} shares of {STOCKS[stock_ref]}')
                            print(current_player)
                            initial = False
                            buy = True
                            choice = "x"
                        else:
                            print(f"Your cash of ${current_player.cash:1.2f} isn't enough to buy ${amount * market[stock_ref].price / 100:1.2f} worth of {STOCKS[stock_ref]}")
                            amount = -1
                    elif action == 'sell':
                        # Does the player have enough shares to sell?
                        if current_player.shares[stock_ref] >= amount:
                            # Player has enough to cover the sell
                            current_player.sell(stock_ref, amount)
                            print(f'\t{current_player.name} sold {amount} shares of {STOCKS[stock_ref]}')
                            print(current_player)
                            initial = False
                            choice = "x"
                        else:
                            print(f"Your shares of {current_player.shares[stock_ref]} isn't enough to sell {amount} worth of {STOCKS[stock_ref]}")
                            amount = -1

                else:
                    print(f"Sorry: {amount} isn't a valid denomination of stock certificates.")

            # loop buy more or Q to quit?
    return


def end_of_game(market, player):
    '''
    end_of_game: args "market" list of Stock objects & "player" list of player objects
                    Sells off all shares at current price
                    Returns a list of all players that had the most cash at game end
    '''
    print(display_market(market))
    print("End of the game!\nTime to CA$H Out!")
    # loop through players
    for current_player in player:
        for ref in range(len(market)):
            if current_player.shares[ref] > 0:
                current_player.sell(ref, current_player.shares[ref])
        print("Liquidated!")
        print(current_player)
    # who had the most money?
    winner = [0]
    for index in range(len(player)):
        if player[index].cash > player[winner[0]].cash:
            winner = [index]
        elif player[index].cash == player[winner[-1]].cash and player[index].name != player[winner[-1]].name:
            winner.append(index)
    return winner


def turn_setup():
    '''
    This function sets up the number of dice rolls per round
    and number of trade turns in the game
    '''
    # How many players?
    rolls = 0
    while rolls not in range(1, MAX_ROLLS + 1):
        try:
            rolls = int(input(f"How many dice rolls per round? (1-{MAX_ROLLS}): "))
        except:
            # Default of 10
            rolls = 10
        if rolls not in range(1, MAX_ROLLS + 1):
            print(f"Sorry but {rolls} is not in the range (1-{MAX_ROLLS}). Please try again")
    turns = 0
    while turns not in range(1, MAX_TURNS + 1):
        try:
            turns = int(input(f"How many turns per game? (3-{MAX_TURNS}): "))
        except:
            # Default of 10
            turns = 10
        if turns not in range(1, MAX_TURNS + 1):
            print(f"Sorry but {turns} is not in the range (3-{MAX_TURNS}). Please try again")

    return (rolls, turns)


# Main
print("Welcome to Stock Ticker Py\n\tThe game that makes fortunes and fun(tm)\n\n")
print("\nThe object of the game, is to buy and sell stocks, and by so doing\n" +
      "accumulate a greater amount of money than the other players\nat the end of the game.")
print("The winner is decided by setting a time limit at the start of the\n" +
      "game, and is the person having the greastest amount of money,\n" +
      "after selling his stocks back to the Broker at their present market\n" +
      "value, plus their monies on hand\n")

# Initialize & Display the market
market = setup_market(STOCKS)
print(display_market(market))

# Initialize each die with tuples because sides don't change
dice_set = setup_dice()

# Initialize player list of player objects
player = player_setup(get_number_of_players())

# Players make first buys
first_trade = True
for each in player:
    trade(each, market, first_trade)

# Setup roll and turns
rolls, turns = turn_setup()

for x in range(turns):
    for y in range(rolls):
        dice_roll(dice_set)
        msg = ''
        for die in dice_set:
            msg += (f'{die.sides[die.showing]} ')
        print(msg + "\n")

        if (dice_set[1].sides[dice_set[1].showing]) == 'UP':
            #
            result = market[dice_set[0].showing].up(dice_set[2].sides[die.showing], dice_set[0].showing, player)
            print(result)
        elif (dice_set[1].sides[dice_set[1].showing]) == 'DOWN':
            #
            result = market[dice_set[0].showing].down(dice_set[2].sides[die.showing], dice_set[0].showing, player)
            print(result)
        else:
            # It's a Dividend
            # Is the stock is paying a dividend?
            if market[dice_set[0].showing].div():
                # Turn the 5,10 or 20 into 0.05, 0.10 or 0.20
                div_percent = dice_set[2].sides[die.showing] / 100
                # Does Player have any shares of the stock?
                for check_player in player:
                    if check_player.shares[dice_set[0].showing] > 0:
                        # add it to player.cash
                        check_player.cash += div_percent * check_player.shares[dice_set[0].showing]
            else:
                print(f"{market[dice_set[0].showing].name} is NOT paying a dividend at ${market[dice_set[0].showing].price / 100:1.2f}")

    for each in player:
        print(display_market(market))
        trade(each, market)

# End of the game
winners = end_of_game(market, player)
if len(winners) > 1:
    print("There was a tie!")
    output = ''
    for each in winners:
        output += (f'{player[each].name}, ')
    print(f'{output} each had ${player[winners[0]].cash:1.2f}')
elif len(player) == 1:
    # Solitare
    print(f"The winner of the game is {player[winners[0]].name}")
    print(f"with \t\t${player[winners[0]].cash:1.2f}")
    print(f"who is also the loser")
    print(f"who was the only player")
    print(f"Let me find you a nice participant ribbon :-P")

else:
    print(f"The winner of the game is {player[winners[0]].name}")
    print(f"with \t\t${player[winners[0]].cash:1.2f}")

