class Mover:
    def __init__(self, Name, TargetPosition, IsActive, State):
        self.Name = Name
        self.TargetPosition = TargetPosition
        self.IsActive = IsActive
        self.State = State

    def Move(self):
        if self.IsActive == False and self.TargetPosition >= 0:
            self.TargetPosition = 15
            self.IsActive = True
            self.State = "Default"
            print(self.TargetPosition)
            print(self.IsActive)
        else:
            self.TargetPosition = 0
            self.IsActive = False
            self.State = "Default"
            print(self.TargetPosition)
            print(self.IsActive)

    def Lockdown(self):
        if self.IsActive == True and self.TargetPosition >= 0 and self.State == "Default":
            self.TargetPosition = 0
            self.IsActive = False
            self.State = "Lockdown"
            print(self.TargetPosition)
            print(self.IsActive)
        else:
            self.TargetPosition = 0
            self.IsActive = False
            self.State = "Default"
            print(self.TargetPosition)
            print(self.IsActive)