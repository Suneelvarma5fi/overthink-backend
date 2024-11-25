from .main import outcomeGenerator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Node
import json

@csrf_exempt
def create_root(request):
    """
    API endpoint to create the root node of the tree based on user input.
    """
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            stateOutcome = data.get("stateOutcome")

            # Check if the root node already exists
            if Node.objects.filter(outcomeID=1).exists():
                return JsonResponse({"error": "Root node already exists!"}, status=400)

            # Create the root node
            Node.objects.create(
                outcomeID=1,
                stateOutcome=stateOutcome,
                stateStorySummary=f"This is your starting point: {stateOutcome.lower()}",
                stateAdditionalContext=None,
                positiveChildID=None,
                negativeChildID=None,
            )
            return JsonResponse({"message": "Root node created successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def get_tree(request):
    """
    API endpoint to fetch the current decision tree.
    """
    nodes = Node.objects.all()
    tree_data = {
        node.outcomeID: {
            "stateOutcome": node.stateOutcome,
            "stateStorySummary": node.stateStorySummary,
            "stateAdditionalContext": node.stateAdditionalContext,
            "positiveChildID": node.positiveChildID,
            "negativeChildID": node.negativeChildID,
        }
        for node in nodes
    }
    return JsonResponse(tree_data)
@csrf_exempt
def expand_node(request):
    if request.method == "POST":
        try:
            # Parse request data
            data = json.loads(request.body)
            outcomeID = int(data.get("outcomeID"))
            additional_context = data.get("stateAdditionalContext", "none")

            # Fetch the parent node
            parent_node = Node.objects.get(outcomeID=outcomeID)

            # Call the outcomeGenerator to generate positive and negative outcomes
            from .main import outcomeGenerator
            outcomes = outcomeGenerator(
                stateOutcome=parent_node.stateOutcome,
                stateStorySummary=parent_node.stateStorySummary,
                stateAdditionalContext=additional_context
            )

            # Extract generated outcomes
            positive_outcome = outcomes["positive_outcome"]
            negative_outcome = outcomes["negative_outcome"]
            stateStorySummary = outcomes["stateStorySummary"]

            # Calculate child IDs
            positive_child_id = outcomeID * 2
            negative_child_id = outcomeID * 2 + 1

            # Add child nodes to the tree
            Node.objects.create(
                outcomeID=positive_child_id,
                stateOutcome=positive_outcome,
                stateStorySummary=stateStorySummary,
                stateAdditionalContext=additional_context,
            )
            Node.objects.create(
                outcomeID=negative_child_id,
                stateOutcome=negative_outcome,
                stateStorySummary=stateStorySummary,
                stateAdditionalContext=additional_context,
            )

            # Update parent node
            parent_node.positiveChildID = positive_child_id
            parent_node.negativeChildID = negative_child_id
            parent_node.save()

            return JsonResponse({
                "message": "Node expanded successfully!",
                "positiveChildID": positive_child_id,
                "negativeChildID": negative_child_id,
                "positiveOutcome": positive_outcome,
                "negativeOutcome": negative_outcome,
                "stateStorySummary": stateStorySummary
            })
        except Node.DoesNotExist:
            return JsonResponse({"error": "Node not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def reset_tree(request):
    """
    API endpoint to reset the tree by deleting all nodes.
    """
    if request.method == "POST":
        try:
            Node.objects.all().delete()  # Deletes all entries in the Node table
            return JsonResponse({"message": "Tree has been reset successfully!"})
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)