#!/usr/bin/python3.5.3
# -*-coding:Utf8 -*

from PIL import ImageChops, Image
from io import BytesIO
import picamera,time, os, io

def comparer_deux_images(img1, img2):
# config:
    seuil = 0.10 # seuil en pourcentage , d'une fourchette de tolérance donnée
    tolerance_pixels = 3500 # nb de pixels à considérer différents avant de déclarer 2 images différentes
# init compteur:
    nb_pixels_differents = 0

    for x in range(0, img1.size[0], 4):
        for y in range(0, img1.size[1], 4):
            pxl_img1, pxl_img2 = img1.getpixel((x,y))[0], img2.getpixel((x,y))[0]
            if (pxl_img1 - seuil * pxl_img1) < pxl_img2 and (pxl_img1 + seuil * pxl_img1) > pxl_img2:
                pass
            else:
                nb_pixels_differents +=1

    print("comparer_deux_images , nb_pixels_différents : " , nb_pixels_differents)
    if nb_pixels_differents > tolerance_pixels:
        return False # les images sont jugées différentes
    else:
        return True
def prise_sequence_video(camera):
    t = time.localtime()
    nom_fichier = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + "_" +str(t[3]) + "h" + str(t[4]) + "min" + str(t[5]) + "sec"
    print('enregistrement : debut')
    camera.start_recording("videos/" + nom_fichier + ".h264")
    camera.wait_recording(5)
    camera.stop_recording()
    print('enregistrement : fin')
def main():
# vérification de l'existence d'un repertoire "videos" et création de ce dernier le cas échéant:
    t = time.localtime()
    heure_demarrage = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + "_" +str(t[3]) + "h" + str(t[4]) + "min" + str(t[5]) + "sec"
    if not os.path.exists("videos"):
        os.makedirs("videos")
    with picamera.PiCamera() as c:
       # c.start_preview()
       # time.sleep(3)
        image_precedente, image_actuelle = None, None
        try: 
            while True:
                stream = io.BytesIO()
                print("capture... (tourne depuis " + heure_demarrage + ")")
                c.capture(stream, format='jpeg')
                image_actuelle = Image.open(stream).convert('LA')

                if image_precedente is None: # c'est la 1ere image
                    pass
                else:
                    if not comparer_deux_images(image_actuelle, image_precedente): # les images sont différentes
                        print("mouvement detecté, enregistrement")
                        prise_sequence_video(c)
                        image_actuelle = None
                image_precedente = image_actuelle
        except Exception as e:
            print(e)
        finally:
            print("quitter ... ok")

if __name__ == "__main__":
    main()