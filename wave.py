"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.

The samples provided in the assignment description were used.

Author: Alec Galin (amg388)
Date: 12/09/2021
"""
from game2d import *
from consts import *
from models import *
import random


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or
    # None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _direction: the direction the aliens are moving
    # Invariant: _direction is either the string "left" or the string "right"
    #
    # Attribute _moved: a boolean that is true if _aliens moved down in the
    # last Alien "step". Initalized as True.
    # Invariant: _moved is either True or False
    #
    # Attribute _otherbolts: a boolean that is true if there are any bolts
    # fired by the player currently in the wave.
    # Invariant: _otherbolts is either True or False
    #
    # Attribute _random: a random number between 1 and BOLT_RATE from the
    # module consts.
    # Invariant: _random is an int such that 1 <= _random <= BOLT_RATE
    #
    # Attribute _moves: the number of Alien "steps" since the last bolt was
    # fired. Initialized as -1.
    # Invariant: _moves is an int such that -1 <= _random <= BOLT_RATE
    #
    # Attribute _animator: A coroutine to perform an animation
    # Invariant: _animator is a generator-based coroutine or None
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns _ship attribute.
        """
        return self._ship

    def getAliens(self):
        """
        Returns _aliens attribute.
        """
        return self._aliens

    def getBolts(self):
        """
        Returns _bolts attribute.
        """
        return self._bolts

    def getDline(self):
        """
        Returns _dline attribute.
        """
        return self._dline

    def getLives(self):
        """
        Returns _lives attribute.
        """
        return self._lives

    def getTime(self):
        """
        Returns _time attribute.
        """
        return self._time

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIEN
    def __init__(self):
        """
        Initializes a wave object.
        """
        self._ship = Ship(bottom=SHIP_BOTTOM, x=GAME_WIDTH/2, width=SHIP_WIDTH,\
         height=SHIP_HEIGHT, source=SHIP_IMAGE, format=(2,4), frame=0)
        self._aliens  = self.aliens()
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], \
        linewidth=2, linecolor='red')
        self._lives = 3
        self._time = 0
        self._direction = 'right'
        self._moved = True
        self._otherbolts = False
        self._random = random.randint(1,BOLT_RATE)
        self._moves = -1
        self._animator = None

    def aliens(self):
        """
        Returns a 2d list of Alien instances applying relevant constants in the
        module consts.
        """
        all = []
        top_start = GAME_HEIGHT - ALIEN_CEILING - ((ALIEN_ROWS-1)*ALIEN_HEIGHT)\
         - ((ALIEN_ROWS-1)*ALIEN_V_SEP)
        source_index = 0
        for n in range(ALIEN_ROWS):
            if n % 2 == 0 and n != 0:
                if source_index == 2:
                    source_index = 0
                else:
                    source_index += 1
            source = ALIEN_IMAGES[source_index]
            row = []
            left_start = ALIEN_H_SEP
            for n in range(ALIENS_IN_ROW):
                row.append(Alien(top=top_start, left=left_start, \
                width=ALIEN_WIDTH, height=ALIEN_HEIGHT, source=source))
                left_start += (ALIEN_H_SEP + ALIEN_WIDTH)
            all.append(row)
            top_start += (ALIEN_V_SEP + ALIEN_HEIGHT)

        return all

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, ship_amount, input, alien_hor_amount, alien_vert_amount, \
    speed, dt):
        """
        Moves ship, aliens, and laser bolt.

        Precondition: ship_amount is an int or float
        Precondition: input is an instance of GInput
        Precondition: alien_amount is an int or float
        Precondition: speed is an int or float
        Precondition: dt is an int or float
        """
        self.moveShip(ship_amount, input)
        self.moveAliens(alien_hor_amount, alien_vert_amount, speed, dt)
        self.shipBolts(input)
        self.alienBolts()
        self.moveBolts()
        self.alienCollisions()
        self.animateShip(dt)

    # HELPER METHODS FOR UPDATE
    # SHIP HELPER METHODS FOR UPDATE
    def moveShip(self, amount, input):
        """
        Moves the _ship attribute amount to the right each time right key is
        pressed.

        Left key moves the _ship attribute amount to the left.

        Precondition: amount is an int or float
        Precondition: input is an instance of GInput
        """
        if self._ship == None or self._animator != None:
            return
        to_move = 0
        if input.is_key_down("left") and (not self.shipAtLeftEdge()):
            to_move -= amount
        if input.is_key_down("right") and (not self.shipAtRightEdge()):
            to_move += amount
        if self.shipAtLeftEdge() or self.shipAtRightEdge():
            self.moveShipToEdge()
        self._ship.moveShip(to_move)

    def shipAtLeftEdge(self):
        """
        Returns True if the attribute _ship is at the left edge of the window.

        If _ship is None, the function returns False.
        """
        if self._ship == None:
            return False

        return self._ship.atLeftEdge()

    def shipAtRightEdge(self):
        """
        Returns True if the attribute _ship is at the right edge of the window
        as defined in consts.

        If _ship is None, the function returns False.
        """
        if self._ship == None:
            return False

        return self._ship.atRightEdge()

    def moveShipToEdge(self):
        """
        Moves ship to correct position at edge of the game window as defined in
        the module consts.
        """
        try:
            self._ship.moveToEdge()
        except:
            pass

    def animateShip(self, dt):
        """
        Animates the ship.

        Precondition: dt is an int or float greater than or equal to 0.
        """
        if not self._animator == None:
            try:
                self._animator.send(dt)
            except StopIteration:
                self._animator = None
                self._ship = None
        elif self.shipCollides():
            self._animator = self._ship.animateExplosion()
            next(self._animator)

    def newShip(self):
        """
        Creates a new ship.
        """
        self._ship = Ship(bottom=SHIP_BOTTOM, x=GAME_WIDTH/2, \
        width=SHIP_WIDTH, height=SHIP_HEIGHT, source=SHIP_IMAGE, format=(2,4), \
        frame=0)

    # ALIEN HELPER METHODS FOR UPDATE
    def moveAliens(self, hor_amount, vert_amount, speed, dt):
        """
        Moves each alien in a 2d list of aliens hor_amount right after speed
        seconds;
        once aliens hit an edge, aliens move down and in the opposite direction.

        Precondition: hor_amount is an int or float greater than or equal to 0
        Precondition: ver_amount is an int or float greater than or equal to 0
        Precondition: speed is an int or float
        Precondition: dt is an int or float
        """
        if self._time >= speed:
            if self.aliensAtRight() and self._moved == False:
                self.moveAliensDown(vert_amount)
                self._direction = 'left'
                self._moved = True
            elif self.aliensAtLeft() and self._moved == False:
                self.moveAliensDown(vert_amount)
                self._direction = 'right'
                self._moved = True
            elif self.aliensNearRight() and not self.aliensAtRight():
                self.moveAliensToRightEdge()
            elif self.aliensNearLeft() and not self.aliensAtLeft() and \
            self._moved == False:
                self.moveAliensToLeftEdge()
            else:
                if self._direction == 'right':
                    self.moveAliensHorizontal(hor_amount)
                    self._moved = False
                elif self._direction == 'left':
                    self.moveAliensHorizontal(-hor_amount)
                    self._moved = False
            self._time = 0
        else:
            self._time += dt

    def moveAliensHorizontal(self, amount):
        """
        Moves each alien in a 2d list of aliens amount to the right. If amount
        is negative, the aliens move |amount| left.

        Precondition: amount is an int or float.
        """
        for row in self._aliens:
            for alien in row:
                try:
                    alien.moveHorizontal(amount)
                except:
                    pass

    def moveAliensDown(self, amount):
        """
        Moves each alien in a 2d list of aliens amount down.

        Precondition: amount is an int or float greater than or equal to 0
        """
        for row in self._aliens:
                for alien in row:
                    try:
                        alien.moveVertical(-amount)
                    except:
                        pass

    def checkEmpty(self):
        """
        Returns True if _aliens is empty.
        """
        if len(self._aliens) == 0:
            return True
        #checks if _aliens only contains None objects
        num_of_aliens = 0
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    num_of_aliens += 1
        if num_of_aliens == 0:
            return True

        return False

    def checkEmptyRow(self, row):
        """
        Returns True if list of Alien instances is empty.

        Precondition: row is a list of Alien instances.
        """
        for n in range(len(row)):
            none_count = 0
            for alien in row:
                if alien == None:
                    none_count += 1
            if none_count >= ALIENS_IN_ROW:
                return True

    def leftMostAlien(self):
        """
        Returns list where first element is row of leftmost alien second
        element is column of leftmost alien in that row.
        """
        if self.checkEmpty():
            return
        farthest = {}
        for n in range(len(self._aliens)):
            if self.checkEmptyRow(self._aliens[n]):
                continue
            else:
                row = self._aliens[n]
                for i in range(len(row)):
                    if row[i] == None:
                        continue
                    else:
                        farthest[n] = i
                        break
        farthest_row = min(farthest, key=farthest.get)
        column = farthest[farthest_row]

        return [farthest_row,column]

    def rightMostAlien(self):
        """
        Returns list where first element is row of rightmost alien second
        element is column of rightmost alien in that row.
        """
        if self.checkEmpty():
            return
        farthest = {}
        for n in range(len(self._aliens)):
            if self.checkEmptyRow(self._aliens[n]):
                continue
            else:
                row = self._aliens[n][::-1]
                for i in range(len(row)):
                    if row[i] == None:
                        continue
                    else:
                        farthest[n] = len(row) - i - 1
                        break
        farthest_row = max(farthest, key=farthest.get)
        column = farthest[farthest_row]

        return [farthest_row,column]

    def aliensAtLeft(self):
        """
        Returns True if _aliens are at left edge. Else returns False.
        """
        if self.checkEmpty():
            return False
        leftmost = self.leftMostAlien()
        leftmost_row = leftmost[0]
        column = leftmost[1]
        if self._aliens[leftmost_row][column].atLeftEdge():
            return True

        return False

    def aliensAtRight(self):
        """
        Returns True if _aliens are at right edge. Else returns False.
        """
        if self.checkEmpty():
            return False
        rightmost = self.rightMostAlien()
        rightmost_row = rightmost[0]
        column = rightmost[1]
        if self._aliens[rightmost_row][column].atRightEdge():
            return True

        return False

    def aliensNearLeft(self):
        """
        Returns True if leftmost alien in _aliens in ALIEN_H_SEP away or less
        from left edge. Else returns False.
        """
        if self.checkEmpty():
            return False
        leftmost = self.leftMostAlien()
        leftmost_row = leftmost[0]
        column = leftmost[1]
        if self._aliens[leftmost_row][column].nearLeftEdge():
            return True

        return False

    def aliensNearRight(self):
        """
        Returns True if rightmost alien in _aliens is ALIEN_H_SEP away or less
        from left edge. Else returns False.
        """
        if self.checkEmpty():
            return False
        rightmost = self.rightMostAlien()
        rightmost_row = rightmost[0]
        column = rightmost[1]
        if self._aliens[rightmost_row][column].nearRightEdge():
            return True

        return False

    def aliensAtEdge(self):
        """
        Returns True if _aliens are at left or right edge. Else returns False.
        """
        if self.checkEmpty():
            return False
        try:
            if self.aliensAtLeft() or self.aliensAtRight():
                return True
        except:
            pass

        return False

    def moveAliensToLeftEdge(self):
        """
        Moves 2D list of Aliens to left edge.
        """
        if self.checkEmpty():
            return
        leftmost = self.leftMostAlien()
        leftmost_row = leftmost[0]
        column = leftmost[1]
        distance_to_move = self._aliens[leftmost_row][column].getLeft() - \
        ALIEN_H_SEP
        for row in self._aliens:
            for alien in row:
                try:
                    alien.moveHorizontal(-distance_to_move)
                except:
                    pass

    def moveAliensToRightEdge(self):
        """
        Moves 2D list of Aliens to right edge.
        """
        if self.checkEmpty():
            return
        rightmost = self.rightMostAlien()
        rightmost_row = rightmost[0]
        column = rightmost[1]
        distance_to_move = GAME_WIDTH - ALIEN_H_SEP - \
        self._aliens[rightmost_row][column].getLeft() - ALIEN_WIDTH
        for row in self._aliens:
            for alien in row:
                try:
                    alien.moveHorizontal(distance_to_move)
                except:
                    pass

    # BOLT HELPER METHODS FOR UPDATE
    def shipBolts(self, input):
        """
        Shoots bolts out of the ship if the up key is pressed.

        Bolts are removed if they reach higher than GAME_HEGHT defined in the
        module consts.

        Bolts can only be fired if there are no other player bolts on the
        screen.

        Precondition: input is a valid instance of GInput
        """
        if self._ship == None:
            return
        otherbolts = False
        if input.is_key_down('up'):
            for bolt in self._bolts:
                if bolt.isPlayerBolt():
                    otherbolts = True
            if otherbolts == False:
                self._bolts.append(Bolt(bottom = (self._ship.getBottom() + \
                SHIP_HEIGHT), left = (self._ship.getX()-(BOLT_WIDTH/2)), width \
                = BOLT_WIDTH, height = BOLT_HEIGHT, linecolor = 'yellow', \
                fillcolor = 'yellow', velocity = BOLT_SPEED))
        too_high_removed = []
        for bolt in self._bolts:
            if bolt.getBottom() <= GAME_HEIGHT:
                too_high_removed.append(bolt)
        self._bolts = too_high_removed

    def alienBolts(self):
        """
        Shoots bolts from the bottom row of a random column of self._aliens.

        Bolts are shot at random rate such that 1 <= the number of alien steps
        between bolt firings <= BOLT_RATE (as defined in the modules consts).
        """
        if self._time == 0:
            self._moves += 1
        if self._moves >= self._random:
            #only fire from non empty column
            all_none = True
            while all_none:
                none_count = 0
                randcolumn = random.randint(0,ALIENS_IN_ROW-1)
                for row in self._aliens:
                    if row[randcolumn] == None:
                        none_count += 1
                if none_count < ALIEN_ROWS:
                    all_none = False
                else:
                    pass
            #make alien in last row that's not none shoot bolt
            for n in range(len(self._aliens)):
                if self._aliens[n][randcolumn] != None:
                    self._bolts.append(Bolt(bottom = (self._aliens[n]\
                    [randcolumn].getTop() - ALIEN_HEIGHT - BOLT_HEIGHT),\
                    left = self._aliens[n][randcolumn].getLeft(), width = \
                    BOLT_WIDTH, height = BOLT_HEIGHT, linecolor = 'purple', \
                    fillcolor = 'purple', velocity = -BOLT_SPEED))
                    break
            self._random = random.randint(1,BOLT_RATE)
            self._moves = 0

    def moveBolts(self):
        """
        Moves each Bolt instance in _bolts at the proper velocity.
        """
        for bolt in self._bolts:
            bolt.moveVertical(bolt.getVelocity())

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the wave in view.

        Precondition: view is a valid instance of GView
        """
        try:
            self._ship.draw(view)
        except AttributeError:
            pass
        for row in self._aliens:
            for alien in row:
                try:
                    alien.draw(view)
                except:
                    pass
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def alienCollisions(self):
        """
        Replaces an Alien instance with None if it collides with a player bolt.

        A player bolt is also removed if it collides with an Alien instance
        """
        for n in range(len(self._aliens)):
            for i in range(len(self._aliens[n])):
                new_bolts = []
                for bolt in self._bolts:
                    try:
                        if self._aliens[n][i].collides(bolt):
                            self._aliens[n][i] = None
                        else:
                            new_bolts.append(bolt)
                    except:
                        new_bolts.append(bolt)
                self._bolts = new_bolts

    def shipCollides(self):
        """
        Returns True is the ship collides with a bolt. Else returns False.

        Removes bolt if ship collides with it and lowers _lives by 1.
        """
        collision = False
        if self._ship == None:
            return False
        new_bolts = []
        for bolt in self._bolts:
            if self._ship.collides(bolt):
                collision = True
                break
            else:
                new_bolts.append(bolt)
        self._bolts = new_bolts
        if collision == True:
            self._lives -= 1

        return collision

    # MISC METHODS
    def wonGame(self):
        """
        Returns True if there are no aliens left. Else Returns False
        """
        if self.checkEmpty():
            self.clearBolts()
            return True

        return False


    def aliensCross(self):
        """
        Returns True if any Alien instance crosses the defense line.
        """
        for row in self._aliens:
            for alien in row:
                try:
                    if (alien.getTop() - ALIEN_HEIGHT) <= DEFENSE_LINE:
                        return True
                except:
                    pass

        return False

    def moreLives(self):
        """
        Returns True if _lives is greater than 0. Else returns False.
        """
        if self._lives > 0:
            return True

        return False

    def clearBolts(self):
        """
        Sets the _bolt attribute to an empty list.
        """
        self._bolts.clear()
