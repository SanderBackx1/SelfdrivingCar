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

imagelist = [x[14:]for x in images]
df_final_removed = df_final[df_final['img_path'].isin(imagelist)]
df_final_removed = df_final_removed.drop_duplicates(subset=['img_path'], keep='last')

def get_x (r): return Path(f"./data/images/{r['img_path']}")
def get_y(r): return [r['X'], r['Z']]


##RDP
df_rdp = pd.read_csv('./data/inputs2.csv',names=["img_path", "speed", "steer", "accel", "brake"])
df_rdp["steer"] = df_rdp["steer"].transform(lambda x: '0' if x == "None" else x)
df_rdp['steer'] = df_rdp['steer'].apply(lambda x: (float(x)+255)/512)
df_rdp['accel'] = df_rdp['accel'].apply(lambda x: float(x)/255)
df_rdp['brake'] = df_rdp['brake'].apply(lambda x: float(x)/255)
def get_y_rdp(r): return [r['steer'], r['accel'], r['brake']]




datablock = DataBlock(
                blocks=(ImageBlock,RegressionBlock),
                get_x=get_x,
                get_y=get_y,
                item_tfms=Resize((277,480), method='squish'),
                splitter=RandomSplitter(valid_pct=0.2, seed=32))

dls = datablock.dataloaders(df_data)
learn = cnn_learner(dls, resnet50, y_range=(0,1), metrics=mse )
learn = learn.load('roimodel23')

def getOutput(img):
    return learn.predict(img)




