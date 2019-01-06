from collections import Counter
import numpy
from neurotic.tangles.data_paths import DataPath

SPLIT_ON_THIS = " "
 
def plot_network():
    """
    Creates a simplified plot of our network (simple_network.dot.png)
    """
    graph = Graph(format="png")
    graph.attr(rankdir="LR")
    
    graph.node("a", "horrible")
    graph.node("b", "excellent")
    graph.node("c", "terrible")
    graph.node("d", "")
    graph.node("e", "")
    graph.node("f", "")
    graph.node("g", "")
    graph.node("h", "positive")
    
    graph.edges(["ad", "ae", "af", "ag",
                 "bd", "be", "bf", "bg",
                 "cd", "ce" , "cf", "cg"])
    graph.edges(["dh", 'eh', 'fh', 'gh'])
    graph.render("graphs/simple_network.dot")
    graph
    return

def update_input_layer(review:str, layer_0: numpy.ndarray, word2index: dict) -> Counter:
    """ Modify the global layer_0 to represent the vector form of review.
    The element at a given index of layer_0 should represent
    how many times the given word occurs in the review.

    Args:
        review: the string of the review
        layer_0: array representing layer 0
        word2index: dict mapping word to index in layer_0
    Returns:
         counter for the tokens (used for troubleshooting)
    """
    # clear out previous state by resetting the layer to be all 0s
    layer_0 *= 0
    tokens = review.split(SPLIT_ON_THIS)
    counter = Counter()
    counter.update(tokens)
    for key, value in counter.items():
        layer_0[:, word2index[key]] = value
    return counter

def get_target_for_label(label: str) -> int:
    """Convert a label to `0` or `1`.
    Args:
        label(string) - Either "POSITIVE" or "NEGATIVE".
    Returns:
        `0` or `1`.
    """
    return 1 if label=="POSITIVE" else 0
