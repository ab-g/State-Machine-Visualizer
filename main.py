import sys
import subprocess
import random
from manu.fn import *


def generate_colors(num_colors):
    colors = []
    i = 0
    while i < 360:
        hue = i
        saturation = 90 + random.uniform(0, 1) * 10
        lightness = 50 + random.uniform(0, 1) * 10
        colors.append('{} {} {}'.format(hue / 360, saturation / 100, lightness / 100))
        i += 360 / num_colors
    return colors


def main(game_project_dir_path, output_folder):
    result = '''digraph state_machine {
    
    overlap = scale;
    
    //overlap = false;
    //splines = true;
    
    rankdir=LR;
    node [shape = circle];
'''

    resource_pack_file_path = os.path.join(game_project_dir_path, 'resource-pack.json')
    with open(resource_pack_file_path, 'r') as resource_pack_file:
        resource_pack_data = json.load(resource_pack_file)

    state_machine_id = get_first_state_machine_id_from_resource_pack_data(resource_pack_data)
    state_machine_file_path = os.path.join(game_project_dir_path, 'state-machines/{0}.json'.format(state_machine_id))

    with open(state_machine_file_path, 'r') as state_machine_file:
        state_machine_data = json.load(state_machine_file)

        colors = generate_colors(len(state_machine_data['states']))
        color_index = 0

        state_colors = {}
        for state_machine_state in state_machine_data['states']:
            state_id = state_machine_state['id']['uuid']

            state_colors[state_id] = {}
            # state_colors[state_id]['in'] = '{} {} {}'.format(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
            # state_colors[state_id]['out'] = '{} {} {}'.format(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

            state_colors[state_id]['in'] = colors[color_index]
            color_index = (color_index + 1) % len(colors)

            node_label = '<f0> {}'.format(state_machine_state['displayName'])
            for action in state_machine_state['actions']:
                if 'StateMachineJumpWallForwardDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineJumpWallDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineTurnAroundDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineMoveAirDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineWallHangDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineTimelineAction' == action['@class']:
                    pass
                elif 'StateMachineLadderReleaseTopDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineLadderReleaseDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineMoveDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineStandUpDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineRotateOnSlidingWayDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineLadderMoveDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineSitDownDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineLadderReleaseBottomDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineLadderGrabDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineJumpAirDelegatorAction' == action['@class']:
                    pass
                elif 'StateMachineJumpDelegatorAction' == action['@class']:
                    pass
                else:
                    property_value = action['propertyValue']
                    if isinstance(property_value, dict):
                        property_value = ', '.join([str(num) for num in property_value['values']])
                    node_label += ' | {} = {}'.format(action['propertyName'], property_value)
            result += '''
    "{}" [
        label = "{}"
        shape = "record"
        style="filled"
        color = "{}"
    ];'''.format(state_machine_state['displayName'], node_label, state_colors[state_id]['in'])

        for transition in state_machine_data['behavior']['transitions']:
            source_state = get_state_data_by_id_from_state_machine_data(state_machine_data, transition['source_id']['uuid'])
            destination_state = get_state_data_by_id_from_state_machine_data(state_machine_data, transition['dest_id']['uuid'])

            edge_label = ''
            if len(transition['test']) == 0:
                '''
                {
                    "@class": "StateMachineTransition",
                    "duration": 0,
                    "offset": 0,
                    "source_id": {
                        "uuid": "BDA0A102-47A7-404F-8480-3EA07A28F57F"
                    },
                    "dest_id": {
                        "uuid": "FA8273DF-B54E-401B-B8BC-B56ABC0D3F01"
                    },
                    "test": {}
                },
                '''
                pass
            elif 'StateMachineBoolPropertyTransitionTest' == transition['test']['@class']:
                '''
                {
                    "@class": "StateMachineTransition",
                    "duration": 0,
                    "offset": 0,
                    "source_id": {
                        "uuid": "E78282D1-257E-4D8B-8522-C36276638C6C"
                    },
                    "dest_id": {
                        "uuid": "FA8273DF-B54E-401B-B8BC-B56ABC0D3F01"
                    },
                    "test": {
                        "@class": "StateMachineBoolPropertyTransitionTest",
                        "propertyName": "PI_Landed",
                        "comparator": "equal",
                        "propertyValue": false
                    }
                },
                '''
                edge_label += '{} {} {}'.format(transition['test']['propertyName'], transition['test']['comparator'], transition['test']['propertyValue'])
            elif 'StateMachineTransitionTestContainer' == transition['test']['@class']:
                for test in transition['test']['tests']:
                    if len(edge_label) != 0:
                        edge_label += '\\n'
                    if 'StateMachineAtLadderTopTransitionTest' == test['@class'] or 'StateMachineAtLadderBottomTransitionTest' == test['@class']:
                        edge_label += 'isInvertedTest: {}'.format(test['isInvertedTest'])
                        pass
                    elif 'StateMachineIsRunningTransitionTest' == test['@class']:
                        edge_label += 'running: {}'.format(test['running'])
                    elif 'StateMachineCanStandUpTransitionTest' == test['@class'] or 'StateMachineCanLadderReleaseTransitionTest' == test['@class']:
                        pass
                    else:
                        edge_label += '{} {} {}'.format(test['propertyName'], test['comparator'], test['propertyValue'])

                # edge_label = ''

                # edge_color = '{};0.5:{}'.format(state_colors[source_state['id']['uuid']]['out'], state_colors[destination_state['id']['uuid']]['in'])
                # edge_color = '{} {} {}'.format(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
                edge_color = '{}'.format(state_colors[destination_state['id']['uuid']]['in'])
                # edge_color = 'black'

                result += '\t"{}" -> "{}" [label = "{}" color="{}"];\n'.format(source_state['displayName'], destination_state['displayName'], edge_label, edge_color)

    result += '}'
    print(result)

    layouts = ['dot', 'neato', 'twopi', 'circo', 'fdp', 'osage', 'patchwork', 'sfdp']
    for layout in layouts:
        with open('{}/sm-{}.png'.format(output_folder, layout), "w") as out_file:
            cmd = [layout, '-Tpng']
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, encoding='utf8', stdout=out_file)
            proc.communicate(result)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
