from graphviz import Digraph

def get_node_color(role):
    if role == "Proponent":
        return "lightgreen"
    elif role == "Opponent":
        return "lightcoral"
    elif role == "Moderator":
        return "yellow"
    elif role == "Judge":
        return "gray"
    else:
        return "lightblue"

def get_node_shape(role):
    if role == "Moderator":
        return "diamond"
    elif role == "Judge":
        return "parallelogram"
    elif role == "Topic":
        return "ellipse"
    else:
        return "box"

def truncate_text(text, max_length=100):
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def visualize_debate(debate_data):
    # Create a new directed graph with larger size and custom settings
    dot = Digraph(graph_attr={'size': '12,8', 'ratio': 'fill'})
    
    # Set default node attributes for better readability
    dot.attr('node', fontsize='10', width='2', height='0.8')
    
    # Set graph attributes for better layout
    dot.attr(rankdir='TB', splines='ortho')

    # Create subgraphs for each round to maintain proper ordering
    with dot.subgraph(name='cluster_topic') as c:
        c.attr(label='Topic')
        c.node("Topic", truncate_text(debate_data["topic"]), 
               shape="ellipse", style="filled", fillcolor="lightblue", 
               fontsize='12', width='3')

    # Process each round
    current_round = -1
    for message in debate_data["rounds"]:
        if message["round"] != current_round:
            current_round = message["round"]
            if current_round >= 0:
                with dot.subgraph(name=f'cluster_round_{current_round}') as c:
                    if current_round > 0:
                        c.attr(label=f'Round {current_round}')
                    
                    # Create node for this message
                    node_id = f"{message['role']}_{current_round}"
                    node_label = truncate_text(message["text"])
                    c.node(node_id, node_label,
                          shape=get_node_shape(message["role"]),
                          style="filled",
                          fillcolor=get_node_color(message["role"]),
                          margin='0.2')
                    
                    # Connect to previous round if applicable
                    if current_round > 0:
                        # Connect Moderator to previous round's responses
                        if message["role"] == "Moderator":
                            dot.edge(f"Proponent_{current_round-1}", node_id)
                            dot.edge(f"Opponent_{current_round-1}", node_id)
                        # Connect responses to Moderator's question
                        elif message["role"] in ["Proponent", "Opponent"]:
                            dot.edge(f"Moderator_{current_round}", node_id)
                    else:
                        # Connect opening statements to topic
                        if message["role"] in ["Proponent", "Opponent"]:
                            dot.edge("Topic", node_id)

    # Render with higher DPI for better quality
    dot.render("debate_graph", format="png", cleanup=True)