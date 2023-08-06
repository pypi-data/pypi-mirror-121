# SBPGeologyHeron Package

Hi, I'm Mohammad Ghiasvand Mohammadkhani, the author of this python scientific package .
This package and the programming idea of this package to solve the Heron shortest problem is unique in the World Wide Web and I am the first person who has created this python package .

To use this scientific package,at first you need to install it by pip command, then you have to code the text in the quotation, "from SBPGeologyHeron import SBPGeologyHeron" ;Then if you want to see an output from that, you need to do the following path in the next paragraph .

The description of Heron shortest path problem is 'Which path minimizes the distance needed to get water from the river and then transport it to the green village from the position that you were at first ?'
If you imagine the all of the Axis x as the river and code the text in the quotation, "print(SBPGeologyHeron.heronShortestPath())", you need to pass 4 arguments into heronShortestPath function ;The first one is the x-coordinate of the first position and the second one is the y-coordinate of the first position and the third one is the x-coordinate of the green village position and the fourth one is the y-coordinate of the green village position ;Then if you run the code it will give you the exact spot of the river that you have to pick up water from that to wend the shortest possible path (it means, if you go to that spot from your first position in a straight line and go to the green village afterwards in a straight line, you have transported water by wending the shortest possible path).

But please note that if you enter one of the y coordinates equal to zero, or entering one of the y coordinates negative and also the other one positive, you will encounter to an error (because in that case Heron shortest path problem is not defined due to it would be really easy to solve it in that way and the answer would be a straight line that matches the first position to the green village position). 

Thanks,
Hope to be helpful for you .
