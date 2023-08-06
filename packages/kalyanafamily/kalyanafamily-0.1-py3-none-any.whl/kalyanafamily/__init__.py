class Father():
    def skills(self):
        print("working SE")

class Mather():
    def skill(self):
        print("cooking")

class Child(Father, Mather):
        def skill(self):
            Father.skills(self)
            Mather.skill(self)
            print("playing")