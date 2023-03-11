import requests
import torch
from io import BytesIO
import pandas as pd
import torchvision
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from models.visalisation_predict import VisualisationClass

class model_fastncc(VisualisationClass):
    def __init__(self, threshold, file_name_labels):
        '''
            Конструктор дэтектора
            model Взяли модель fasterrcnn_resnet50_fpn
            device Определили есть ли на машине gpu
            labels Считываем важность пораметров и их название из файла данные заранием рандомом
        '''
        super().__init__(threshold)
        self.weight = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        self.model = models.detection.fasterrcnn_resnet50_fpn(weights=self.weight, pretrained=True)
        self.device = self.device()
        self.labels = self.read_labels(file_name_labels)

    def device(self):
        '''
           поиск gpu на запускаемой машине
        '''
        if (torch.cuda.is_available()):
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')
        return device

    def read_labels(self, file_name_labels):
        '''
           Читаем название labels найденные в интернете (может быть они не верные вовсе)
        '''
        df = pd.read_csv(file_name_labels, index_col='index')
        #print(df)
        return df

    def resize_image(self, x):
        '''
           Трансформация под размеры для того чтобы модель не ваняла
        '''
        transform = self.weight.transforms()
        image = transform(x)
        return image

    def back_tronsfor(self, x):
        '''
            Трансформация под что то
        '''
        transform = torchvision.transforms.ToPILImage()
        img = transform(x)
        #img.show()
        #print(img)
        return img

    def predict(self, x):
        '''
            Считывает с телеграм бота
            Возвращяет картинку на которой отмечено то что нашла модель
            И возвращает результат детектора
        '''
        self.model.eval()
        self.model.to(self.device)
        response = requests.get(x)
        x = Image.open(BytesIO(response.content))
        transform = transforms.Compose([transforms.PILToTensor()])
        torch_image = transform(x)
        x2 = self.resize_image(torch_image)
        x2 = torch.unsqueeze(x2, 0)
        predict = self.model(x2)
        image_predict_tensor = self.visualisation(predict, torch_image)
        image_predict = self.back_tronsfor(image_predict_tensor)
        return predict, image_predict
