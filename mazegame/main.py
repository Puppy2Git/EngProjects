
class room:
  def __init__(self,text, connecitions = [False,False,False,False], ifNull = True):
    self.text = text
    self.connections = connecitions#N, E, S, W
    self.ifNull = ifNull

  def change_text(self,newtext):
    self.text = newtext
  def return_wall(self,dr):
    finish = ""
    if (not self.ifNull):
      if (dr == 0 or dr == 3):
        if (self.connections[0]):
          finish += "⌜   ⌝"
        else:
          finish += "⌜ ‾ ⌝"
      if (dr == 3):
        finish += "\n"
      
      if (dr == 1 or dr == 3):
        if (self.connections[3]):
          finish += "  "
        else:
          finish += "[ "
        finish += self.text
        if (self.connections[1]):
          finish += "  "
        else:
          finish += " ]"
        if (dr == 3):
          finish += "\n"
      if (dr == 2 or dr ==3):
        if (self.connections[2]):
          finish += "⌞   ⌟"
        else:
          finish += "⌞ _ ⌟"
    else:
      finish = "     "
    return finish
def display_rooms():
  todisp = ""
  for x in range(len(rooms)):
    for i in range(3):
      for y in range(len(rooms[x])):
        todisp += rooms[x][y].return_wall(i)
      todisp += "\n"
  print(todisp)

def updaterooms(old = [-1,-1],new = [-1,1]):
  if (old != [-1,-1]):
    rooms[old[0]][old[1]].change_text(" ")
  if (new != [-1,-1]):
    rooms[new[0]][new[1]].change_text("A")
    
def ismovepossible(old,new):
  global rooms
  if (old[1] < new[1]):#moving right
    direN = 3
    direO = 1
  elif (old[1] > new[1]):#moving left
    direN = 1
    direO = 3
  elif (old[0] > new[0]):#Moving down
    direN = 2
    direO = 0
  else:#Moving up
    direN = 0
    direO = 2
  return (rooms[old[0]][old[1]].connections[direO] and rooms[new[0]][new[1]].connections[direN])


def movecharacter(direction):
  global charpos
  newpos = []
  for e in charpos:
    newpos.append(e)
  if direction == "N":
    newpos[0] -= 1
  elif direction == "S":
    newpos[0] += 1
  elif direction == "E":
    newpos[1] += 1
  elif direction == "W":
    newpos[1] -= 1
  cando = True
  try:
    if (rooms[newpos[0]][newpos[1]].ifNull):
      cando = False
      print("Not real")
    if (newpos[0] == -1 or newpos[1] == -1):
      cando = False
      print("Has negative")
    if (not ismovepossible(charpos,newpos)):
      cando = False
      print("w h a t")
  except:
    cando = False
    print("HOW")
  if (cando):
    
    updaterooms(charpos,newpos)
    charpos = []
    for e in newpos:
      charpos.append(e)

rooms = [[],[]]
charpos = [0,0]


rooms[0].append(room(" ",[False,True,True,False],False))
rooms[0].append(room(" ",[False,False,True,True],False))
rooms[0].append(room(" ",[False,True,True,False],False))
rooms[0].append(room(" ",[False,False,False,True],False))
rooms[1].append(room(" ",[True,False,False,False],False))
rooms[1].append(room(" ",[True,True,False,False],False))
rooms[1].append(room(" ",[True,False,False,True],False))

updaterooms(new = charpos)
while True:
  print("Character position: [{0},{1}]".format(charpos[0],charpos[1]))
  display_rooms()
  userin = input(": ")
  movecharacter(userin)
  for i in range(0,25):
    print("")
print(" ")