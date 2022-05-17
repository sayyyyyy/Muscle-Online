# import cv2
# from unittest import result
# from numpy import imag
# import mediapipe as mp
# import os


# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         self.mp_pose = mp.solutions.pose
#         self.pose = self.mp_pose.Pose()
#         self.mp_drawing = mp.solutions.drawing_utils
#         self.mp_pose = mp.solutions.pose

#         # Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         ret,frame = self.video.read()
#         #image = run_web.run(image)
#         frame = cv2.flip(frame,1)
#         image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False
#         results = self.pose.process(image)
#         image.flags.writeable = True
#         image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
#         image_width = image.shape[0]
#         image_height = image.shape[1]
#         self.mp_drawing.draw_landmarks(
#         image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

#         ret, jpeg = cv2.imencode('.jpg', image)
        
#         return jpeg.tobytes()

#         # read()は、二つの値を返すので、success, imageの2つ変数で受けています。
#         # OpencVはデフォルトでは raw imagesなので JPEGに変換
#         # ファイルに保存する場合はimwriteを使用、メモリ上に格納したい時はimencodeを使用
#         # cv2.imencode() は numpy.ndarray() を返すので .tobytes() で bytes 型に変換

