import os  # for os.path.basename and os.path.dirname functions
import pandas as pd  # for DataFrame and Series objects and read_csv function
import numpy as np  # for ndarray and array functions and constants
import matplotlib.pyplot as plt  # for plot and show functions
from sklearn.utils import shuffle  # for shuffle data in train set and test set
import cv2

from tensorflow.keras.models import Sequential  # for Sequential model
from tensorflow.keras.layers import Convolution2D, Flatten, Dense  # for Convolution2D,Flatten,Dense layers
from tensorflow.keras.optimizers import Adam  # for Adam optimizer

import matplotlib.image as mpimg  # for imread function
from imgaug import augmenters as iaa  # for augmenters

import random  # for random.sample function


def getName(filePath):  # get file name from file path
    myImagePathL = filePath.split('/')[-2:]  # get last two elements of list
    myImagePath = os.path.join(myImagePathL[0], myImagePathL[1])  # join the two elements
    return myImagePath  # return the file name


def importDataInfo(path):  # import data info from csv file
    columns = ['Center', 'Steering']  # define columns of dataframe
    noOfFolders = len(os.listdir(path)) // 2  # get number of folders in the path
    data = pd.DataFrame()  # create dataframe
    for x in range(0, 1):
        dataNew = pd.read_csv(os.path.join(path, f'log_{x}.csv'), names=columns)  # read csv file
        print(f'{x}:{dataNew.shape[0]} ', end='')  # print number of rows in dataframe
        dataNew['Center'] = dataNew['Center'].apply(getName)  # apply getName function to get file name
        data = data.append(dataNew, True)  # append dataframe
    print(' ')  # print space
    print('Total Images Imported', data.shape[0])  # print total number of images imported
    return data  # return dataframe


def balanceData(data, display=True):  # balance data
    nBin = 31  # number of bins
    samplesPerBin = 300  # samples per bin
    hist, bins = np.histogram(data['Steering'], nBin)  # get histogram
    if display:  # if display is true
        center = (bins[:-1] + bins[1:]) * 0.5  # get center of bins
        plt.bar(center, hist, width=0.03)  # plot histogram
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samplesPerBin, samplesPerBin))  # plot line
        plt.title('Data Visualisation')  # plot title
        plt.xlabel('Steering Angle')  # plot x label
        plt.ylabel('No of Samples')
        plt.show()  # show plot
    removeindexList = []  # create empty list
    for j in range(nBin):
        binDataList = []  # create empty list
        for i in range(len(data['Steering'])):
            if data['Steering'][i] >= bins[j] and data['Steering'][i] <= bins[
                j + 1]:  # if steering angle is in bin
                binDataList.append(i)  # append index of data to binDataList
        binDataList = shuffle(binDataList)  # shuffle binDataList
        binDataList = binDataList[samplesPerBin:]  # get last samplesPerBin samples
        removeindexList.extend(binDataList)  # append binDataList to removeindexList

    print('Removed Images:', len(removeindexList))  # print number of removed images
    data.drop(data.index[removeindexList], inplace=True)  # drop rows from dataframe
    print('Remaining Images:', len(data))  # print number of remaining images
    if display:  # if display is true
        hist, _ = np.histogram(data['Steering'], (nBin))  # get histogram
        plt.bar(center, hist, width=0.03)  # plot histogram
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samplesPerBin, samplesPerBin))  # plot line
        plt.title('Balanced Data')  # plot title
        plt.xlabel('Steering Angle')  # plot x label
        plt.ylabel('No of Samples')  # plot y label
        plt.show()  # show plot
    return data  # return dataframe


def loadData(path, data):  # load data
    imagesPath = []  # create empty list
    steering = []  # create empty list
    for i in range(len(data)):
        indexed_data = data.iloc[i]  # get indexed data
        imagesPath.append(os.path.join(path, indexed_data[0]))  # append path to imagesPath
        steering.append(float(indexed_data[1]))  # append steering angle to steering
    imagesPath = np.asarray(imagesPath)  # convert to numpy array
    steering = np.asarray(steering)  # convert to numpy array
    return imagesPath, steering  # return imagesPath and steering


def augmentImage(imgPath, steering):  # augment image
    img = mpimg.imread(imgPath)  # read image
    if np.random.rand() < 0.5:  # if random number is less than 0.5
        pan = iaa.Affine(
            translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)})  # create affine transform  with translation  (x,y)
        img = pan.augment_image(img)  # augment image  with affine transform
    if np.random.rand() < 0.5:  # if random number is less than 0.5
        zoom = iaa.Affine(scale=(1, 1.2))  # create affine transform  with scale
        img = zoom.augment_image(img)  # augment image  with affine transform
    if np.random.rand() < 0.5:  # if random number is less than 0.5
        brightness = iaa.Multiply((0.5, 1.2))  # create brightness transform
        img = brightness.augment_image(img)  # augment image  with brightness transform
    if np.random.rand() < 0.5:  # if random number is less than 0.5
        img = cv2.flip(img, 1)  # flip image horizontally
        steering = -steering  # flip steering angle
    return img, steering  # return image and steering angle


def preProcess(img):  # preprocess image
    img = img[54:120, :, :]  # crop image
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  # convert to YUV color space
    img = cv2.GaussianBlur(img, (3, 3), 0)  # blur image
    img = cv2.resize(img, (200, 66))  # resize image
    img = img / 255  # normalize image
    return img  # return image


def createModel():  # create model
    model = Sequential()  # create sequential model

    model.add(Convolution2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation='elu'))  # add convolution layer
    model.add(Convolution2D(36, (5, 5), (2, 2), activation='elu'))  # add convolution layer
    model.add(Convolution2D(48, (5, 5), (2, 2), activation='elu'))  # add convolution layer
    model.add(Convolution2D(64, (3, 3), activation='elu'))  # add convolution layer
    model.add(Convolution2D(64, (3, 3), activation='elu'))  # add convolution layer

    model.add(Flatten())  # flatten image
    model.add(Dense(100, activation='elu'))  # add dense layer
    model.add(Dense(50, activation='elu'))  # add dense layer
    model.add(Dense(10, activation='elu'))  # add dense layer
    model.add(Dense(1))  # add dense layer

    model.compile(Adam(lr=0.0001), loss='mse')  # compile model
    return model  # return model


def dataGen(imagesPath, steeringList, batchSize, trainFlag):  # data generator
    while True:
        imgBatch = []  # create empty list for images
        steeringBatch = []  # create empty list for steering angles

        for i in range(batchSize):
            index = random.randint(0, len(imagesPath) - 1)  # get random index
            if trainFlag:  # if train flag is true
                img, steering = augmentImage(imagesPath[index],
                                             steeringList[index])  # augment image and steering angle
            else:  # if train flag is false
                img = mpimg.imread(imagesPath[index])  # read image
                steering = steeringList[index]  # get steering angle
            img = preProcess(img)  # preprocess image
            imgBatch.append(img)  # append image to list
            steeringBatch.append(steering)  # append steering angle
        yield (np.asarray(imgBatch), np.asarray(steeringBatch))  # yield images and steering angles
