from .agent import Agent
from copy import deepcopy
from math import inf
import GameAgents.evaluation_functions


class Node:
    def __init__(self, parent=None, value=0, move=None, engine=None):
        self.value = value
        self.children = []
        self.parent = parent
        self.move = move
        self.engine = engine


class MinimaxAgent(Agent):
    def __init__(self, engine, player, depth=3):
        self.engine = engine
        self.depth = depth
        self.root = None
        self.player = player
        self.agent_type = 'Minimax'

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or node.engine.game_state is not None:
            return node
        if maximizing_player:
            max_child = None
            max_value = -inf
            for move in node.engine.get_valid_moves():
                child = self.build_child(parent=node, move=move)
                child_max = self.minimax(child, depth-1, False).value
                if max_value <= child_max:
                    max_child = child
                    max_value = child_max
                    node.value = max_value
            return max_child
        else:
            min_child = None
            min_value = inf
            for move in node.engine.get_valid_moves():
                child = self.build_child(parent=node, move=move)
                child_min = self.minimax(child, depth-1, True).value
                if min_value >= child_min:
                    min_child = child
                    min_value = child_min
                    node.value = min_value
            return min_child

    def build_child(self, parent, move):
        child = Node(parent=parent, move=move, engine=deepcopy(parent.engine))
        child.engine.make_move(move)
        child.value = self.compute_position_value(child.engine)
        parent.children.append(child)
        return child

    def compute_position_value(self, engine):
        return GameAgents.evaluation_functions.simple_eval(engine)

    def compute_next_move(self):
        self.root = Node(engine=deepcopy(self.engine))
        # self.construct_value_tree(self.root, engine_copy, self.depth)
        node = self.minimax(self.root, self.depth, self.player == 1)
        print(f'{self.agent_type}: {chr(node.move.x + 97)}{node.move.y}, Board Eval: {node.value}')
        return node.move
