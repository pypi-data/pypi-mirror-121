import numpy as np
import pandas as pd
from PIL import Image

class phot_excel():
    def __init__(self,Image_Path,size = (260,260),Save_Path = 'output.xlsx', Status = True):
        self.size = size
        self.image = Image.open(Image_Path)
        self.save_path = Save_Path
        self.status = Status
        self.Convert()
    
    def coloring(self,val):
        hexval = '#%02x%02x%02x' % val
        return hexval
    
    def Convert(self):

        if self.status:
            print('Started Converting')

        resized_image = self.image.resize(self.size)
        im_data = resized_image.getdata()
        
        color_data = []
        for i in range(self.size[0]*self.size[1]):
            color_data.append(self.coloring(val=im_data[i]))
        
        color_data = np.array(color_data).reshape(self.size)
        
        df = pd.DataFrame(color_data)
        df = df.style.applymap(lambda x: f'background-color: {x} ;color: {x}')
        
        self.Save(data= df)
    
    def Save(self, data):

        if self.status:
            print('Saving')

        data.to_excel(self.save_path,index=False,header=False)
        
        if self.status:
            print('Saved output')
    

