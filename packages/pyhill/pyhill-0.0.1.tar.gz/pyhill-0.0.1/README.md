# PyHill
Easily modify the readwritememory of Brick Hill

## Installation
In Command Prompt, run the command:
`pip install pyhill`
  
    
## How to Use
The first thing you should always do is use the function `attach()`. This attaches PyHill to Player.exe.

##### Modify Memory
To modify memory, use the `modify(variable, value)` function.  
Here is an example:
```python
import pyhill.pyhill as ph

ph.attach()            #Attach PyHill to the game
ph.modify("x", 2.5)    #Set your x position to 2.5
```
This script attaches PyHill to the game and sets the player's x position to 2.5.

##### Get Memory
To get memory, read the `get` class. Make sure to update the `get` class with the function `updateGet(only)`  
Here is an example:
```python
import pyhill.pyhill as ph

ph.attach()            #Attach PyHill to the game

while True:
    ph.updateGet("x")  #Update the x variable in the get class (if argument is left blank it will update every variable)
    print(ph.get.x)    #Print the player's current x position
```

##### Memory you can access
- `x` - The player's x position
- `y` - The player's y position
- `z` - The player's z position
- `fov` - The player's field of view
- `rotation` - The player's character rotation
- `zoom` - The player's camera zoom distance
- `fps` - The player's current frames per second *(can only be read and not modified)*
- `jump` - The player's current jump height  
  
More may be added in the future.

##### Custom (Advanced)
You can also modify custom memory pointers. This can be done using the `modifyCustom(baseaddress, offsets, datatype, value)` function.  
Here is an example:
```python
import pyhill.pyhill as ph

ph.attach()
ph.modifyCustom("0x0123456", "0x0, 0x1, 0x2, 0x3, 0x4", "double", 10)
```