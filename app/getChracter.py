from random import randint as rand

class getChracter():
    def __init__(self):
        self.chracters = ['🐼','🐻','🐘','🐭','🐬','🦀','🐞','🪳','🍀','🍁','🍎','🌶️ ','🛺','🌟','☃️ ','🔥','❄️ ','🧸','🎭','🎸','🔎','⚙️ ',
        '🔓','📌','☢️ ','😎 ','🤠','💀','👻','✌️ ','🤟','🧙','👣']
        ...

    def chracter(self)->chr:
        return self.chracters[rand(0,len(self.chracters)-1)]
        ...



# obj=getChracter()
# print(obj.chracter())