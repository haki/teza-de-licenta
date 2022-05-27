print('Setting UP')
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from sklearn.model_selection import train_test_split
from utlis import *

path = '..\\DataCollected'
data = importDataInfo(path)
print(data.head())

data = balanceData(data, display=True)

imagesPath, steerings = loadData(path, data)

xTrain, xVal, yTrain, yVal = train_test_split(imagesPath, steerings,
                                              test_size=0.2, random_state=10)
print('Total Training Images: ', len(xTrain))
print('Total Validation Images: ', len(xVal))

model = createModel()

history = model.fit(dataGen(xTrain, yTrain, 100, 1),
                    steps_per_epoch=100,
                    epochs=10,
                    validation_data=dataGen(xVal, yVal, 50, 0),
                    validation_steps=50)

model.save('model.h5')
print('Model Saved')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()
