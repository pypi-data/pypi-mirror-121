from BaseClass import MoverClass

# --// Inheritance

class AnotherMover(MoverClass):

    def Slide(self):
        self.TargetPosition = 5
        print(self.TargetPosition)