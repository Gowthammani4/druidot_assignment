import cv2
from pytesseract import pytesseract 
class OCR():
  def __init__(self):
    self.path="Tesseract-OCR\\tesseract.exe"
    pytesseract.tesseract_cmd=self.path

  def extract(self,im):
    pytt=pytesseract.image_to_string(image=im)
    return pytt


