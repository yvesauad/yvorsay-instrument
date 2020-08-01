import sys
import numpy
#from nionswift_plugin.eels_analysis import AlignZLP


__author__ = "Yves Auad"


def _isPython3():
    return sys.version_info[0] >= 3

def SENDMYMESSAGEFUNC(sendmessagefunc):
    return sendmessagefunc

class gainData:

    def __init__(self, sendmessage):
        self.sendmessage=sendmessage


    def send_raw_MetaData(self, rd):
        index = [] #max position for alignment
        array = [0] * len(rd[0][0].data[0])
        temp_data =  [array] * len(rd)


        for i in range(len(rd)):
            for j in range(len(rd[i])):
                cam_hor = numpy.sum(rd[i][j].data, axis=0)
                index.append(numpy.where(cam_hor==numpy.max(cam_hor))[0][0]) #double [0] is because each numpy.where is a array of values. We dont want to have two maximums because aligning will be messy. Remember that we dont expect two maximuns in a ZLP that aren't pixels close together (probably neighbour)
                cam_hor = numpy.roll(cam_hor, -index[len(index)-1]+index[0])
                temp_data[i] = temp_data[i] + cam_hor

        temp_data = numpy.asarray(temp_data) #need this because nion gets some numpy array atributes, such as .shape
        return temp_data, index[0]

    def data_item_calibration(self, ic, dc, start_wav, step_wav, disp, index_zlp):
        ic.units='counts'
        dc[0].units='nm'
        dc[0].offset=start_wav
        dc[0].scale=step_wav
        dc[1].units='eV'
        dc[1].scale=disp
        dc[1].offset=-disp*index_zlp
        intensity_calibration = ic
        dimensional_calibrations = dc
        return intensity_calibration, dimensional_calibrations

    def send_info_data(self, info_data):
        temp_wl_data=[]
        temp_pw_data=[]
        temp_di_data=[]
        for i in range(len(info_data)):
            for j in range(len(info_data[i])):
                temp_wl_data.append(info_data[i][j][0])
                temp_pw_data.append(info_data[i][j][1])
                temp_di_data.append(info_data[i][j][2])
        temp_wl_data = numpy.asarray(temp_wl_data)
        temp_pw_data = numpy.asarray(temp_pw_data)
        temp_di_data = numpy.asarray(temp_di_data)
        return temp_wl_data, temp_pw_data, temp_di_data
