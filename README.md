# Sheep and Wolves
A typical crossing river puzzle

## Rules
The task is getting sheep and wolves across a river for some reason. If the wolves ever outnumber the sheep on either side of the river, the wolves will overpower and eat the sheep. You have a boat, which can only take one or two animals in it at a time, and must have at least one animal in it because you’ll get lonely (and because the problem is trivial otherwise). How do you move all the animals from one side of the river to the other?

In the original Sheep & Wolves problem, we specified there were 3 sheep and 3 wolves; here, though, your agent should be able to solve the problem for an arbitrary number of initial sheep and wolves. You may assume that the initial state of the problem will follow those rules (e.g. we won’t give you more wolves than sheep to start). However, not every initial state will be solvable; there may be combinations of sheep and wolves that cannot be solved.

You will return a list of moves that will solve the problem, or an empty list if the problem is unsolvable based on the initial set of Sheep and Wolves. You will also submit a brief report describing your approach.

## Algorithm
Depth-first search
