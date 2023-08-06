from fastnode2vec import Node2Vec, Graph
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
    
def n2v_algorithm(G, node=1, picked=10, train_time = 30, Weight=False, **kwargs):
    """
    Description
    -----------
    Performs FastNode2Vec algorithm with full control on the crucial parameters.
    In particular, this function allows the user to keep working with networkx objects
    -- that are generally quite user-friendly -- instead of the ones required by the fastnode2vec
    algorithm.

    Parameters
    ----------
    G : networkx.Graph object
        Sets the network that will be analyzed by the algorithm.
    p : float
        Sets the probability '1/p' necessary to perform the fastnode2vec random walk. It affects how often the walk is
        going to immediately revisit the previous node. The smaller it is, the more likely the node will be revisited.
    q : float
        Sets the probability '1/q' necessary to perform the fastnode2vec random walk. It affects how far the walk
        will go into the network. The smaller it is, the larger will be the distance from the initial node.
    node : int, optional
        Sets the node from which to start the analysis. This is a gensim.models.word2vec parameter.
        The default value is '1'.
    picked : int, optional
        Sets the first 'picked' nodes that are most similar to the node identified with 'node'. This is a
        gensim.models.word2vec parameter.
        The default value is '10'.
    train_time : int, optional
        Sets the number of times we want to apply the algorithm. It is the 'epochs' parameter in Node2Vec.
        The value of this parameter drastically affect the computational time.
        The default value is '5'.
    Weight : bool, optional
        Specifies if the algorithm must also consider the weights of the links. If the networks is unweighted this
        parameter must be 'False', otherwise it receives too many parameters to unpack.
        The default value is 'False'.
    Returns
    -------
    output : ndarray, ndarray
        The output of the function is a tuple of two numpy arrays. The first contains the top 'picked' most similar
        nodes to the 'node' one, while the second contains their similarities with respect to the 'node' one.

    Notes
    -----
    - The node parameter is by default an integer. However, this only depends on the node labels that are given to the nodes in the network.
    - The rest of the parameters in **kwargs are the ones in fastnode2vec.Node2Vec constructor, I only specified what I considered.
    - I noticed that the walk_length parameter should be at least #Nodes/2 in order to be a solid walk.
    the most relevant q and p.
    
    Examples
    --------
    >>> G = nx.generators.balanced_tree(r=3, h=4)
    >>> nodes, similarity = n2v_algorithm(G, dim=128, walk_length=30, 
                                          context=100, p=0.1, q=0.9, workers=4)
        nodes: [0 4 5 6 45 40 14 43 13 64]
        similarity: [0.81231129 0.81083304 0.760795 0.7228986 0.66750246 
                     0.64997339 0.64365959 0.64236712 0.63170493 0.63144475]
    
    """
    if Weight == False:
        G_fn2v = Graph(G.edges(), directed = False, weighted = Weight)
    else:
        G_fn2v = Graph(list(G.edges.data("weight", default = 1)), directed = False, weighted = Weight)
    n2v = Node2Vec(G_fn2v, **kwargs)
    n2v.train(epochs=train_time)
    nodes = n2v.wv.most_similar(node, topn = picked)
    nodes_id = list(list(zip(*nodes))[0])
    similarity = list(list(zip(*nodes))[1])
    nodes_id = np.array(nodes_id)
    similarity = np.array(similarity)
    return nodes_id, similarity

def Draw(G, nodes_result, title = 'Community Network', **kwargs):
    """
        Description
        -----------
        Draws a networkx plot highlighting some specific nodes in that network. The last node is higlighted in red, the remaining nodes
        in "nodes_result" are in blue, while the rest of the network is green.

        Parameters
        ----------
        G : networkx.Graph object
            Sets the network that will be drawn.
        nodes_result : ndarray
            Gives the nodes that will be highlighted in the network. The last element will be red, the others blue.
        title : string, optional
            Sets the title of the plot.

        Notes
        -----
        - This function returns a networkx draw plot, which is good only for networks with few nodes (~40). For larger networks I suggest to use other visualization methods, like Gephi.

        Examples
        --------
        >>> G = nx.generators.balanced_tree(r=3, h=4)
        >>> nodes, similarity = n2v_algorithm(G, dim=128, walk_length=30, context=100, p=0.1, q=0.9, workers=4)
        >>> red_node = 2
        >>> nodes = np.append(nodes, red_node)
        >>> Draw(G, nodes)
        """
    color_map = []
    for node in G:
        if node == int(nodes_result[-1]):
            color_map.append('red')
        elif node in nodes_result:
            color_map.append('blue')
        else:
            color_map.append('green')
    plt.figure(figsize = (7, 5))
    ax = plt.gca()
    ax.set_title(title, fontweight = "bold", fontsize = 18, **kwargs)
    nx.draw(G, node_color = color_map, with_labels = True)
    plt.show()
