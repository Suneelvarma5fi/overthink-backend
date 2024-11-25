import json
from tree.main import outcomeGenerator  # Import the actual generator function

# Initialize the tree structure
tree_dict = {}  # Start with an empty dictionary


# Binary Tree Node Calculations
def get_child_ids(parent_id):
    """
    Calculate positive and negative child IDs for a given parent node ID.
    """
    return parent_id * 2, parent_id * 2 + 1


# Add Node to the Tree
def add_node(parent_id, positive_outcome, negative_outcome, stateStorySummary, stateAdditionalContext=None):
    """
    Add positive and negative child nodes to the tree, based on parent_id.
    """
    pos_child_id, neg_child_id = get_child_ids(parent_id)

    # Add Positive Node
    tree_dict[pos_child_id] = {
        "stateOutcome": positive_outcome,
        "stateStorySummary": stateStorySummary,
        "stateAdditionalContext": stateAdditionalContext,
        "positiveChildID": None,
        "negativeChildID": None,
    }

    # Add Negative Node
    tree_dict[neg_child_id] = {
        "stateOutcome": negative_outcome,
        "stateStorySummary": stateStorySummary,
        "stateAdditionalContext": stateAdditionalContext,
        "positiveChildID": None,
        "negativeChildID": None,
    }

    # Update Parent Node
    tree_dict[parent_id] = {
        **tree_dict[parent_id],
        "positiveChildID": pos_child_id,
        "negativeChildID": neg_child_id,
    }


# Expand Node
def expand_node(outcomeID, stateAdditionalContext=None):
    """
    Expand the selected node by generating positive and negative outcomes.
    """
    if outcomeID not in tree_dict:
        raise ValueError(f"Node with outcomeID {outcomeID} does not exist.")

    # Get parent node details
    parent_node = tree_dict[outcomeID]
    stateOutcome = parent_node["stateOutcome"]
    stateStorySummary = parent_node["stateStorySummary"]

    # Generate outcomes using the actual outcomeGenerator
    response = outcomeGenerator(
        outcomeID=outcomeID,
        stateOutcome=stateOutcome,
        stateStorySummary=stateStorySummary,
        stateAdditionalContext=stateAdditionalContext or "none"
    )

    positive_outcome = response["positive_outcome"]
    negative_outcome = response["negative_outcome"]
    generated_stateStorySummary = response["stateStorySummary"]

    # Add children to the tree
    add_node(outcomeID, positive_outcome, negative_outcome, generated_stateStorySummary, stateAdditionalContext)


def save_tree_to_file():
    """
    Save the tree dictionary to a JSON file.
    The filename is derived from the first 20 characters of the root node's stateOutcome.
    """
    if 1 not in tree_dict:
        print("Error: Root node is missing. Cannot save the tree.")
        return

    # Get the root node's stateOutcome
    root_state_outcome = tree_dict[1]["stateOutcome"]

    # Create a safe filename using the first 20 characters
    safe_filename = root_state_outcome[:20].replace(" ", "_").replace("/", "_") + ".json"

    # Save the tree to the file
    try:
        with open(safe_filename, "w") as f:
            json.dump(tree_dict, f, indent=4)
        print(f"Tree saved successfully as {safe_filename}")
    except Exception as e:
        print(f"Error saving tree: {e}")


def load_tree_from_file(filename="tree.json"):
    """
    Load the tree dictionary from a JSON file.
    """
    global tree_dict
    with open(filename, "r") as f:
        tree_dict = json.load(f)


# Traversal for Debugging
def traverse_tree(nodeID, depth=0):
    """
    Traverse the tree structure and print details.
    """
    if nodeID not in tree_dict:
        return
    node = tree_dict[nodeID]
    print("  " * depth + f"Node {nodeID}: {node['stateOutcome']}")
    if node["positiveChildID"]:
        traverse_tree(node["positiveChildID"], depth + 1)
    if node["negativeChildID"]:
        traverse_tree(node["negativeChildID"], depth + 1)


# User Interaction Loop
def user_interaction():
    """
    Interactive loop for the user to define and expand the tree.
    """
    print("Welcome to Overthink! Let's explore your decision tree.")

    # If the tree is empty, prompt for the first node
    if not tree_dict:
        root_state_outcome = input("Enter the initial state or action you are considering (e.g., 'I want to quit my job and start a company'): ")
        tree_dict[1] = {
            "stateOutcome": root_state_outcome,
            "stateStorySummary": f"You decided to {root_state_outcome.lower()}.",
            "stateAdditionalContext": None,
            "positiveChildID": None,
            "negativeChildID": None,
        }
        print(f"Root node created: {tree_dict[1]['stateOutcome']}")

    while True:
        # Show the current tree
        print("\nCurrent Tree Structure:")
        traverse_tree(1)

        # Ask user for action
        user_input = input(
            "\nEnter the outcomeID you want to expand (or type 'exit' to quit, 'save' to save the tree): "
        )

        if user_input.lower() == "exit":
            print("Exiting Overthink. Goodbye!")
            break
        elif user_input.lower() == "save":
            save_tree_to_file()
            print("Tree saved successfully!")
            continue

        try:
            # Validate and convert outcomeID
            outcomeID = int(user_input)
            if outcomeID not in tree_dict:
                print(f"Invalid outcomeID: {outcomeID}. Please try again.")
                continue

            # Ask for additional context (optional)
            additional_context = input(
                "Enter additional context for this outcome (or press Enter to skip): "
            )

            # Expand the chosen node
            expand_node(outcomeID, stateAdditionalContext=additional_context)
            print(f"Node {outcomeID} expanded successfully!")

        except ValueError:
            print("Invalid input. Please enter a valid outcomeID or command.")


# Example Usage
if __name__ == "__main__":
    user_interaction()