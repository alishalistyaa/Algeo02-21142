from modules.config import ROOT_DIR
import matplotlib.pyplot as plt
import numpy as np
from zipfile import ZipFile
import cv2
import os
import shutil

def show_image(imgFile):
# Shows image on GUI
    cv2.imshow("image", imgFile)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_image_plt(M):
    # Mengembalikan display image dari Matrix input
    # Kamus
    # Algoritma
    M = M.reshape(256,256) 
    # Reshape diperlukan jika matriks masih berukuran (65536, 1)
    img = plt.imshow(M)
    img.set_cmap('gray')
    plt.axis('off')
    plt.show

def norm(img):
    return (img/255)
    # return (img-np.amin(img)) * (255/(np.amax(img)-np.amin(img)))

# ================================================= #
# FILE PROCESSING #
# ================================================= #

def extract(filename):
    # Unzipping zip files menjadi folder
    dirname = os.path.join(ROOT_DIR, "../out/extracted")
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    with ZipFile(filename, 'r') as zip:
        zip.extractall(dirname)

    # Notifikasi extracting berhasil
    print('Done extracting!')

# From stackoverflow to fixBadZipFiles
# https://stackoverflow.com/questions/4923142/zipfile-cant-handle-some-type-of-zip-data

def fixBadZipfile(zipFile):  
     f = open(zipFile, 'r+b')  
     data = f.read()  
     pos = data.find(b'\x50\x4b\x05\x06') # End of central directory signature  
     if (pos > 0):  
         f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
         f.truncate()  
         f.close()  
     else:  
        pass
         # raise error, file is truncated 

def list_files(filepath, filetype):
    # Mengembalikan array berisi pathfiles
    # Kamus
    paths = []
    # Algoritma
    for root, dirs, files in os.walk(filepath):
        for file in files:
            if file.lower().endswith(filetype.lower()):
                paths.append(os.path.join(root, file))
    return (paths)

def image_to_matrix(dirname):
    # Mengembalikan kumpulan matrix dari folder dataset yang tersedia
    # Kamus
    # P : Array of filepaths
    M = np.array([])
    first = True

    # Algoritma
    P = list_files(dirname, ".jpg")
    for data in P:
        # Konversi image ke matrix
        img = norm(cv2.imread(data, 0))
        resized = cv2.resize(img, (256, 256))
        flat = resized.flatten()  
        if first:
            M = flat.reshape(len(flat), 1)
            first = False
        else:
            M = np.hstack((M, flat.reshape(len(flat), 1)))
    
    return(M)


def image_matrix_file(filename):
    img = norm(cv2.imread(filename, 0))
    resized = cv2.resize(img, (256, 256))
    flat = resized.flatten()
    return flat.reshape(len(flat), 1)