#---------------------------#
#ESRGAN_Helper  Library(1.0)#
#___________________________#
#      Dependecies          #
#___________________________#
#Everything Dependency      #
import os                   #
#___________________________#
# Slicer Dependecies        #
import image_slicer         #
from PIL import Image       #
#___________________________#
#ESRGAN Dependecies         #
import cv2                  #
import numpy as np          #
import torch                #
import RRDBNet_arch as arch #
#___________________________#

# image Slicer script to lower amount of crashes (Due to large images)
# takes input folder / output folder / max size of tile dimintions / and format of images
def Slice(inFolder,outFolder,TileDim,formatx):
    #scan input folder
    for root, dirs, files in os.walk(inFolder):
        for file in files:
            #check file extention
            if file.lower().endswith(formatx.lower()):
                #open file as image
                with Image.open(root+file) as img:
                    #print status
                    print('cutting : '+ file)
                    #get image dimintions
                    width, height = img.size
                    #find image size
                    imgSize = width * height
                    #find tile size from tile dimentions
                    TileSize = TileDim * TileDim
                    #check if tile larger than image
                    if TileSize <= imgSize:
                        #if no
                        #then floor devide image size by Tile size 
                        TileNum = imgSize // TileSize
                        #check if number of tiles is even
                        if (TileNum % 2) != 0:
                            #if no
                            #add one
                            TileNum = TileNum + 1
                        #create tiles from image
                        tiles = image_slicer.slice(root+file, TileNum,save=False)
                        #save tiles to output folder
                        image_slicer.save_tiles(tiles, directory=outFolder, prefix=file[0:-4], format=formatx)
                    else:
                        #if image is smaller then tile
                        #move to output folder
                        os.system('cp '+root+file+' '+outFolder)
                    
# ESRGAN function (modified from ESRGAN test.py)
# takes ESRGAN model path/ torch Device ( CPU or CUDA ) / input folder/ output folder/ and format
def ESRGAN(model_path,DEVice,FolderIN,FolderOUT,format1):
    #sets DEVice
    device = torch.device(DEVice)
    #sets up model
    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    model = model.to(device)
    #prints status
    print('Model path {:s}. \nTesting...'.format(model_path))
    #setup index
    idx = 0
    #get files from input folder
    for root, dirs, files in os.walk(FolderIN):
        for file in files:
            #check file extention
            if file.lower().endswith(format1.lower()):
                # add 1 to index:
                idx += 1
                #print file name and number
                print(idx, file)
                #DO ESRGAN
                img = cv2.imread(root+file, cv2.IMREAD_COLOR)
                img = img * 1.0 / 255
                img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
                img_LR = img.unsqueeze(0)
                img_LR = img_LR.to(device)

                with torch.no_grad():
                    output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
                output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
                output = (output * 255.0).round()
                #write upscaled image to output folder
                cv2.imwrite(FolderOUT + file, output)

# image Join script to fix sliced images
# accepts input folder / temp folder / output folder / format
def Join(inFldr,midFldr,outFldr,format1):
    #scan input folder
    for root, dirs, files in os.walk(inFldr):
        for file in files:
            #check format of images
            if file.lower().endswith(format1.lower()):
                #check if named as tile
                if file[-7] != '_' and file[-10] != '_':
                    #if not named like tile copy to output folder
                    os.system('cp '+inFldr+file+' '+outFldr)
                else:
                    #if named like tile
                    #print status
                    print('Stitching image: '+file[0:-10]+' Row: '+ file[-9:-7])
                    #use image magick to combine rows to Temp folder
                    os.system('convert '+inFldr+ file[0:-7] +'_*'+format1+' +append '+midFldr+file[0:-10]+'_LN_'+file[-9:-7]+format1)
    #scan temp folder
    for root2, dirs2, files2 in os.walk(midFldr):
        for file2 in files2:
            #check for row images with 1
            if file2.endswith('_LN_01.png') or file2.endswith('_LN_01.PNG'):
                #print status
                print('Stitching image: ' + file2[0: -10] )
                #use image magick to stitch rows to full image and save to output folder
                os.system('convert '+ midFldr + file2[0:-9]+'LN_*'+format1+' -append ' + outFldr + str(file2[0: -10]) + format1)
                
# Temp Folder System
# Make Temp Folders Script
def TmpFS_Make(direktory):
        #use mkdir to create folders
        os.system('mkdir '+direktory+'/ESRGAN_Helper_TMP/')
        os.system('mkdir '+direktory+'/ESRGAN_Helper_TMP/1')
        os.system('mkdir '+direktory+'/ESRGAN_Helper_TMP/2')
        os.system('mkdir '+direktory+'/ESRGAN_Helper_TMP/3')
        #return list of folders
        midDirlist = [direktory + '/ESRGAN_Helper_TMP/1/', direktory + '/ESRGAN_Helper_TMP/2/', direktory + '/ESRGAN_Helper_TMP/3/']
        return midDirlist
# Clran Temp folders
def TmpFS_Clean(direktory):
        os.system('rm -r '+direktory+'/ESRGAN_Helper_TMP/')
        return 0
