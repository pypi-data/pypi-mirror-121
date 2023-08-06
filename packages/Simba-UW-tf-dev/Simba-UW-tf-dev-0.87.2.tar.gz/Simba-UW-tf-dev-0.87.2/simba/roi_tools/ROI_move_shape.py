import numpy as np
import re

def update_all_tags(closest_roi):
    if closest_roi['Shape_type'] == 'Rectangle':
        closest_roi['Tags']['Center tag'] = (int(closest_roi['Top_left_X'] + closest_roi['Width'] / 2), int(closest_roi['Top_left_Y'] + closest_roi['Height'] / 2))
        closest_roi['Tags']['Top left tag'] = (int(closest_roi['Top_left_X']), int(closest_roi['Top_left_Y']))
        closest_roi['Tags']['Bottom right tag'] = (int(closest_roi['Top_left_X'] + closest_roi['Width']), int(closest_roi['Top_left_Y'] + closest_roi['Height']))
        closest_roi['Tags']['Top right tag'] = (int(closest_roi['Top_left_X'] + closest_roi['Width']), int(closest_roi['Top_left_Y']))
        closest_roi['Tags']['Bottom left tag'] = (int(closest_roi['Top_left_X']), int(closest_roi['Top_left_Y'] + closest_roi['Height']))
        closest_roi['Tags']['Top tag'] = (int(closest_roi['Top_left_X'] + closest_roi['Width'] / 2), int(closest_roi['Top_left_Y']))
        closest_roi['Tags']['Right tag'] = (int(closest_roi['Top_left_X'] + closest_roi['Width']), int(closest_roi['Top_left_Y'] + closest_roi['Height'] / 2))
        closest_roi['Tags']['Left tag'] = (int(closest_roi['Top_left_X']), int(closest_roi['Top_left_Y'] + closest_roi['Height'] / 2))
        closest_roi['Tags']['Bottom tag'] = (int(closest_roi['Top_left_X'] + closest_roi['Width'] / 2), int(closest_roi['Top_left_Y'] + closest_roi['Height']))

    elif closest_roi['Shape_type'] == 'Circle':
        closest_roi['Tags']['Center tag'] = (closest_roi['Center_X'], closest_roi['Center_Y'])
        closest_roi['Tags']['Border tag'] = (int(closest_roi['Center_X'] - closest_roi['Radius']), closest_roi['Center_Y'])

    else:
        pass

    return closest_roi

def move_edge(closest_roi, closest_tag, new_click_loc):

    if closest_roi['Shape_type'] == 'Polygon':
        if closest_tag == 'Center_tag':
            delta_x, delta_y = closest_roi['Center_X'] - new_click_loc[0], closest_roi['Center_Y'] - new_click_loc[1]
            closest_roi['Center_X'], closest_roi['Center_Y'] = new_click_loc[0], new_click_loc[1]
            new_array = np.zeros((0))
            for v in closest_roi['Polygon np.array']:
                new_x = v[0] - delta_x
                new_y = v[1] - delta_y
                new_array = np.concatenate((new_array, np.array([new_x, new_y])), axis=0).astype('int32')
            closest_roi['Polygon np.array'] = np.reshape(new_array, (-1, 2))
            polygon_pts_dict = {}
            for v, p in enumerate(closest_roi['Polygon np.array']):
                polygon_pts_dict['Tag_' + str(v)] = (p[0], p[1])
            polygon_pts_dict['Center_tag'] = (closest_roi['Center_X'], int(closest_roi['Center_Y']))
            closest_roi['Tags'] = polygon_pts_dict

        else:
            tag_ix = int(re.sub("[^0-9]", "", closest_tag))
            closest_roi['Polygon np.array'][tag_ix] = new_click_loc
            closest_roi['Tags'][closest_tag] = new_click_loc
            poly_center = closest_roi['Polygon np.array'].mean(axis=0)
            closest_roi['Tags']['Center_tag'] = (int(poly_center[0]), int(poly_center[1]))
            closest_roi['Center_X'], closest_roi['Center_Y'] = int(poly_center[0]), int(poly_center[1])


    elif closest_roi['Shape_type'] == 'Rectangle':
        if closest_tag == "Right tag":
            closest_roi['Bottom_right_X'] = new_click_loc[0]
            closest_roi['Width'] = closest_roi['Bottom_right_X'] - closest_roi['Top_left_X']
        if closest_tag == "Left tag":
            closest_roi['Top_left_X'] = new_click_loc[0]
            closest_roi['Width'] = closest_roi['Bottom_right_X'] - closest_roi['Top_left_X']
        if closest_tag == "Top tag":
            closest_roi['Top_left_Y'] = new_click_loc[1]
            closest_roi['Height'] = closest_roi['Bottom_right_Y'] - closest_roi['Top_left_Y']
        if closest_tag == "Bottom tag":
            closest_roi['Bottom_right_Y'] = new_click_loc[1]
            closest_roi['Height'] = closest_roi['Bottom_right_Y'] - closest_roi['Top_left_Y']
        if closest_tag == "Top left tag":
            closest_roi['Top_left_X'], closest_roi['Top_left_Y'] = new_click_loc[0], new_click_loc[1]
            closest_roi['Width'] = closest_roi['Bottom_right_X'] - closest_roi['Top_left_X']
            closest_roi['Height'] = closest_roi['Bottom_right_Y'] - closest_roi['Top_left_Y']
        if closest_tag == "Top right tag":
            closest_roi['Bottom_right_X'], closest_roi['Top_left_Y'] = new_click_loc[0], new_click_loc[1]
            closest_roi['Width'] = closest_roi['Bottom_right_X'] - closest_roi['Top_left_X']
            closest_roi['Height'] = closest_roi['Bottom_right_Y'] - closest_roi['Top_left_Y']
        if closest_tag == "Bottom left tag":
            closest_roi['Top_left_X'], closest_roi['Bottom_right_Y'] = new_click_loc[0], new_click_loc[1]
            closest_roi['Width'] = closest_roi['Bottom_right_X'] - closest_roi['Top_left_X']
            closest_roi['Height'] = closest_roi['Bottom_right_Y'] - closest_roi['Top_left_Y']
        if closest_tag == "Bottom right tag":
            closest_roi['Bottom_right_X'], closest_roi['Bottom_right_Y'] = new_click_loc[0], new_click_loc[1]
            closest_roi['Width'] = closest_roi['Bottom_right_X'] - closest_roi['Top_left_X']
            closest_roi['Height'] = closest_roi['Bottom_right_Y'] - closest_roi['Top_left_Y']
        if closest_tag == 'Center tag':
            delta_x, delta_y = closest_roi['Tags']['Center tag'][0] - new_click_loc[0], closest_roi['Tags']['Center tag'][1] - new_click_loc[1]
            closest_roi['Top_left_X'] = closest_roi['Top_left_X'] - delta_x
            closest_roi['Top_left_Y'] = closest_roi['Top_left_Y'] - delta_y
        update_all_tags(closest_roi)

    elif closest_roi['Shape_type'] == 'Circle':
        if closest_tag == "Center tag":
            closest_roi['Center_X'], closest_roi['Center_Y'] = new_click_loc[0], new_click_loc[1]
        if closest_tag == "Border tag":
            closest_roi['Radius'] = int((np.sqrt((closest_roi['Center_X'] - new_click_loc[0]) ** 2 + (closest_roi['Center_Y'] - new_click_loc[1]) ** 2)))
        update_all_tags(closest_roi)

def move_edge_align(move_roi, move_tag, target_roi, target_tag):
    move_cord = target_roi['Tags'][target_tag]
    if move_roi['Shape_type'] == 'Rectangle':
        if move_tag == 'Top left tag':
            move_roi['Top_left_X'] = move_cord[0]
            move_roi['Top_left_Y'] = move_cord[1]
        if move_tag == 'Top tag':
            move_roi['Top_left_X'] = move_cord[0] - int(move_roi['Width'] / 2)
            move_roi['Top_left_Y'] = move_cord[1]
        if move_tag == 'Top right tag':
            move_roi['Top_left_X'] = move_cord[0] - move_roi['Width']
            move_roi['Top_left_Y'] = move_cord[1]
        if move_tag == 'Left tag':
            move_roi['Top_left_X'] = move_cord[0]
            move_roi['Top_left_Y'] = move_cord[1] - int(move_roi['Height'] / 2)
        if move_tag == 'Bottom left tag':
            move_roi['Top_left_X'] = move_cord[0]
            move_roi['Top_left_Y'] = move_cord[1] - int(move_roi['Height'])
        if move_tag == 'Bottom tag':
            move_roi['Top_left_X'] = move_cord[0] - int(move_roi['Width'] / 2)
            move_roi['Top_left_Y'] = move_cord[1] - int(move_roi['Height'])
        if move_tag == 'Bottom right tag':
            move_roi['Top_left_X'] = move_cord[0] - int(move_roi['Width'])
            move_roi['Top_left_Y'] = move_cord[1] - int(move_roi['Height'])
        if move_tag == 'Right tag':
            move_roi['Top_left_X'] = move_cord[0] - int(move_roi['Width'])
            move_roi['Top_left_Y'] = move_cord[1] - int(move_roi['Height'] / 2)
        if move_tag == 'Center tag':
            move_roi['Top_left_X'] = move_cord[0] - int(move_roi['Width'] / 2)
            move_roi['Top_left_Y'] = move_cord[1] - int(move_roi['Height'] / 2)
        update_all_tags(move_roi)

    if move_roi['Shape_type'] == 'Polygon':
        move_roi['Tags'][move_tag] = (move_cord[0], move_cord[1])
        new_array = np.zeros((0))
        for tag in list(move_roi['Tags'].keys())[:-1]:
            new_x = move_roi['Tags'][tag][0]
            new_y = move_roi['Tags'][tag][1]
            new_array = np.concatenate((new_array, np.array([new_x, new_y])), axis=0).astype('int32')
        move_roi['Polygon np.array'] = np.reshape(new_array, (-1, 2))
        poly_center = move_roi['Polygon np.array'].mean(axis=0)
        move_roi['Center_X'], move_roi['Center_Y'] = int(poly_center[0]), int(poly_center[1])

    if move_roi['Shape_type'] == 'Circle':
        if move_tag == 'Center tag':
            move_roi['Center_X'], move_roi['Center_Y'] = move_cord[0], move_cord[1]
        if move_tag == 'Border tag':
            move_roi['Center_X'], move_roi['Center_Y'] = int(move_cord[0] + move_roi['Radius']), move_cord[1]
        update_all_tags(move_roi)





