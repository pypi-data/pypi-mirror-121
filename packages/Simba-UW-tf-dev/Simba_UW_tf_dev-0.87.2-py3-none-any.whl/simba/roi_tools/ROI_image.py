import os, glob
import cv2
import pandas as pd
import itertools
import numpy as np
import re
from copy import deepcopy
from simba.roi_tools.ROI_move_shape import move_edge, move_edge_align
from simba.roi_tools.ROI_zoom import zoom_in


class ROI_image_class():
    def __init__(self, config_path, video_path, img_no, colors_dict, master_top_left_x, duplicate_jump_size, line_type, click_sens):
        self.duplicate_jump_size, self.line_type, self.click_sens = duplicate_jump_size, line_type, click_sens,
        self.cap = cv2.VideoCapture(video_path)
        self.video_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.cap.set(1, img_no)
        self.colors = colors_dict
        self.select_color = (128, 128, 128)
        _, self.orig_frame = self.cap.read()
        self.frame_width, self.frame_height = self.orig_frame.shape[0], self.orig_frame.shape[1]
        self.frame_default_loc = (int(master_top_left_x - self.frame_width), 0)
        self.zoomed_img = deepcopy(self.orig_frame)
        self.zoomed_img_ratio = 1
        self.no_shapes = 0
        self.current_zoom = 100
        self.working_frame = deepcopy(self.orig_frame)
        cv2.namedWindow('Define shape', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Define shape', self.frame_default_loc[0], 0)
        cv2.imshow('Define shape', self.working_frame)
        self.out_rectangles = []
        self.out_circles = []
        self.out_polygon = []

    def update_frame_no(self, new_frame_no):
        self.cap.set(1, new_frame_no)
        _, self.working_frame = self.cap.read()
        self.insert_all_ROIs_into_image(change_frame_no=True)

    def draw_rectangle(self, rectangle_info):
        ROI = cv2.selectROI('Define shape', self.working_frame)
        top_left_x,top_left_y = ROI[0], ROI[1]
        width = (abs(ROI[0] - (ROI[2] + ROI[0])))
        height = (abs(ROI[2] - (ROI[3] + ROI[2])))
        bottom_right_x, bottom_right_y = top_left_x + width,  top_left_y + height
        center_tag_loc = (int(top_left_x + width/2), int(top_left_y + height/2))
        br_tag = (int(top_left_x + width), int(top_left_y + height))
        tr_tag = (int(top_left_x + width), int(top_left_y))
        bl_tag = (int(top_left_x), int(top_left_y + height))
        top_tag = (int(top_left_x + width/2), int(top_left_y))
        right_tag = (int(top_left_x + width), int(top_left_y + height/2))
        left_tag = (int(top_left_x), int(top_left_y + height/2))
        bottom_tag = (int(top_left_x + width/2), int(top_left_y + height))
        self.out_rectangles.append({'Video': rectangle_info['Video_name'],
                                    'Shape_type': 'Rectangle',
                                    'Shape_name': rectangle_info['Shape_name'],
                                    'Color name': rectangle_info['Shape_color_name'],
                                    'Color BGR': rectangle_info['Shape_color_BGR'],
                                    'Thickness': rectangle_info['Shape_thickness'],
                                    'Top_left_X': top_left_x,
                                    'Top_left_Y': top_left_y,
                                    'Bottom_right_X': bottom_right_x,
                                    'Bottom_right_Y': bottom_right_y,
                                    'Width': width,
                                    'Height': height,
                                    'Tags': {'Center tag': center_tag_loc,
                                                 'Top left tag': (top_left_x, top_left_y),
                                                 'Bottom right tag': br_tag,
                                                 'Top right tag': tr_tag,
                                                 'Bottom left tag': bl_tag,
                                                 'Top tag': top_tag,
                                                 'Right tag': right_tag,
                                                 'Left tag': left_tag,
                                                 'Bottom tag': bottom_tag},
                                    'Ear_tag_size': int(rectangle_info['Shape_ear_tag_size'])})

        self.insert_all_ROIs_into_image()

    def draw_circle(self, circle_info):
        self.center_status = False
        self.not_done = True

        def draw_circle_callback(event, x, y, flags, param):
            if event == 1:
                if not self.center_status:
                    self.center_X, self.center_Y = int(x), int(y)
                    cv2.circle(self.working_frame, (self.center_X, self.center_Y), int(circle_info['Shape_ear_tag_size']), circle_info['Shape_color_BGR'], -1)
                    self.center_status = True
                    cv2.imshow('Define shape', self.working_frame)
                    cv2.waitKey(1000)
                else:
                    self.border_x, self.border_y = int(x), int(y)
                    self.radius = int((np.sqrt((self.center_X - self.border_x) ** 2 + (self.center_Y - self.border_y) ** 2)))
                    border_tag = (int(self.center_X - self.radius), self.center_Y)
                    self.out_circles.append({'Video': circle_info['Video_name'],
                                             'Shape_type': 'Circle',
                                             'Shape_name': circle_info['Shape_name'],
                                             'Color name': circle_info['Shape_color_name'],
                                             'Color BGR':  circle_info['Shape_color_BGR'],
                                             'Thickness': circle_info['Shape_thickness'],
                                             'Center_X': self.center_X,
                                             'Center_Y': self.center_Y,
                                             'Radius': self.radius,
                                             'Tags': {'Center tag': (self.center_X, self.center_Y),
                                                      'Border tag': border_tag},
                                             'Ear_tag_size': int(circle_info['Shape_ear_tag_size'])})
                    self.insert_all_ROIs_into_image()
                    self.not_done = False

        while True:
            cv2.setMouseCallback('Define shape', draw_circle_callback)
            cv2.waitKey(800)
            if self.not_done == False:
                break

    def draw_polygon(self):
        self.polygon_pts = []
        def polygon_x_y_callback(event, x, y, flags, param):
            if event == 1:
                self.click_loc = (int(x), int(y))
                cv2.circle(self.working_frame, (self.click_loc[0], self.click_loc[1]), self.draw_info['Shape_thickness'], self.draw_info['Shape_color_BGR'], -1)
                self.polygon_pts.append([int(x), int(y)])
                cv2.imshow('Define shape', self.working_frame)
                cv2.waitKey(800)

        def initiate_x_y_callback():
            while True:
                cv2.setMouseCallback('Define shape', polygon_x_y_callback)
                k = cv2.waitKey(20)
                if k==27:
                    break

        initiate_x_y_callback()
        self.polygon_pts = list(k for k, _ in itertools.groupby(self.polygon_pts))  #REMOVES DUPLICATES
        self.polygon_pts = np.array(self.polygon_pts).astype('int32')
        self.poly_center = self.polygon_pts.mean(axis=0)
        self.polygon_pts_dict = {}

        for v, p in enumerate(self.polygon_pts):
            self.polygon_pts_dict['Tag_' + str(v)] = (p[0], p[1])
        self.polygon_pts_dict['Center_tag'] = (int(self.poly_center[0]), int(self.poly_center[1]))

        self.out_polygon.append({'Video': self.draw_info['Video_name'],
                                 'Shape_type': 'Polygon',
                                 'Shape_name': self.draw_info['Shape_name'],
                                 'Color name': self.draw_info['Shape_color_name'],
                                 'Color BGR': self.draw_info['Shape_color_BGR'],
                                 'Thickness': self.draw_info['Shape_thickness'],
                                 'Center_X': int(self.poly_center[0]),
                                 'Center_Y': int(self.poly_center[1]),
                                 'Polygon np.array': self.polygon_pts,
                                 'Tags': self.polygon_pts_dict,
                                 'Ear_tag_size': int(self.draw_info['Shape_ear_tag_size'])})

        self.insert_all_ROIs_into_image()

    def initiate_draw(self, draw_dict):
        self.draw_info = draw_dict
        if self.draw_info['Shape_type'] is 'rectangle':
            self.draw_rectangle(self.draw_info)
        if self.draw_info['Shape_type'] is 'circle':
            self.draw_circle(self.draw_info)
        if self.draw_info['Shape_type'] is 'polygon':
            self.draw_polygon()

        self.all_shape_names = []
        for r in self.out_rectangles:
            self.all_shape_names.append('Rectangle: ' + str(r['Shape_name']))
        for c in self.out_circles:
            self.all_shape_names.append('Circle: ' + str(c['Shape_name']))
        for p in self.out_polygon:
            self.all_shape_names.append('Polygon: ' + str(p['Shape_name']))
        if (len(self.all_shape_names) > 1) and ('None' in self.all_shape_names):
            self.all_shape_names.remove('None')

        return self.all_shape_names

    def interact_functions(self, interact_method, zoom_val = None):
        self.not_done = True

        def get_x_y_callback(event, x, y, flags, param):
            if event == 1:
                self.click_loc = (int(x), int(y))
                self.not_done = False

        def initiate_x_y_callback():
            while True:
                cv2.setMouseCallback('Define shape', get_x_y_callback)
                cv2.waitKey(20)
                if self.not_done == False:
                    break

        def recolor_roi_tags():
            self.not_done = True
            if self.closest_roi['Shape_type'] == 'Rectangle':
                if self.closest_tag == "Center tag":
                    cv2.rectangle(self.working_frame, (self.closest_roi['Top_left_X'], self.closest_roi['Top_left_Y']), (self.closest_roi['Top_left_X'] + self.closest_roi['Width'], self.closest_roi['Top_left_Y'] + self.closest_roi['Height']), self.select_color, self.closest_roi['Thickness'])
                if (self.closest_tag == "Top tag") or (self.closest_tag == "Top left tag") or (self.closest_tag == "Top right tag") :
                    cv2.line(self.working_frame, (self.closest_roi['Top_left_X'], self.closest_roi['Top_left_Y']), (self.closest_roi['Top_left_X'] + self.closest_roi['Width'], self.closest_roi['Top_left_Y']), self.select_color, self.closest_roi['Thickness'])
                if (self.closest_tag == "Bottom tag") or (self.closest_tag == "Bottom left tag") or (self.closest_tag == "Bottom right tag"):
                    cv2.line(self.working_frame, self.closest_roi['Tags']['Bottom left tag'], self.closest_roi['Tags']['Bottom right tag'],self.select_color, self.closest_roi['Thickness'])
                if (self.closest_tag == "Left tag") or (self.closest_tag == "Bottom left tag") or (self.closest_tag == "Top left tag"):
                    cv2.line(self.working_frame, self.closest_roi['Tags']['Top left tag'], self.closest_roi['Tags']['Bottom left tag'],self.select_color, self.closest_roi['Thickness'])
                if (self.closest_tag == "Right tag") or (self.closest_tag == "Top right tag") or (self.closest_tag == "Bottom right tag"):
                    cv2.line(self.working_frame, self.closest_roi['Tags']['Top right tag'], self.closest_roi['Tags']['Bottom right tag'],self.select_color, self.closest_roi['Thickness'])

            if self.closest_roi['Shape_type'] == 'Circle':
                cv2.circle(self.working_frame, (self.closest_roi['Center_X'], self.closest_roi['Center_Y']), self.closest_roi['Radius'], self.select_color, int(self.closest_roi['Thickness']))

            if self.closest_roi['Shape_type'] == 'Polygon':
                if self.closest_tag == 'Center_tag':
                    pts = self.closest_roi['Polygon np.array'].reshape((-1, 1, 2))
                    cv2.polylines(self.working_frame, [pts], True, self.select_color, int(self.closest_roi['Thickness']))
                else:
                    picked_tag_no = int(re.sub("[^0-9]", "", self.closest_tag))
                    border_tag_1, border_tag_2 = 'Tag_' + str(picked_tag_no - 1), 'Tag_' + str(picked_tag_no + 1)
                    if border_tag_1 not in self.closest_roi['Tags']:
                        border_tag_1 = list(self.closest_roi['Tags'].keys())[-1]
                        if border_tag_1 == 'Center_tag':
                            border_tag_1 = list(self.closest_roi['Tags'].keys())[-2]
                    if border_tag_2 not in self.closest_roi['Tags']:
                        border_tag_2 = list(self.closest_roi['Tags'].keys())[0]
                        if border_tag_2 == 'Center_tag':
                            border_tag_2 = list(self.closest_roi['Tags'].keys())[1]
                    cv2.line(self.working_frame, self.closest_roi['Tags'][self.closest_tag], self.closest_roi['Tags'][border_tag_1], self.select_color, self.closest_roi['Thickness'])
                    cv2.line(self.working_frame, self.closest_roi['Tags'][self.closest_tag], self.closest_roi['Tags'][border_tag_2], self.select_color, self.closest_roi['Thickness'])

            cv2.circle(self.working_frame, (self.closest_roi['Tags'][self.closest_tag][0], self.closest_roi['Tags'][self.closest_tag][1]), self.closest_roi['Ear_tag_size'], self.select_color, self.closest_roi['Thickness'])
            cv2.imshow('Define shape', self.working_frame)

        def find_closest_ROI_tag():
            self.closest_roi, self.closest_tag, self.closest_dist = {}, {}, np.inf
            merged_out = self.out_rectangles + self.out_circles + self.out_polygon
            for s in merged_out:
                for t in s['Tags']:
                    dist = int((np.sqrt((self.click_loc[0] - s['Tags'][t][0]) ** 2 + (self.click_loc[1] - s['Tags'][t][1]) ** 2)))
                    if ((not self.closest_roi) and (dist < self.click_sens)) or (dist < self.closest_dist):
                        self.closest_roi, self.closest_tag, self.closest_dist = s, t, dist
            if self.closest_dist is not np.inf:
                recolor_roi_tags()

        def check_if_click_is_tag():
            self.click_roi, self.click_tag, self.click_dist = {}, {}, -np.inf
            merged_out = self.out_rectangles + self.out_circles + self.out_polygon
            merged_out[:] = [d for d in merged_out if d.get('Shape_name') != self.closest_roi['Shape_name']]
            for shape in merged_out:
                for tag in shape['Tags']:
                    distance = int((np.sqrt((self.click_loc[0] - shape['Tags'][tag][0]) ** 2 + (self.click_loc[1] - shape['Tags'][tag][1]) ** 2)))
                    if ((not self.click_roi) and (distance < self.click_sens)) or (distance < self.click_dist):
                            self.click_roi, self.click_tag, self.closest_dist = shape, tag, distance

        if interact_method == 'zoom_home':
            cv2.destroyAllWindows()
            self.zoomed_img = self.orig_frame
            self.current_zoom = 100
            cv2.imshow('Define shape', self.orig_frame)

        if interact_method == 'move_shape':
            self.insert_all_ROIs_into_image(ROI_ear_tags=True)
            initiate_x_y_callback() # get x y loc ROI tag
            find_closest_ROI_tag() # find closest ROI tag to x y loc
            initiate_x_y_callback() # get x y loc for new x y loc
            check_if_click_is_tag()
            if self.click_roi:
                move_edge_align(self.closest_roi, self.closest_tag, self.click_roi, self.click_tag)
            else:
                move_edge(self.closest_roi, self.closest_tag, self.click_loc)
            self.insert_all_ROIs_into_image() #re-insert ROIs

        if (interact_method == 'zoom_in') or (interact_method == 'zoom_out'):
            zoom_in(self, zoom_val)

        if interact_method == None:
            self.insert_all_ROIs_into_image(ROI_ear_tags=False)

    def remove_ROI(self, roi_to_delete):
        if roi_to_delete.startswith('Rectangle'):
            rectangle_name = roi_to_delete.split('Rectangle: ')[1]
            self.out_rectangles[:] = [d for d in self.out_rectangles if d.get('Shape_name') != rectangle_name]
        if roi_to_delete.startswith('Circle'):
            circle_name = roi_to_delete.split('Circle: ')[1]
            self.out_circles[:] = [d for d in self.out_circles if d.get('Shape_name') != circle_name]
        self.insert_all_ROIs_into_image()

    def insert_all_ROIs_into_image(self, ROI_ear_tags = False, change_frame_no = False, show_zoomed_img = False):
        cv2.destroyAllWindows()
        self.no_shapes = 0
        if (change_frame_no is False) and (show_zoomed_img is False):
            self.working_frame = deepcopy(self.orig_frame)

        for e in self.out_rectangles:
            self.no_shapes += 1
            cv2.rectangle(self.working_frame, (e['Top_left_X'], e['Top_left_Y']), (e['Top_left_X'] + e['Width'], e['Top_left_Y'] + e['Height']), self.colors[e['Color name']], int(e['Thickness']), lineType=self.line_type)
            if ROI_ear_tags is True:
                for t in e['Tags']:
                    cv2.circle(self.working_frame, e['Tags'][t], e['Ear_tag_size'], self.colors[e['Color name']], -1)

        for c in self.out_circles:
            self.no_shapes += 1
            cv2.circle(self.working_frame, (c['Center_X'], c['Center_Y']), c['Radius'], c['Color BGR'], int(c['Thickness']), lineType=self.line_type)
            if ROI_ear_tags is True:
                for t in c['Tags']:
                    cv2.circle(self.working_frame, c['Tags'][t], c['Ear_tag_size'], self.colors[c['Color name']], -1)

        for pg in self.out_polygon:
            self.no_shapes += 1
            pts = pg['Polygon np.array'].reshape((-1, 1, 2))
            cv2.polylines(self.working_frame, [pts], True,  pg['Color BGR'], int(pg['Thickness']), lineType=self.line_type)
            if ROI_ear_tags is True:
                for p in pg['Tags']:
                    cv2.circle(self.working_frame, pg['Tags'][p], pg['Ear_tag_size'], self.colors[pg['Color name']], -1)

        cv2.namedWindow('Define shape', cv2.WINDOW_NORMAL)
        cv2.moveWindow('Define shape', self.frame_default_loc[0], 0)
        cv2.imshow('Define shape', self.working_frame)
