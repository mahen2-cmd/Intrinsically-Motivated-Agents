Autonomous AI Agents and Intrinsic Motivation

We use intrinsically motivated reinforcement learning for two agents in a grid world environment. They are motivated by exploring unknown areas of the environment.  
There are no external rewards in this system unlike traditional reinforcement learning. The only rewards occur from the agents themselves in an intrinsic fashion. In a sense the agents are acting out of pure curiosity. 
They are fundamentally motivated by curiosity and cooperation. The cooperation protocol will be explained below.
There is also a heavy box placed at a particular point in the environment. The box can only be pushed when both agents push the box together. And, the agents get an extra reward for pushing it together.
This is used to reward cooperation.
If the agents manage to push the box to a specific corner of the environment, then a portal opens up at another point of the environment. The agents can pass through the portal to enter another land which they can explore.
We find that just using intrinsic motivation, with enough iterations, agents figure out how to push the box to the specified location and figure out how go through the portal and move to the other environment.
