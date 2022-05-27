import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os  # os library
import cv2  # opencv library
from datetime import datetime  # datetime library

global imgList, steeringList  # global variables
countFolder = 0  # count for folder
count = 0  # count for image
imgList = []  # list for image
steeringList = []  # list for steering

myDirectory = os.path.join(os.getcwd(), '../DataCollected')  # path to the directory where the data will be stored

while os.path.exists(os.path.join(myDirectory, f'IMG{str(countFolder)}')):  # if the folder exists
    countFolder += 1  # increase the count
newPath = myDirectory + "/IMG" + str(countFolder)  # new path
os.makedirs(newPath)  # create the new path


def saveData(img, steering):  # save the data to the csv file
    global imgList, steeringList  # global variables
    now = datetime.now()  # get the current date and time
    timestamp = str(datetime.timestamp(now)).replace('.', '')  # get the timestamp
    fileName = os.path.join(newPath, f'Image_{timestamp}.jpg')  # file name
    cv2.imwrite(fileName, img)  # save the image
    imgList.append(fileName)  # add the image to the list
    steeringList.append(steering)  # add the steering to the list


def saveLog():  # save the log file with the data
    global imgList, steeringList  # global variables
    rawData = {'Image': imgList,
               'Steering': steeringList}  # create the dataframe
    df = pd.DataFrame(rawData)  # create the dataframe from the data
    df.to_csv(os.path.join(myDirectory, f'log_{str(countFolder)}.csv'), index=False,
              header=False)  # save the dataframe to the csv file
    print('Log Saved')  # print the log saved
    print('Total Images: ', len(imgList))  # print the total images


if __name__ == '__main__':  # if the file is run directly
    cap = cv2.VideoCapture(0)  # create the video capture
    for x in range(10):  # for 10 images
        _, img = cap.read()  # read the image
        saveData(img, 0.5)  # save the data
        cv2.waitKey(1)  # wait for 1 ms
        cv2.imshow("Image", img)  # show the image
    saveLog()  # save the log file
