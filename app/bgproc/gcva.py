from models import AnalyzeResult
from .base import BackgroundAnalyzeProcessBase
from google.cloud import vision
from google.oauth2 import service_account
import io
import os

class GcvaAnalyze(BackgroundAnalyzeProcessBase):
    def __init__(self, json_path: str) -> None:
        self.json_path = json_path

    def run(self, image_path: str) -> list[AnalyzeResult]:
        # 身元証明書のjson読み込み(GCVA)
        credentials = service_account.Credentials.from_service_account_file(self.json_path)
        client = vision.ImageAnnotatorClient(credentials=credentials)

        # Loads the image into memory(GCVA)
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file(GCVA)
        response =  client.document_text_detection(
                image=image,
                image_context={'language_hints': ['ja']}
            )
        
        # レスポンスからテキストデータを抽出(GCVA)
        #output_text = ''
        #for page in response.full_text_annotation.pages:
        #    for block in page.blocks:
        #        for paragraph in block.paragraphs:
        #            for word in paragraph.words:
        #                output_text += ''.join([
        #                    symbol.text for symbol in word.symbols
        #                ])
        #            output_text += '\n'
        #print(output_text)

        # レスポンスからテキストの位置座標を抽出(GCVA)
        output=[]
        count=0
        for texts in response.text_annotations:
            vertices = [(vertex.x, vertex.y) for vertex in texts.bounding_poly.vertices]
            x1=min(vertices[0][0],vertices[3][0])
            y1=min(vertices[0][1],vertices[1][1])
            x2=max(vertices[1][0],vertices[2][0])
            y2=max(vertices[2][1],vertices[3][1])
            if count !=0:
                output.append([14,x1,y1,x2,y2])
            count += 1
        return(output)

