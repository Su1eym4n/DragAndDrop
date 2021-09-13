# DragAndDrop

#About
In this programm you will be able to drag, drop and resize opjects you see, using your gestures.

To move objects with one hand, use your middle and tip fingers. 
- If middle and tip fingers are far like in the `V sign` the user will go through the object without changing its state. 
- If fingers are close and inside the object, the object will follow fingers' position.

To move objects with both hands, use thumb and tip finger on both hands.
- If hands are relaxed, nothing will change.
- If thumb and tip fingers are positioned perpendicularly to each other on both hands, and the point between is inside the object, object will change its size and position.  

## Set up the environment
Run following commands to set up the environment
- `python3 -m venv venv` create virtual environemnt
- `source venv/bin/activate` activate virtual environment
- `pip install cvzone` install cvzone
- `pip install opencv-python` install cv2

## Run the Code
To run the code simply type:
```
python main.py   
```
