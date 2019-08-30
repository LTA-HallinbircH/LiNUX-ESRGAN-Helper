import ESRGAN_Helper
import os
#ESRGAN_Helper by e[Li]THIA_HallinbircH
#
#
#
#!CONFIG!#
#option to clear temp folder when done
ClearTmpFS = 0 # 0 : no / 1 : yes
#Format of images
formatx='.png'
formatxnodot='png'
#!Folders!#
#input folder (trailing '/' required)
InputFolder = './LR/'
#output folder (trailing '/' required)
OutputFolder = './Result/'
#where temp folder will be made (trailing '/' required)
TmpFSParent = './'
#!End_Folders!#
#!Torch_Options!#
EModelPath = './models/ESRGAN.pth'
TorchDevice = 'cpu'#cpu or cuda
#!End_Torch_Options!#
#!Image_Split_Options!#
SplitSize = 255
#!End_Image_Split_Options!#
#!End_Config!#
#
#
#

#main program
if os.path.exists('./Done.xao') != True:
    #Get Temp folder paths
    MidFldrs = ESRGAN_Helper.TmpFS_Make(TmpFSParent)
    SplitFolder = MidFldrs[0]  
    SplitUpscaleFolder = MidFldrs[1]
    JoinRowFolder = MidFldrs[2]
    #Check status of Sliced images
    if os.path.exists('./SlicedAlready.xao') != True:
        #slice images
        ESRGAN_Helper.Slice(InputFolder,SplitFolder, SplitSize,formatxnodot)
        #write status file
        f= open("./SlicedAlready.xao","w+")
        f.close()
    #remove already upscaled files
    for root, dirs, files in os.walk(SplitUpscaleFolder):
        for filez in files:
            if os.path.exists(SplitFolder+filez) == True:
                os.system('rm '+SplitFolder+filez+' ')
                print(SplitFolder+filez+ ' Found And Removed!')
            else:
                print(SplitFolder+filez+ ' Not Found!')
    #upscale split images
    ESRGAN_Helper.ESRGAN(EModelPath,TorchDevice,SplitFolder,SplitUpscaleFolder,formatx)
    #check status of Joined images
    if os.path.exists('./JoinAlready.xao') != True:
        #join images
        ESRGAN_Helper.Join(SplitUpscaleFolder,JoinRowFolder,OutputFolder,formatx)
        #write status file
        f = open("./JoinAlready.xao","w+")
        f.close()
    #Check Clear TmpFS Setting
    if ClearTmpFS == 1:
        #clear Temp folders
        ESRGAN_Helper.TmpFS_Clean(1,TmpFSParent)
    f = open('./Done.xao','w+')
    f.close()
#cleanup
else:
    print('Cleaning up')
    os.remove("./Done.xao")
    os.remove("./JoinAlready.xao")
    os.remove("./SlicedAlready.xao")
    if (os.path.exists("./Done.xao") != True) and (os.path.exists("./JoinAlready.xao") != True) and (os.path.exists("./SlicedAlready.xao") != True):
        print('CLEAN now restart script')
        input('press enter to finish')
    else:
        input('SCREW LOOSE SOMEWHERE : 005 : Files not removed sucsesfully')
