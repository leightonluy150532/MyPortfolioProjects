class Animals:
    
    def _init_(self, name = None, kingdom=  None):
        self.name = name
        self.Kingdom = Kingdom

        def sound(self):
            print(f"{self.name} Animals moans in the bed)
        def move(self):
            print(f"{self.name} Animals moved")
        def bark(self):
            print(f"{self.name} Animals bark")
            

class Mammals(Animals):
    def _init_(self,name):
        super()._init_(name, "Animals")

    def sound(self):
        print(f"{self.name} Animals moans in the bed)
    def move(self):
        print(f"{self.name} Animals moved")
    def bar(self):
        print(f"{self.name} Animals bark")

    def feed_milk(self):
        print(f"{self.name} Animels fed milk")

class Dogs(Mammals):
    def _init_(self,name):
        super()._init_(self, name, breed)
        self.breed = breed
    def sound(self):
        print(f"{self.name} Animals moans in the bed)    
    def bark(self):
        print(f"{self.name} Animals bark")
class Poodle(Dogs):
    def _init_(self, name, is_hypoallergenic):
        super()._init_(name, "Poodle")
        self.is_hypoallergenic = is_hypoallergenic

    def _groom(self):
        print(f"{self.name} is being groomed")
class bird(Animals):
    def _init_(self, "Animals"):
        super()._init_
    
