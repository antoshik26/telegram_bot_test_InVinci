import matplotlib.pyplot as plt
from torchvision.utils import draw_bounding_boxes


class VisualisationClass:
    def __init__(self, threshold):
        '''
            Конструктор определяем порог уверености модели в том что она задетектила
            И ширину полосы обрамляемого того что модела задетектила
        '''
        self.predict_scores_threshold = .8
        self.width = 2

    def visualisation(self, predict, image):
        '''
           Рисует рамки
        '''
        #boxes_predict = [draw_bounding_boxes(image_t, boxes=output['boxes'][output['scores'] > self.predict_scores_threshold], width=4), for image_t, output in zip(image, predict)]
        #print(predict)
        #print(type(predict[0]['scores']))
        #print(predict[0]['scores'])
        #score_threshold = .8
        #for i in predict[0]['scores']:
        #    if i > score_threshold:
        #        image = draw_bounding_boxes(image, boxes=predict[0]['boxes'].tolist()[i], width=4)
        #НЕ успел сюда прикрутить лейблы
        boxes_predict = draw_bounding_boxes(image, boxes=predict[0]['boxes'][predict[0]['scores'] > self.predict_scores_threshold], width=2, colors='red')
        #score_threshold = .8
        #dogs_with_boxes = [
        #    draw_bounding_boxes(dog_int, boxes=output['boxes'][output['scores'] > score_threshold], width=4)
        #    for dog_int, output in zip(image, predict)
        #print(type(boxes_predict))
        return boxes_predict

