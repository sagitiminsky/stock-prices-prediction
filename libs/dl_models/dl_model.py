import onnxruntime
from keras.models import load_model
import onnx
import keras2onnx

class DLModel:
    def __init__(self,model,config,time_scale):
        self.model=model
        self.onnx_model = None

        self.lib=config['lib'] if 'lib' in config else None
        self.path2model=config['path2model'] if 'path2model' in config else None
        self.version=config['version'] if 'version' in config else None
        self.path2onnx_model = config['path2onnx_model'] if 'path2onnx_model' in config else None
        self.time_scale=time_scale


    def import_onnx_model(self):
        self.onnx_model = onnxruntime.InferenceSession(self.path2onnx_model + self.version+'_'+self.time_scale + '.onnx')

    def export_onnx_model(self):
        onnx_model = keras2onnx.convert_keras(self.model,self.path2model+'/'+self.version+'_'+self.time_scale)
        onnx.save_model(onnx_model, self.path2onnx_model+'/'+ self.version+'_'+self.time_scale)

    def improt_model(self):
        if self.lib=='Keras': self.model=load_model(self.path2model+'/'+self.version+'_'+self.time_scale)

    def export_model(self):
        self.model.save(self.path2model+'/'+self.version+'_'+self.time_scale)
