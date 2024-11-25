

from django.urls import path
from . import views

urlpatterns = [
    path('create_root/', views.create_root, name='create_root'),  # Create root node
    path('tree/', views.get_tree, name='get_tree'),              # Get tree structure
    path('expand/', views.expand_node, name='expand_node'),      # Expand a node
    path('reset/', views.reset_tree, name='reset_tree'),
]