import pyzbar.pyzbar as pyzbar
import cv2
from skimage import io

def decodeQrFromImg(im): 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    print 'Type : ', obj.type
    print 'Data : ', obj.data,'\n' 
     
  return decodedObjects

def loadImgFromUrl(url):
    return io.imread(url)
  

  #display(im, decodedObjects)

