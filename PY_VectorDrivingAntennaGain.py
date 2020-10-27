import pickle
import sys
import importlib.util
sys.path.append("C:\\Users\\vlesser\\Desktop\\ansysToStkPython\\ansysToStkPython\\")
from utilities import utils
import numpy as np
import math

global PY_VectorDrivingAntennaGain_init
global PY_VectorDrivingAntennaGain_Inputs
global PY_VectorDrivingAntennaGain_Outputs

print(__name__)

PY_VectorDrivingAntennaGain_init = -1

#==========================================================================
# PY_CalcObject() fctn
#==========================================================================
def PY_VectorDrivingAntennaGain ( argList ):
    callMode = str(argList[0])
    if callMode == 'None' :
        retVal = PY_VectorDrivingAntennaGain_compute( argList )    # do compute
    elif callMode == 'register' :
        global PY_VectorDrivingAntennaGain_init 
        PY_VectorDrivingAntennaGain_init = -1
        retVal = PY_VectorDrivingAntennaGain_register()
    elif callMode == 'compute' :
        retVal = PY_VectorDrivingAntennaGain_compute( argList )    # do compute
    else:
        retVal = []    # # bad call, return empty list
    return retVal

 

def PY_VectorDrivingAntennaGain_register():

 

    return [
        ["ArgumentType = Output", "Name = AntennaGain", "ArgumentName = AntennaGain"],
        ["ArgumentType = Output", "Name = Beamwidth", "ArgumentName = Beamwidth"],
        ["ArgumentType = Output", "Name = AntennaMaxGain", "ArgumentName = AntennaMaxGain"],
        ["ArgumentType = Output", "Name = IntegratedGain", "ArgumentName = IntegratedGain"],
        ["ArgumentType = Output", "Name = AntennaCoordSystem", "ArgumentName = AntennaCoordSystem"],
        ["ArgumentType = Input", "Name = DateUTC", "ArgumentName = DateUTC", "Type = Value"],
        ["ArgumentType = Input", "Name = CbName", "ArgumentName = CbName", "Type = Value"],
        ["ArgumentType = Input", "Name = Frequency", "ArgumentName = Frequency", "Type = Value"],
        ["ArgumentType = Input", "Name = AzimuthAngle", "ArgumentName = AzimuthAngle", "Type = Value"],
        ["ArgumentType = Input", "Name = ElevationAngle", "ArgumentName = ElevationAngle", "Type = Value"],
        ["ArgumentType = Input", "Name = AntennaPosLLA", "ArgumentName = AntennaPosLLA", "Type = Value"],
        ["ArgumentType = Input", "Name = AntennaCoordSystem", "ArgumentName = AntennaCoordSystem", "Type = Value"],
        ["ArgumentType = Input", "Name = DateUTC", "ArgumentName = dateStr"],        
        ["ArgumentType = Output", "Name = DynamicGain", "ArgumentName = Value"]
    ]

 

def PY_VectorDrivingAntennaGain_compute( inputData ):
    # NOTE: argList[0] is the call Mode, which is either None or 'compute'
    global PY_VectorDrivingAntennaGain_init
    global PY_VectorDrivingAntennaGain_Inputs
    if PY_VectorDrivingAntennaGain_init < 0:
        PY_VectorDrivingAntennaGain_init = 1
        PY_VectorDrivingAntennaGain_Inputs = g_PluginArrayInterfaceHash['PY_VectorDrivingAntennaGain_Inputs']
        PY_VectorDrivingAntennaGain_Outputs = g_PluginArrayInterfaceHash['PY_VectorDrivingAntennaGain_Outputs']

    #############################################################################################
    # USER ANTENNA GAIN MODEL AREA.
    # PLEASE REPLACE THE CODE BELOW WITH YOUR ANTENNA GAIN COMPUTATION MODEL
    #############################################################################################
    # NOTE: the outputs that are returned MUST be in the same order as registered
    # AntennaGain (dB), gain of the antenna at time and in the Azi-Elev direction off the boresight.
    # Beamwidth (Rad) is the 3-dB beamwith of the antenna.
    # AntennaMaxGain (dB) is the maximum ( possibly boresight gain of the antenna)
    # IntegratedGain of the antenna (range 0-1) used for antenna Noise computation.
    
    #
    eff = 0.55
    dia = 1.0
    freq = float(inputData[PY_VectorDrivingAntennaGain_Inputs['Frequency']])
    el   = float(inputData[PY_VectorDrivingAntennaGain_Inputs['ElevationAngle']])
    az   = float(inputData[PY_VectorDrivingAntennaGain_Inputs['AzimuthAngle']])
    
    antPos    = inputData[PY_VectorDrivingAntennaGain_Inputs['AntennaPosLLA']]
    antPosLat = antPos[0]
    antPosLon = antPos[1]
    antPosAlt = antPos[2]

    lambda_value = 299792458.0 / freq
    thetab = lambda_value / (dia * math.sqrt(eff))

 

    """""""""""""""""""""
    START OF ANSYS SCRIPT
    """""""""""""""""""""
    
    ##############################################################################
    #
    #   USER INPUTS
    #
    ##############################################################################
    #load results from file, instead of loading them dynamiclaly from HFSS
    load_ffd_from_file=False 

    #Which angle should beam be pointing?
    #This is for testing
    #phi_scan = 90 #defined based on starndard sperical coordinate system
    #theta_scan = 45 

    #path where results and/or project file is stored
    file_path = "C:\\Users\\vlesser\\Desktop\\SSR\\ansysToStkPython\\"
    project_file = "FiniteArray_Radome_77GHz_3D_CADDM.aedt" 
    project_path = file_path + project_file 

    #freq = 77e9 #solution frequency, used for calculating electrical spacing of array
    array_shape = [4,4] #number of elements in x and y direction, assumes no empty cells 

    #these are only needed if load_ff_from_file=False
    solution_setup_name = 'Setup1 : LastAdaptive'
    ff_setup_name = '3D' 

    ##############################################################################
    #
    #   END USER INPUTS
    #
    ##############################################################################
    
    eep_file = project_file.replace('.aedt','.eep') #pre-computed results are stored as .eep file (embedded element patterns)
    if load_ffd_from_file:
        #load all variables stored in .eep file, this included embedded element patterns
        #as well as theta/phi and lattice spacing
        save_results_file = file_path + eep_file
        f = open(save_results_file, 'rb')
        obj = pickle.load(f)
        f.close()
        locals().update(obj)
    else:
        #if loading results dynamically from AEDT, we need to load the 
        #Ansys Automation library
        import sys
        sys.path.insert(0, "C:\\Users\\vlesser\\AnsysAutomation")
        from AEDTLib.Desktop import Desktop
        desktopVersion = "2020.2"
        oDesktop = None
        NonGraphical = False
        NewThread = False
        Desktop(desktopVersion, NewThread, NonGraphical)

        MainModule = sys.modules['__main__']
        oDesktop = MainModule.oDesktop

        #access the active project/design
        oProject = oDesktop.GetActiveProject()
        oDesign = oProject.GetActiveDesign()
        oEditor = oDesign.SetActiveEditor("3D Modeler")
        units = oEditor.GetModelUnits()
        oModelModule = oDesign.GetModule("ModelSetup")

        #get lattice vectors, this tells us the spacing of the array elements
        lattice_vectors = oModelModule.GetLatticeVectors()
        lattice_vectors = [utils.convert_units(vec,units,'meter') for vec in lattice_vectors ]
            
        #get embedded element pattern of each port, on completion this will
        #store all ther results in a pickle that can be loaded in future runs
        #so we don't need to extract eep every time
        all_eep = utils.get_eep(oDesign,setup_name=solution_setup_name,ff_setup=ff_setup_name)
        for_output_save = {}
        for_output_save = {'all_eep':all_eep,
                           'lattice_vectors':lattice_vectors}
        save_results_file = file_path+ eep_file
        f = open(save_results_file, 'wb+')
        pickle.dump(for_output_save, f)
        f.close()

        #call function that will output far field pattern based on user requested
        #phi and theta scan angles
        #loc_offset is used if the array does not start at the edge, for example
        #in this design, the array elements start 2 spaces from the edge, the radome
        #and empty space occupy the first 2 cells. We might be able to figure this out
        #automatically in the future, but for now I am just specifying this value
        all_qtys = utils.ff_beamsteer(all_eep,
                                  lattice_vectors,
                                  freq,
                                  phi_scan=50,
                                  theta_scan=el,
                                  loc_offset=2,
                                  array_shape=array_shape)

        #get embedded element pattern of each port, on completion this will
        #store all ther results in a pickle that can be loaded in future runs
        #so we don't need to extract eep every time
        all_eep = utils.get_eep(oDesign,setup_name=solution_setup_name,ff_setup=ff_setup_name)
        print("Created all_eep")
        for_output_save = {}
        for_output_save = {'all_eep':all_eep,
                           'lattice_vectors':lattice_vectors}
        save_results_file = file_path+ eep_file
        f = open(save_results_file, 'wb+')
        pickle.dump(for_output_save, f)
        f.close()
          
        qty_str = 'RealizedGain'
        gainArray = 10*np.log10(np.abs(all_qtys[qty_str]))    
        #gainArray = np.load("C:\\Users\\vlesser\\Desktop\\SSR\\AnsysScript\\gainArray.npy")    
        azDeg = round(az*(180/math.pi))
        azIndx = round((azDeg)/2)    
        elDeg = round(el*(180/math.pi))
        elIndx = round((elDeg))    
        gain = float(gainArray[azIndx,elIndx])
        
        save_results_file = file_path+ eep_file
        f = open(save_results_file, 'wb+')
        pickle.dump(for_output_save, f)
        f.close()
        #np.abs
        gainArray = str(all_qtys)
        #float(np.max(gainArray))
        gmax = str(all_qtys)
        
        """""""""""""""""""""
        END OF ANSYS SCRIPT
        """""""""""""""""""""
        return [
            thetab,                   # PY_VectorDrivingAntennaGain_Outputs.AntennaGain (returns gain based on azimuth and elevation)
            thetab,                    # PY_VectorDrivingAntennaGain_Outputs.Beamwidth
            thetab,                   # PY_VectorDrivingAntennaGain_Outputs.AntennaMaxGain (taken from Ansys file)
            .5,                    # PY_VectorDrivingAntennaGain_Outputs.IntegratedGain
            0,                        # PY_VectorDrivingAntennaGain_Outputs.AntennaCoordSystem, AntennaCoordSystem return 0 for Polar and 1 for Rectangular
            1,                       #dynamic output
        ]
    
def main():
    print("hello world!")

 

if __name__ == "__main__":
    main()