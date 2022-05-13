from collections import deque, defaultdict


class Node:
    def __init__(self, state, action=None):
        self.state = state
        self.action = action


class State:
    def __init__(self, left, right, d=1):
        """
        State represents the number of animals on left and right sides of t he river.
        Args:
            left: A tuple (sheep, wolves) contained the number of sheep and wolves on left side.
            right: A tuple (sheep, wolves) contained the number of sheep and wolves on right side.
            d: The direction of the boat
        """
        self.boat = (left, right)  # eg. start state = ((sheep, wolves), (0, 0))
        self.direction = d

    def valid_state(self, s, w):
        """
        Check if current state is valid. Does wolves outnumber sheep on either left side or right side? Does the
        number of sheep or wolves transported in range?
        Returns:
            True if not violated the constraint. False otherwise.
        """
        for lst in self.boat:
            if (0 < lst[0] < lst[1]) or (lst[0] < 0 or lst[1] < 0) or (s < lst[0] or w < lst[1]):
                return False
        return True

    def goal_test(self, s, w):
        """
        Check if the state is a goal state. The state is a goal state when Left side of river is empty and all animals
        are on right side.
        Returns:
            Return True if no animals on left side and all animals on right. Otherwise, return False.
        """
        return self.boat == ([0, 0], [s, w])

    def successors(self, state, s, w):
        """
        Find all possible next actions which are valid and all the new states are based on current state.
        Args:
            s: Number of initial sheep
            w: Number of initial wolves
            state: Containing the number of sheep and the number of wolves on both side.
        Returns:
            A list of tuples [(new state, action)].
        """
        result = []
        possible_actions = [(0, 1), (1, 0), (1, 1), (0, 2), (2, 0)]  # a list of tuples of all possible actions.
        lst = [i for i in state.boat]

        for action in possible_actions:
            new_state = State(lst[0], lst[1], state.direction)
            # reverse direction
            new_state.direction = 1 - new_state.direction
            # When the boat travel from left to right(direction= == 0), increase the number of animals on right
            # side and then decrease the number of animals on left side. When boat direction is travelling to left(
            # direction == 1), do the opposite.
            if new_state.direction == 0 and action in possible_actions[2:]:
                l = [new_state.boat[0][0] - action[0], new_state.boat[0][1] - action[1]]
                r = [new_state.boat[1][0] + action[0], new_state.boat[1][1] + action[1]]
                new_state.boat = (l, r)
                if new_state.valid_state(s, w):
                    result.append((new_state, action))

            elif new_state.direction == 1 and action in possible_actions[:3]:
                l = [new_state.boat[0][0] + action[0], new_state.boat[0][1] + action[1]]
                r = [new_state.boat[1][0] - action[0], new_state.boat[1][1] - action[1]]
                new_state.boat = (l, r)
                if new_state.valid_state(s, w):
                    result.append((new_state, action))

        return result


class SemanticNetsAgent:
    def __init__(self):
        self.parent_dict = defaultdict()  # track the states that we already had

    def solution(self, parent):
        """
        A function returns the solution.
        Args:
            parent: A default dictionary represents new state as keys and their parent as values.

        Returns:
            A a list of moves from start state to goal state.
        """
        node = (list(parent.keys())[-1])
        moves = []

        while node.action:
            moves.append(node.action)
            node = parent[node]
        moves.reverse()
        return moves

    def bfs(self, state, s, w):
        """
        Implementation of BFS. Perform the goal test right after obtaining all the possible next states. If one of the
        next state is target, then return and call solution() immediately.
        Returns:
            Class method solution() and pass self.parent_dict as parameter.
        """
        frontier = deque([Node(state)])
        visited = set()
        depth = -1

        while True:
            depth += 1
            if not frontier:
                return []

            node = frontier.popleft()

            for child_state, action in node.state.successors(node.state, s, w):
                child_node = Node(child_state, action)
                if child_state.goal_test(s, w):  # check if child state is goal state
                    self.parent_dict[child_node] = node
                    print("depth: ", depth)#debug
                    return self.solution(self.parent_dict)

                elif str([child_state.boat, child_state.direction]) not in visited:
                    if action != node.action:
                        self.parent_dict[child_node] = node
                        frontier.append(child_node)
                        visited.add(str([child_state.boat, child_state.direction]))

    def solve(self, initial_sheep, initial_wolves):
        """
        A main function to solve sheep & wolves problem.
        Args:
            initial_sheep: Number of sheep
            initial_wolves: Number of wolves
        Returns:
            A list of tuple that can successfully solve the problem.
            If the problem is unsolvable, return empty list.
        """
        initial_state = State([initial_sheep, initial_wolves], [0, 0])
        ans = []
        if initial_state.valid_state(initial_sheep, initial_wolves):
            ans = self.bfs(initial_state, initial_sheep, initial_wolves)
        return ans
