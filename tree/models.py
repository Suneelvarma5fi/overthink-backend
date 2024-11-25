from django.db import models

class Node(models.Model):
    outcomeID = models.IntegerField(unique=True)  # Binary tree node ID
    stateOutcome = models.TextField()  # Description of the state or decision
    stateStorySummary = models.TextField()  # Summary of the current state
    stateAdditionalContext = models.TextField(null=True, blank=True)  # Optional context
    positiveChildID = models.IntegerField(null=True, blank=True)  # Positive branch
    negativeChildID = models.IntegerField(null=True, blank=True)  # Negative branch

    def __str__(self):
        return f"Node {self.outcomeID}: {self.stateOutcome}"