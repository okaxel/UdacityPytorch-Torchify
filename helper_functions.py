import plotly.graph_objs as go


def calculate_position(input_nodes, value):
    if value % 2 == 0:
        pos = round(((input_nodes-value)/2)*3,0)
    else:
        pos = round((((input_nodes-(value+1))/2))*3,0)
        
    return pos 

def create_node_nbr_dict(input_nodes, hidden_nodes, output_nodes):
    # node nbrs 
    node_list = []
    node_list.append(input_nodes)
    node_list = node_list + hidden_nodes
    node_list.append(output_nodes)
    keys = range(len(node_list))
    node_nbr_dict = {}

    for i in keys:
        node_nbr_dict[i] = node_list[i]
        
    return node_nbr_dict, node_list

def create_circles(node_nbr_dict, input_nodes):
    
    max_layer = list(node_nbr_dict.keys())[-1]
    min_layer = list(node_nbr_dict.keys())[0]
    circle_dict_list = []

    for key, value in node_nbr_dict.items():
        if key == min_layer: ## INPUT 
            circle_fill = 'rgba(50, 171, 96, 0.7)'
            circle_line = 'rgba(50, 171, 96, 1)'

        elif key == max_layer: #OUTPUT 
            circle_fill = 'rgba(229, 71, 27, 0.7)'
            circle_line = 'rgba(229, 71, 27, 1)'
        else:  # HIDDEN 
            circle_fill = 'rgba(247, 234, 98, 0.7)'
            circle_line = 'rgba(247, 234, 98, 1)'
                
        value = int(value)
        for i in range(value):
            pos = calculate_position(input_nodes, value)
            bef = list(node_nbr_dict.values())[key-1]
            
            circle_dict={'type': 'circle',
                         'fillcolor': circle_fill ,
                         'line': {'color': circle_line }
                        } 
            circle_dict['x0'] = key*6 + 1  
            circle_dict['x1'] = circle_dict['x0'] + 2 
            circle_dict['y0'] = (3*i+2) + pos
            circle_dict['y1'] = circle_dict['y0'] + 2 
            circle_dict_list.append(circle_dict)

    return circle_dict_list

def get_nodes(circle_dict_list, node_list, element):
    x = circle_dict_list 
    step_list = [0]
    nodes = []
    for i in node_list:
        if i == node_list[0]:
            y = x[:i]
        else:
            y = x[(step_list[-1]) : (step_list[-1]) + i]
        nodes.append(y)
        step_list.append(step_list[-1] + i)
    
    return nodes[element]

def draw_lines(actual_nodes, next_nodes): 
    line_dict_list = []

    actual_nodes_nbr = len(actual_nodes)
    next_nodes_nbr = len(next_nodes)

    for i in range(actual_nodes_nbr):
        actual_node = actual_nodes[i]
        for j in range(next_nodes_nbr):
            next_node = next_nodes[j]
            line_dict =  {'type': 'line', 'opacity': 1, 'line': {'width': 0.5}} 
            line_dict['x0'] = actual_node['x1']
            line_dict['x1'] = next_node['x0']
            line_dict['y0'] = actual_node['y0'] + 1
            line_dict['y1'] = next_node['y1'] - 1
            line_dict_list.append(line_dict)  
			
    return line_dict_list

def create_lines(node_nbr_dict, node_list, circle_dict_list):
    list_of_lines = []
    last_layer = list(node_nbr_dict.keys())[-1]
    for key, value in node_nbr_dict.items():
        if key != last_layer: 
            actual_layer = key
            next_layer = list(node_nbr_dict.keys())[key+1]
            actual_nodes = get_nodes(circle_dict_list, node_list,actual_layer)
            next_nodes = get_nodes(circle_dict_list, node_list,next_layer)
            list_of_lines += draw_lines(actual_nodes, next_nodes)
    return list_of_lines


def plot_neural_network(final_shape_list, input_nodes):
    max_range = input_nodes  * 3.1
    trace0 = go.Scatter(
        x=[],
        y=[],
        mode='text')
    
    data = [trace0]

    layout = {
        'xaxis': {
            'range': [0, max_range],
           # 'autoscale': False, 
            'zeroline': False,
            'showgrid': False, 
            'showline': False, 
            'ticks': '', 
            'showticklabels': False
        },
        'yaxis': {
            'range': [0, max_range],
            #'autoscale': False, 
            'zeroline': False,
            'showgrid': False, 
            'showline': False, 
            'ticks': '', 
            'showticklabels': False
        },
    'height': 1000, 
     'width':1000,
    'shapes': final_shape_list
    }
    
    fig = {'data': data,
           'layout': layout
            }
    
    
    return fig 