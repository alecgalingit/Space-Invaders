"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

The samples provided in the assignment description were used.

Author: Alec Galin (amg388)
Date: 12/09/2021
"""
from consts import *
from game2d import *


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBottom(self):
        return self.bottom

    def getX(self):
        return self.x

    def getFormat(self):
        return self.format

    def getFrame(self):
        return self.frame

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, bottom, x, width, height, source, format, frame):
        """
        Initializes a ship.

        Precondition: bottom is an int or float
        Precondition: x is an int or float
        Precondition: width is an int or float
        Precondition: height is an int or float
        Precondition: source is a string refering to a valid file
        """
        super().__init__(bottom=bottom, x=x, width=width, height=height, \
        source=source, format=format, frame=frame)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveShip(self,amount):
        """
        Moves a ship "amount" to the right. Negative values of amount move the
        ship left.

        Precondition: amount is an int or float
        """
        self.x += amount

    def collides(self,bolt):
        """
        Returns True if an alien bolt collides with the ship

        This method returns False if bolt was not fired by an alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if not bolt.isPlayerBolt():
            if self.contains((bolt.getLeft(),bolt.getBottom())):
                return True
            if self.contains((bolt.getLeft(),bolt.getBottom()+BOLT_HEIGHT)):
                return True
            if self.contains((bolt.getLeft()+BOLT_WIDTH,bolt.getBottom())):
                return True
            if self.contains((bolt.getLeft()+BOLT_WIDTH,bolt.getBottom()+\
            BOLT_HEIGHT)):
                return True
        return False

    def atLeftEdge(self):
        """
        Returns True if a ship is at the left edge of the window.
        """
        if self.x <= (SHIP_WIDTH/2):
            return True
        else:
            return False

    def atRightEdge(self):
        """
        Returns True if a ship is at the right edge of the window as defined by
        GAME_WIDTH in the module consts.
        """
        if self.x >= GAME_WIDTH-(SHIP_WIDTH/2):
            return True
        else:
            return False

    def moveToEdge(self):
        """
        Moves ship to proper position at edge if hits that edge (to make sure
        the ship doesn't go over).
        """
        if self.atLeftEdge():
            self.x = (SHIP_WIDTH/2)
        if self.AtRightEdge():
            self.x = GAME_WIDTH-(SHIP_WIDTH/2)

    # COROUTINE METHOD TO ANIMATE THE SHIP
    def animateExplosion(self):
        time_added = 0
        steps = 8 / DEATH_SPEED
        animating = True
        while animating:
            dt = (yield)
            time_added += dt
            amount = steps*time_added
            if int(amount) > 7:
                animating = False
            else:
                self.frame = int(amount)


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTop(self):
        """
        Returns top attribute
        """
        return self.top

    def getLeft(self):
        """
        Returns left attribute
        """
        return self.left

    def setLeft(self, left):
        """
        Sets left attribute.

        Precondition: left is an int or float
        """
        self.left = left

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, top, left, width, height, source):
        """
        Initializes an alien.

        Precondition: top is an int or float
        Precondition: left is an int or float
        Precondition: width is an int or float
        Precondition: height is an int or float
        Precondition: source is a string refering to a valid file
        """
        super().__init__(top=top, left=left, width=width, height=height, \
        source=source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.isPlayerBolt():
            if self.contains((bolt.getLeft(),bolt.getBottom())):
                return True
            if self.contains((bolt.getLeft(),bolt.getBottom()+BOLT_HEIGHT)):
                return True
            if self.contains((bolt.getLeft()+BOLT_WIDTH,bolt.getBottom())):
                return True
            if self.contains((bolt.getLeft()+BOLT_WIDTH,bolt.getBottom()+\
            BOLT_HEIGHT)):
                return True

        return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def moveHorizontal(self, amount):
        """
        Moves Alien instance amount to the right. If the amount is negative,
        the Alien moves left.
        """
        self.left += amount

    def moveVertical(self, amount):
        """
        Moves Alien instance amount up. If the amount is negative, the Alien
        moves down.
        """
        self.top += amount

    def atLeftEdge(self):
        """
        Returns True if alien's left edge is at ALIEN_H_SEP (as defined in
        module consts). Else returns False.
        """
        if self.left <= ALIEN_H_SEP:
            return True

        return False

    def atRightEdge(self):
        """
        Returns True if alien's left edge is at GAME_WIDTH - ALIEN_H_SEP -
        ALIEN_WIDTH (as defined in module consts). Else returns False.
        """
        if self.left >= (GAME_WIDTH - ALIEN_H_SEP - ALIEN_WIDTH):
            return True

        return False

    def nearLeftEdge(self):
        """
        Returns True if alien is ALIEN_H_WALK away or less from left edge.
        """
        if (self.left - ALIEN_H_WALK) < ALIEN_H_SEP and not self.atLeftEdge():
            return True

    def nearRightEdge(self):
        """
        Returns True if alien is ALIEN_H_WALK away or less from right edge.
        """
        if (self.left + ALIEN_WIDTH + ALIEN_H_WALK) > (GAME_WIDTH - \
        ALIEN_H_SEP) and not self.atRightEdge():
            return True

    def atEdge(self):
        """
        Returns True if either the atleftedge() or the atrightedge() method
        return True.
        """
        return self.atLeftEdge() or self.atRightEdge()

    def atStart(self):
        """
        Returns True if alien's left edge is at ALIEN_H_SEP AND alien's top
        edge is at GAME_HEIGHT - ALIEN_CEILING
        (as defined in module consts). Else returns False.
        """
        if self.left == ALIEN_H_SEP and self.top == GAME_HEIGHT - \
        ALIEN_CEILING - ((ALIEN_ROWS-1)*ALIEN_HEIGHT) - \
        ((ALIEN_ROWS-1)*ALIEN_V_SEP):
            return True

        return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBottom(self):
        """
        Returns bottom attribute
        """
        return self.bottom

    def getLeft(self):
        """
        Returns left attribute
        """
        return self.left

    def getVelocity(self):
        """
        Returns velocity attribute
        """
        return self._velocity

    def __init__(self, bottom, left, width, height, linecolor, fillcolor, \
    velocity):
        """
        Initializes a Bolt.

        Precondition: bottom is an int or float
        Precondition: left is an int or float
        Precondition: width is an int or float
        Precondition: height is an int or float
        Precondition: linecolor is a string for a valid color
        Precondition: fillcolor is a string for a valid color
        Precondition: velocity is an int or float
        """
        super().__init__(bottom=bottom,left=left,width=width,height=height,\
        linecolor=linecolor,fillcolor=fillcolor)
        self._velocity = velocity

    def moveVertical(self, amount):
        """
        Moves bolt amount up. If amount is negative, bolt moves down.
        """
        self.bottom += amount

    def isPlayerBolt(self):
        """
        Returns true if bolt was fired by player. Else returns false.
        """
        if self._velocity > 0:
            return True
        elif self._velocity < 0:
            return False
