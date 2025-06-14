from collections import deque
from typing import Dict, List, Set, Iterable

class AhoCorasick:
    """
    Aho-Corasick algorithm implementation for multiple pattern matching
    """
    
    class TrieNode:
        """Inner class representing a node in the Aho-Corasick trie."""
        
        def __init__(self):
            self.children: Dict[str, AhoCorasick.TrieNode] = {}
            self.failure = None
            self.outputs: List[str] = []
    
    def __init__(self, patterns: Iterable[str]):
        """
        Initialize the Aho-Corasick automaton with a list of patterns.
        
        Args:
            patterns: List of keyword patterns to search for
        """
        self.root = self.TrieNode()
        self.build_trie(patterns)
        self.build_failure_links()
    
    def build_trie(self, patterns: Iterable[str]):
        """
        Build a trie from the list of patterns.
        
        Args:
            patterns: List of keyword patterns to add to the trie
        """
        for pattern in patterns:
            current_node = self.root
            
            for char in pattern:
                if char not in current_node.children:
                    current_node.children[char] = self.TrieNode()
                current_node = current_node.children[char]
            
            current_node.outputs.append(pattern)
    
    def build_failure_links(self):
        """Build failure links for the Aho-Corasick automaton using BFS."""
        queue = deque()
        
        # Set failure links for depth 1 nodes to root
        for char, child in self.root.children.items():
            child.failure = self.root
            queue.append(child)
        
        # BFS to set failure links for the rest of the nodes
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                failure = current.failure
                
                while failure is not None and char not in failure.children:
                    failure = failure.failure
                
                if failure is None:
                    child.failure = self.root
                else:
                    child.failure = failure.children[char]
                    # Add outputs of failure node to this node
                    child.outputs.extend(child.failure.outputs)
    
    def search(self, text: str) -> Dict[str, List[int]]:
        """
        Search for all pattern occurrences in the text.
        
        Args:
            text: The text to search in
            
        Returns:
            Dictionary mapping each matched pattern to a list of positions where it was found
        """
        result: Dict[str, List[int]] = {}
        current_node = self.root
        
        for i in range(len(text)):
            char = text[i]
            
            # Follow failure links until we find a valid transition
            while current_node != self.root and char not in current_node.children:
                current_node = current_node.failure
            
            # Make a transition if possible
            if char in current_node.children:
                current_node = current_node.children[char]
            
            # Process any pattern matches at this position
            for pattern in current_node.outputs:
                position = i - len(pattern) + 1
                if pattern not in result:
                    result[pattern] = []
                result[pattern].append(position)
        
        return result