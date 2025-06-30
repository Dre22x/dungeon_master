import random
from typing import List

def roll_dice(kind: str, number_of_rolls: int) -> List[int]:
  """
  Rolls a dice of the given kind, number of times, and sides.
  """
  rolls = []
  for i in range(number_of_rolls):
    if kind == "d20":
      rolls.append(random.randint(1, 20))
    elif kind == "d12":
      rolls.append(random.randint(1, 12))
    elif kind == "d10":
      rolls.append(random.randint(1, 10))
    elif kind == "d8":
      rolls.append(random.randint(1, 8))
    elif kind == "d6":
      rolls.append(random.randint(1, 6))
  
  return rolls


if __name__ == "__main__":
  print(roll_dice("d20", 3))