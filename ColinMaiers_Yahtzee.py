import pygame, simpleGE, random
""" Colin Maiers
    Yahtzee
"""

class SplashScreen(simpleGE.Scene):
    def __init__(self):
        super().__init__(size=(1280, 720))
        self.background.fill((20, 50, 100))  

        self.lblTitle = simpleGE.Label()
        self.lblTitle.center = (640, 200)
        self.lblTitle.text = "YAHTZEE"
        self.lblTitle.font = pygame.font.Font("freesansbold.ttf", 72)
        self.lblTitle.fgColor = (255, 255, 255)
        self.lblTitle.bgColor = (20, 50, 100)
        self.lblTitle.size = (400, 100)

        self.lblSubtitle = simpleGE.Label()
        self.lblSubtitle.center = (640, 300)
        self.lblSubtitle.text = "Roll the dice and score big!"
        self.lblSubtitle.font = pygame.font.Font("freesansbold.ttf", 24)
        self.lblSubtitle.fgColor = (200, 200, 200)
        self.lblSubtitle.bgColor = (20, 50, 100)
        self.lblSubtitle.size = (400, 50)

        self.lblInstructions = simpleGE.MultiLabel()
        self.lblInstructions.center = (640, 450)
        self.lblInstructions.textLines = [
            "Instructions:",
            "• Click dice to lock them before rolling",
            "• You get 3 rolls per turn",
            "• Choose a scoring category after rolling",
            "• Try to get the highest score possible!"
        ]
        self.lblInstructions.font = pygame.font.Font("freesansbold.ttf", 20)
        self.lblInstructions.fgColor = (255, 255, 255)
        self.lblInstructions.bgColor = (20, 50, 100)
        self.lblInstructions.size = (600, 200)

        self.btnStart = simpleGE.Button()
        self.btnStart.center = (540, 600)
        self.btnStart.text = "START GAME"
        self.btnStart.font = pygame.font.Font("freesansbold.ttf", 24)
        self.btnStart.size = (200, 50)
        self.btnStart.bgColor = (100, 150, 255)
        self.btnStart.fgColor = (255, 255, 255)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (740, 600)
        self.btnQuit.text = "QUIT"
        self.btnQuit.font = pygame.font.Font("freesansbold.ttf", 24)
        self.btnQuit.size = (200, 50)
        self.btnQuit.bgColor = (255, 100, 100)
        self.btnQuit.fgColor = (255, 255, 255)

        self.sprites = [self.lblTitle, self.lblSubtitle, self.lblInstructions, 
                       self.btnStart, self.btnQuit]

    def process(self):
        if self.btnStart.clicked:
            game = Game()
            game.start()
            self.stop()

        if self.btnQuit.clicked:
            self.stop()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__(size=(1280, 720))
        self.setImage("background.png")

        self.sndRoll = simpleGE.Sound("diceRoll.wav")

        self.dice = []
        for i in range(5):
            newDie = Die(self)
            newDie.position = (140 + (i * 120), 450)
            self.dice.append(newDie)

        self.rollCount = 0
        self.maxRolls = 3
        self.totalScore = 0

        self.btnRoll = BtnRoll()
        self.lblInfo = simpleGE.Label()
        self.lblInfo.center = (380, 580)
        self.lblInfo.text = "Click dice to lock. Max 3 rolls."

        self.lblScore = simpleGE.Label()
        self.lblScore.center = (900, 688)
        self.lblScore.text = "Total Score: 0"

        self.btnMenu = simpleGE.Button()
        self.btnMenu.center = (50, 50)
        self.btnMenu.text = "Menu"
        self.btnMenu.size = (80, 30)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (150, 50)
        self.btnQuit.text = "Quit"
        self.btnQuit.size = (80, 30)
        self.btnQuit.bgColor = (255, 100, 100)
        self.btnQuit.fgColor = (255, 255, 255)

        self.scoreButtons = []
        categories = [
            "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Three of a Kind", "Four of a Kind", "Full House",
            "Small Straight", "Large Straight", "Yahtzee", "Chance"
        ]
        for i, name in enumerate(categories):
            cat_key = name.lower().replace(" ", "_")
            btn = ScoreButton(name, cat_key, self)
            btn.center = (900, 100 + i * 40)
            self.scoreButtons.append(btn)

        self.sprites = self.dice + [self.btnRoll, self.lblInfo, self.lblScore, 
                                   self.btnMenu, self.btnQuit] + self.scoreButtons

    def rollAll(self):
        if self.rollCount < self.maxRolls:
            self.sndRoll.play()
            for die in self.dice:
                die.roll()
            self.rollCount += 1

    def resetTurn(self):
        self.rollCount = 0
        for die in self.dice:
            die.locked = False
            die.roll()

    def process(self):
        if self.btnRoll.clicked:
            self.rollAll()

        if self.btnMenu.clicked:
            splash = SplashScreen()
            splash.start()
            self.stop()

        if self.btnQuit.clicked:
            self.stop()

        if self.rollCount >= self.maxRolls:
            self.lblInfo.text = "Select a score category"
        else:
            self.lblInfo.text = f"Rolls left: {self.maxRolls - self.rollCount}"

        self.lblScore.text = f"Total Score: {self.totalScore}"

        # End condition
        if all(btn.used for btn in self.scoreButtons):
            final = FinalScreen(self.totalScore)
            final.start()
            self.stop()

    def processEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.resetTurn()

    def calculate_score(self, category):
        values = [die.value for die in self.dice]
        counts = {i: values.count(i) for i in range(1, 7)}
        total = sum(values)

        if category == "ones": return counts.get(1, 0) * 1
        elif category == "twos": return counts.get(2, 0) * 2
        elif category == "threes": return counts.get(3, 0) * 3
        elif category == "fours": return counts.get(4, 0) * 4
        elif category == "fives": return counts.get(5, 0) * 5
        elif category == "sixes": return counts.get(6, 0) * 6
        elif category == "three_of_a_kind": return total if any(c >= 3 for c in counts.values()) else 0
        elif category == "four_of_a_kind": return total if any(c >= 4 for c in counts.values()) else 0
        elif category == "full_house": return 25 if 3 in counts.values() and 2 in counts.values() else 0
        elif category == "small_straight":
            straights = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
            return 30 if any(s.issubset(set(values)) for s in straights) else 0
        elif category == "large_straight":
            return 40 if set(values) in [set([1,2,3,4,5]), set([2,3,4,5,6])] else 0
        elif category == "yahtzee": return 50 if any(c == 5 for c in counts.values()) else 0
        elif category == "chance": return total
        return 0

class Die(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("1_dots.png")
        self.setSize(80, 80)
        self.locked = False
        self.images = [None] + [
            pygame.transform.scale(pygame.image.load(f"{i}_dots.png"), (80, 80))
            for i in range(1, 7)
        ]
        self.roll()

    def roll(self):
        if not self.locked:
            self.value = random.randint(1, 6)
            self.copyImage(self.images[self.value])

    def process(self):
        if self.clicked:
            self.locked = not self.locked
            self.image.set_alpha(100 if self.locked else 255)

class BtnRoll(simpleGE.Button):
    def __init__(self):
        super().__init__()
        self.center = (380, 530)
        self.text = "Roll 'em (R)"

class ScoreButton(simpleGE.Button):
    def __init__(self, label, category, scene):
        super().__init__()
        self.text = label
        self.category = category
        self.scene = scene
        self.used = False

    def update(self):
        super().update()
        if self.clicked and not self.used:
            score = self.scene.calculate_score(self.category)
            self.scene.totalScore += score
            self.used = True
            self.bgColor = (150, 150, 150)
            self.scene.resetTurn()

class FinalScreen(simpleGE.Scene):
    def __init__(self, finalScore):
        super().__init__(size=(1280, 720))
        self.background.fill((0, 30, 60))

        self.lblGameOver = simpleGE.Label()
        self.lblGameOver.center = (640, 200)
        self.lblGameOver.text = "Game Over!"
        self.lblGameOver.font = pygame.font.Font("freesansbold.ttf", 72)
        self.lblGameOver.fgColor = (255, 255, 255)
        self.lblGameOver.bgColor = (0, 30, 60)
        self.lblGameOver.size = (500, 100)

        self.lblFinalScore = simpleGE.Label()
        self.lblFinalScore.center = (640, 300)
        self.lblFinalScore.text = f"Final Score: {finalScore}"
        self.lblFinalScore.font = pygame.font.Font("freesansbold.ttf", 36)
        self.lblFinalScore.fgColor = (255, 255, 255)
        self.lblFinalScore.bgColor = (0, 30, 60)
        self.lblFinalScore.size = (400, 80)

        self.btnRestart = simpleGE.Button()
        self.btnRestart.center = (540, 450)
        self.btnRestart.text = "Play Again"
        self.btnRestart.font = pygame.font.Font("freesansbold.ttf", 24)
        self.btnRestart.size = (200, 50)
        self.btnRestart.bgColor = (100, 150, 255)
        self.btnRestart.fgColor = (255, 255, 255)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (740, 450)
        self.btnQuit.text = "Quit"
        self.btnQuit.font = pygame.font.Font("freesansbold.ttf", 24)
        self.btnQuit.size = (200, 50)
        self.btnQuit.bgColor = (255, 100, 100)
        self.btnQuit.fgColor = (255, 255, 255)

        self.sprites = [self.lblGameOver, self.lblFinalScore,
                        self.btnRestart, self.btnQuit]

    def process(self):
        if self.btnRestart.clicked:
            splash = SplashScreen()
            splash.start()
            self.stop()

        if self.btnQuit.clicked:
            self.stop()

def main():
    splash = SplashScreen()
    splash.start()

if __name__ == "__main__":
    main()
