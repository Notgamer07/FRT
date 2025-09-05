## FRT

requirements : pygame-ce       2.5.4

to install via terminal(if you have created Virtual Environment already): 
```bash 
pip install pygame-ce==2.5.4
```

**If You Don't Have Know How To Create Virtual Environment Then**

*  **ON WINDOWS**
```bash
python.exe -m venv venv
venv/Scripts/activate
pip install pygame-ce==2.5.4
```

* **ON MAC**
```bash
python3 -m venv venv
source venv/bin/activate
pip install pygame-ce==2.5.4
```
This project is make a game so irritating and insufferable that no one likes to play it.
As of now it now one rectangle (player) which is controlled through left arrow key and right arror key.
And you get the question and options (block with options on it) falling from top of screen
and you have to navigate the player(currently just a white rectangle) to avoid the wrong options
and collide with the right option. You have three hearts representing three possible mistake
you can do.


Currently, there are two branches -> ***Main***  and  ***AnimationIssue***


**MAIN BRANCH**

->audio    
| -> game-bonus-2-294446.mp3  
| -> game-level-complete-143022.mp3  
| -> level-up-89823.mp3  
->img  
| -> defeated.png  
| -> red-heart.png  
| -> star.png  
| -> VICTORY.png  
->UI  
| -> __init__.py  
| -> block.py  
| -> button.py  
| -> label.py  
| -> raisedButton.py  
->audio.py  
->data.json  
->datahandle.py  
->display_Elements.py  
->main.py  
->new_data.json  
->settings.json  

to run program, after activating virtual environment, enter this command in terminal but made sure that FRT folder is opened in terminal.   
```bash
python main.py
```
* OR
```bash
python3 main.py
```

----The *UI* folder contains the class Block, Button, Label, RaisedButton. 

Block class creates the block object that falls during **game** screen. this class
has an attribute *autofit* that fits the given text within limited dimension. This attribute was headache and causing problem for good week of coding this game. Righit, now it is fixed and working as intended (I think).

**autofit method**<details>*This attributes take boolean value and its 
set to true then its set the given text into specificed dimension initilised at the creation of
object. And it will store the necessary details of text (such as its rect, fontSize)
and will use that for displaying/drawing block. and will recalculate the text details
everytime a new text is given via set_text( new_text ) method.* </details>  

RaisedButton class is upgraded version of Button class.This class is like
Button but with an additional feature, the button of RaisedButton class
feels more like a button than button of Button class and the RaisedButton
can be disable so if in future it requires to lock a button until a certain
requirement is fulfilled then this class is to go. Honestly, I don't know
why I still have Button class. I might delete it in future.

**settings.json** Is there to store the music / sfx On or Off state only.
in future they will (hopefully) store more states such as sensitivity, volume, keyboard Only
or Mouse Only or both.  

**audio.py** according to settings store in setting.json, audio fill plays
audio when called upon by main.py

**data.json AND new_data.json** the data json file conatins about 30 question
all of which are basic arthmatics related. The new_data json stores some question 
of general knowledge also though currently only data.json is accessed by ***datahandle.py***


***THE ISSUE*** as of right now the issue in this branch is that the animation
feels choppy and sound needs to changed along with visuals of Victory and Defeat screen  

**AnimationIssue BRANCH**  


This branch was created for the sole purpose of dealing with animation issue.
after re-writing the whole code multiple times, and re checking everything in **MAIN BRANCH**
AND still not fixing the choppy animation issue. I gave up and created this Branch
where I re-wrote the whole logic but in single file, named ***testfile.py*** . and Surprisingly,
it worked!! why it worked? don't ask me cause I don't know. while working on it, I found the issue with Label class however after fixing that issue, the animation on main.py still felt choppy while in testfile.py the animation is smooth after that fix.

->audio  ------ *(Not used in this branch code at all as audio was not fixed in this)*  
| -> game-bonus-2-294446.mp3  
| -> game-level-complete-143022.mp3  
| -> level-up-89823.mp3  
->img  
| -> defeated.png  ------ *(not used)*  
| -> red-heart.png  
| -> star.png  
| -> VICTORY.png  ------ *(not used)*  
->UI  
| -> __init__.py  
| -> block.py  
| -> button.py  
| -> label.py  
| -> raisedButton.py  
->audio.py ------- ---- |  *(not used, I might remove it in future)*  
->data.json ----- ----- |  *(not used)*  
->datahandle.py --- --- |  *(not used)*  
->display_Elements.py |  *(not used)*  
->main.py -- -------- |  *(not used)*  
->new_data.json ----- |  *(not used)*  
->settings.json ----- |  *(not used, This needs to be implemented but after audio)*  
->data1.json -------- |  *(This has same data as data.json just in different manner)*  
->testfile.py ------- |  **MAIN FILE**  


to run program, after activating virtual environment, enter this command in terminal but made sure that FRT folder is opened in terminal.  
```bash
python testfile.py
```
* OR
```bash
python3 testfile.py
```

# Future-Things  
* Add audio to fixed code of AnimationIssue Branch.
* Add Victory/Defeat window to it.
* Add setting page.
* Remove unnecessary files on AnimationIssue Branch.
* Add dynamic creation of arthmatic question (probably will use code from Math-Game repo of mine.)
* Add image of player and more features.  

**IF you have read this till now and are infurated by this and Please consider me for internship at your workplace. ** 🥹🥹🥹  
📧 Email: [jagrath07@gmail.com](mailto:jagrath07@gmail.com) 
