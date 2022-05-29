print('Setting UP')  # Setting up the environment for the program to run in
import os  # Importing the os module to be able to use the os.system function to run the program in the terminal

os.environ[
    'TF_CPP_MIN_LOG_LEVEL'] = '3'  # Setting the environment variable to suppress the warning messages  from the tensorflow library
from sklearn.model_selection import \
    train_test_split  # Importing the train_test_split function from the sklearn library to split the data into training and testing data
from utils import *  # Importing the utils.py file to be able to use the functions in the utils.py file

path = '..\\DataCollected'  # Setting the path to the data collected
data = importDataInfo(path)  # Calling the importDataInfo function to import the data collected
print(data.head())  # Printing the first 5 rows of the data

data = balanceData(data, display=True)  # Calling the balanceData function to balance the data

imagesPath, steerings = loadData(path, data)  # Calling the loadData function to load the data

xTrain, xVal, yTrain, yVal = train_test_split(imagesPath, steerings,
                                              test_size=0.2,
                                              random_state=10)  # Splitting the data into training and testing data
print('Total Training Images: ', len(xTrain))  # Printing the total number of training images
print('Total Validation Images: ', len(xVal))  # Printing the total number of validation images

model = createModel()  # Calling the createModel function to create the model

history = model.fit(dataGen(xTrain, yTrain, 100, 1),
                    steps_per_epoch=100,
                    epochs=10,
                    validation_data=dataGen(xVal, yVal, 50, 0),
                    validation_steps=50)  # Training the model

model.save('model.h5')  # Saving the model
print('Model Saved')  # Printing that the model has been saved

plt.plot(history.history['loss'])  # Plotting the loss function
plt.plot(history.history['val_loss'])  # Plotting the validation loss function
plt.legend(['Training', 'Validation'])  # Labeling the plot
plt.title('Loss')  # Labeling the plot
plt.xlabel('Epoch')  # Labeling the plot
plt.show()  # Showing the plot
