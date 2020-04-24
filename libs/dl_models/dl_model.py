import onnxruntime
from keras.models import load_model
import onnx
import keras2onnx

class DLModel:
    def __init__(self,model,config):
        self.model=model
        self.onnx_model = None

        self.lib=config['lib'] if 'lib' in config else self.lib=None
        self.path2model=config['path2model'] if 'path2model' in config else self.path2model=None
        self.model_version=config['model_version'] if 'model_version' in config else self.model_version=None
        self.path2onnx_model = config['path2onnx_model'] if 'path2onnx_model' in config else self.path2onnx_model=None
        self.onnx_model_version=config['onnx_model_version'] if 'onnx_model_version' in config else  self.onnx_model_version=None


    def import_onnx_model(self):
        self.onnx_model = onnxruntime.InferenceSession(self.path2onnx_model + self.onnx_model_version + '.onnx')

    def export_onnx_model(self):
        onnx_model = keras2onnx.convert_keras(self.model,self.path2model+'/'+self.model_version)
        onnx.save_model(onnx_model, self.path2onnx_model+'/'+ self.onnx_model_version)

    def improt_model(self):
        if self.lib=='Keras': self.model=load_model(self.path2model+'/'+self.model_version)

    def export_model(self):
        self.model.save(self.path2model+'/'+self.model_version)
