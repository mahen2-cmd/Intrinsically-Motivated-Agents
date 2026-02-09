# Autonomous AI Agents and Intrinsic Motivation

We study **intrinsically motivated reinforcement learning** in a grid-world environment with two autonomous agents. Unlike traditional reinforcement learning setups, **there are no external task-based rewards**. Instead, the agents are driven entirely by **intrinsic rewards**, encouraging exploration and curiosity.

---

## Intrinsic Motivation

The agents receive rewards for:
- Exploring previously unknown areas of the environment  
- Reducing uncertainty about their surroundings  

As a result, their behavior emerges from **pure curiosity**, rather than explicit goals imposed by the environment designer.

---

## Cooperation Mechanism

The environment contains a **heavy box** placed at a fixed location.  
This box:
- Cannot be moved by a single agent  
- Can only be pushed when **both agents act together**

When the agents successfully push the box cooperatively, they receive an **additional intrinsic reward**, explicitly reinforcing cooperative behavior.

---

## Environment Progression

If the agents manage to push the box to a designated corner of the grid:
- A **portal** opens at another location in the environment  
- The agents can enter the portal and transition to a **new environment**  

This new environment provides additional unexplored areas, further fueling intrinsic motivation.

---

## Emergent Behavior

Despite the absence of external rewards or predefined objectives, we observe that:
- With sufficient training iterations  
- The agents learn to coordinate their actions  
- They discover how to push the box cooperatively  
- They successfully activate the portal and transition to the new environment  

This demonstrates that **intrinsic motivation alone**, combined with minimal cooperative incentives, is sufficient for the emergence of complex, goal-directed, and cooperative behaviors.
