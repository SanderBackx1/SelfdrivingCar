from fastai.vision.all import *
import pandas as pd
import os



#get images
images = [ f"./data/images/{x}" for x in os.listdir("./data/images")]

#get input data
df_data = pd.read_csv('./data/inputs.csv',names=["img_path", "X", "Y", "Throttle", "Brake"])

#We don't need the input of the Y axis because this doesn't influence the steering of the vehicle
del df_data["Y"]

#Replace None
df_data["X"] = df_data["X"].transform(lambda x: '0' if x == "None" else x)

df_data["X"] = df_data["X"].astype(float) 
df_data["Throttle"] = df_data["Throttle"].astype(float) 
df_data["Brake"] = df_data["Brake"].astype(float) 


x_max = 32767
x_min = -32767
def transformX(x):
  #This removes negative values
  new_x = x + x_max
  new_x = new_x / (x_max+x_max)

  return   new_x 


df_data["X"] = df_data["X"].apply(transformX)
df_data["Throttle"] = df_data["Throttle"].apply(lambda t: t/255*x_min)
df_data["Brake"] = df_data["Brake"].apply(lambda b: b/255*x_max)

df_data["Z"] = df_data["Throttle"] + df_data["Brake"]
df_data["Z"] = df_data["Z"].apply(transformX)

df_final = df_data.copy()
del df_final["Throttle"]
del df_final["Brake"]

def get_x (r): return Path(f"./data/images/{r['img_path']}")
def get_y(r): return [r['X'], r['Z']]


datablock = DataBlock(
                blocks=(ImageBlock,RegressionBlock),
                get_x=get_x,
                get_y=get_y,
                item_tfms=Resize(244, method='squish'),
                splitter=RandomSplitter(valid_pct=0.2, seed=32))

dls = datablock.dataloaders(df_final)
learn = cnn_learner(dls, resnet18, y_range=(-1,1), metrics=mse )
learn = learn.load('racecar')

def getOutput(img):
    return learn.predict(img)




