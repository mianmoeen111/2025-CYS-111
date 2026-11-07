def minimax(node, maximizing_player):
  # Base case: if the node is a number (leaf), return its value
  if isinstance(node, (int, float)):
    return node

  if maximizing_player:
    # MAX node: choose the maximum value among children
    return max(minimax(child, False) for child in node)
  else:
    # MIN node: choose the minimum value among children
    return min(minimax(child, True) for child in node)


# Tree representation based on the diagram:
# Root is MAX, with three MIN subtrees, each containing 3 leaf nodes.
game_tree = [[4, 7, 2], [9, 1, 6], [3, 8, 5]]

# Evaluate starting with the root as the maximizing player (True)
root_value = minimax(game_tree, True)

print(f"The optimal value for the root MAX node is: {root_value}")