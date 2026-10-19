Suppose the vacuum cleaner has a unique function of returning home to recharge batteries. Places are clean, 
but there is a trap in our place (marked as -1) where the robot can get stuck! Also, we have an obstacle 
that you can't move in (marked as X). For this, use the 4x4 environment. The vacuum cleaner moves in four 
directions following the MDP algorithm. This environment uses the same rule as our Grid World (80% N, 10% E and 10% W).

1) You aim to create a function that looks for the recharge spot (marked with 10).

2) Test your robot with three different living costs (rewards). 

Print a log with the path followed by the vacuum cleaner. Submit your program with a log (or your notebook results)  
and a video showing it running. Only one group member needs to record the video.

Environment initial setup. 

Tip: you can implement this as an expectimax and the rewards control or use the MDP function available in the vacuum world.


0	0	0	start
0	X	0	0
0	0	0	0
0	-1	0	10
