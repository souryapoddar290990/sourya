import cv2
import webbrowser
import time
import numpy as np
import matplotlib.pyplot as plt
from iplotter import C3Plotter
from scipy.cluster import hierarchy
from scipy.spatial import distance

class LeafCam():

    def __init__(self):
        self.camera_width = 0
        self.camera_height = 0
        self.camera_frame_rate = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.threshold_motion = []
        self.contour_motion = []
        self.max_area_motion = []
        self.total_area_motion = []
        self.frame_number = []
        self.time_frame_buffer = 25
        self.cluster_distance = 200

    def set_cam_details(self,input_path):
        cam = cv2.VideoCapture(input_path)
        grabbed,frame = cam.read()
        self.camera_width = int(cam.get(3))
        self.camera_height = int(cam.get(4))
        try:
            self.camera_frame_rate = int(cam.get(5))
        except:
            # self.camera_frame_rate = 10
            self.camera_frame_rate = self.get_frame_rate(input_path)
        print self.camera_height,self.camera_width,self.camera_frame_rate

    def get_frame_rate(self,input_path):
        cam = cv2.VideoCapture(input_path)
        grabbed,frame = cam.read()
        count = 0
        start_time = time.time()
        while count < 1800:
            frame = cam.read()[1]
            count += 1
        end_time = time.time()
        return int(1800/(end_time-start_time))

    def main(self,input_path):
        cam = cv2.VideoCapture(input_path)
        grabbed,frame = cam.read()
        avg = np.float32(frame)
        threshold_motion,contour_motion,max_area_motion,total_area_motion,frame_number,frame_count = [],[],[],[],[],0
        while True:
            if frame_count%300 == 0: print frame_count/600.0
            grabbed,frame = cam.read()
            if grabbed == False: break
            max_area,total_area = 0,0
            frame_count += 1
            frame_number.append(frame_count)
            cv2.accumulateWeighted(frame,avg,0.1)
            res = cv2.convertScaleAbs(avg)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            firstFrame = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)    
            frameDelta = cv2.absdiff(firstFrame, gray)
            count = int(cv2.norm(firstFrame,gray,cv2.NORM_L1))
            if count/(cam.get(3)*cam.get(4)) > 1:
                # print "motion"
                threshold_motion.append(1)
            else:
                # print ""
                threshold_motion.append(0) 
            thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
            contour_motion.append(len(cnts))
            for c in cnts:
                contour_area = cv2.contourArea(c)
                total_area += contour_area
                if contour_area > max_area:
                    max_area = contour_area
            max_area_motion.append(max_area)
            total_area_motion.append(total_area)
            # cv2.imshow('img',frameDelta)
            # cv2.imshow('avg',res)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cam.release()
        cv2.destroyAllWindows()
        return threshold_motion,contour_motion,max_area_motion,total_area_motion,frame_number

    def save_video(self,seconds,input_path,output_path):
        camera = cv2.VideoCapture(input_path)
        out = cv2.VideoWriter(output_path, self.fourcc, self.camera_frame_rate, (self.camera_width,self.camera_height))
        counter = self.seconds*self.camera_frame_rate
        while counter > 0:
            print counter
            frame = camera.read()[1]
            out.write(frame)
            counter -= 1
        out.release()

    def view_video(self,input_path):
        cam = cv2.VideoCapture(input_path)
        while True:
            frame = cam.read()[1]
            cv2.imshow('Feed',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        cam.release()
        cv2.destroyAllWindows()

    def analysis(self,input_path):
        # cam = cv2.VideoCapture(input_path)
        self.threshold_motion,self.contour_motion,self.max_area_motion,self.total_area_motion,self.frame_number = self.main(input_path)
        fig = plt.figure()
        # plt.subplot(4, 1, 1)
        # plt.ylim((0,1.2))
        # plt.plot(self.frame_number,self.threshold_motion)
        # plt.subplot(4, 1, 2)
        # plt.plot(self.frame_number,self.contour_motion)
        # plt.subplot(4, 1, 3)
        # plt.plot(self.frame_number,self.max_area_motion)
        # plt.subplot(4, 1, 4)
        # plt.plot(self.frame_number,self.total_area_motion)
        # plt.show()

    def plot_chart1(self,file_name,display):
        data1,data2,data3,data4 = ['threshold_motion'],['contour_motion'],['max_area_motion'],['total_area_motion']

        for index in range(len(self.threshold_motion)):
            data1.append(self.threshold_motion[index])
            data2.append(self.contour_motion[index]>0)
            data3.append(self.max_area_motion[index]/1000)
            data4.append(self.total_area_motion[index]/1000)

        chart1 = {
            "data": {
                "columns": [data1,data2,data3,data4],
                "types": {
                    "data1": 'area-spline',
                    "data2": 'area-spline',
                    "data3": 'area-spline',
                    "data4": 'area-spline'
                },
            }
        }

        plotter = C3Plotter()
        plotter.plot_and_save(chart1,filename=file_name)
        if display == 1: webbrowser.open(file_name+'.html')

    def plot_chart2(self,file_name,display):
        data = ['Decision_Value']

        for index in range(len(self.threshold_motion)):
            # print self.threshold_motion[index]*(self.contour_motion[index]>0)*(self.max_area_motion[index]/1000)*(self.total_area_motion[index]/1000)
            data.append(self.threshold_motion[index]*(self.contour_motion[index]>0)*max((self.max_area_motion[index]/1000),(self.total_area_motion[index]/1000)))

        chart2 = {
            "data": {
                "columns": [data],
                "types": {
                    "data": 'area-spline'
                },
            }
        }

        plotter = C3Plotter()
        plotter.plot_and_save(chart2,filename=file_name)
        if display == 1: webbrowser.open(file_name+'.html')

    def get_cluster(self,cluster_data):
        cluster_value = []
        for index in range(len(cluster_data)):
            if cluster_data[index] == True:
                cluster_value.append(index)

        dimension = len(cluster_value)
        distance_matrix=[[0 for row in range(dimension)] for col in range(dimension)]
        for row in range(dimension):
            for col in range(dimension):
                distance_matrix[row][col]=abs(cluster_value[row]-cluster_value[col])
        distance_array = distance.squareform(distance_matrix)
        clusters=hierarchy.linkage(distance_array, method='weighted', metric='euclidean')
        T = hierarchy.fcluster(clusters, self.cluster_distance, criterion='distance')
        temp_holder = {}
        for item in range(max(T)):
            temp_holder[item+1] = []

        for index in range(dimension):
            temp_holder[T[index]].append(cluster_value[index])

        # print temp_holder
        # print T
        # print cluster_value
        return temp_holder

    def save_video_clip(input_path,output_path,clip_number,start_frame,stop_frame):
        camera = cv2.VideoCapture(input_path)
        out = cv2.VideoWriter(output_path+str(clip_number)+'.avi', self.fourcc, self.camera_frame_rate, (self.camera_width,self.camera_height))
        counter = 0
        frame_range = range(start_frame,stop_frame)
        while counter < stop_frame:
            grabbed,frame = camera.read()
            # print counter,grabbed	
            if counter in frame_range:
                out.write(frame)
            counter += 1
        out.release()

    def cluster_level1(output_path):
        cluster_value = []
        for index in range(len(self.threshold_motion)):
            # cluster_value.append((threshold_motion[index]+(contour_motion[index]>0)+(max_area_motion[index]/1000>0)+(total_area_motion[index]/1000>0))>3)
            cluster_value.append((threshold_motion[index]*(contour_motion[index]>0)*max((max_area_motion[index]/1000),(total_area_motion[index]/1000))>1))

        clustered_data = self.get_cluster(cluster_value)

        result = []
        for item in clustered_data:
            start_frame,stop_frame = max(0,min(clustered_data[item])-self.time_frame_buffer),min(max(clustered_data[item])+self.time_frame_buffer,len(threshold_motion))
            # start_frame,stop_frame = min(clustered_data[item]),max(clustered_data[item])
            # print start_frame,stop_frame
            result.append([start_frame,stop_frame])
            # self.save_video_clip(output_path,item,start_frame,stop_frame,camera_width,camera_height,camera_frame_rate,fourcc)
        return result

    def cluster_level2(output_path):
        cluster_data = self.cluster_level1(output_path)
        all_outcome = range(dimension)
        cluster_value = [0]*dimension
        for item in cluster_data:
            temp = [0]*dimension
            for ind in range(item[0],item[1]): temp[ind] = 1
            cluster_value = [x|y for x,y in zip(cluster_value,temp)]

        clustered_data = self.get_cluster(cluster_value)
        for index,item in enumerate(clustered_data):
            start_frame,stop_frame = min(clustered_data[item]),max(clustered_data[item])
            # print start_frame,stop_frame
            save_video_clip(output_path,index,start_frame,stop_frame,camera_width,camera_height,camera_frame_rate,fourcc)

# if __name__ == '__main__':
	# start = time.time()
	# lc = LeafCam()
	# lc.set_cam_details('http://192.168.0.205/videostream.cgi?loginuse=admin&loginpas=admin')
	# end = time.time()

cam = cv2.VideoCapture('video5\output_video_clip_1.avi')
while True:
	grabbed,frame = cam.read()
	cv2.imshow('',frame)
	if cv2.waitKey(50) & 0xFF == ord("q"):
		cv2.imwrite('a.jpg',frame)
		break

