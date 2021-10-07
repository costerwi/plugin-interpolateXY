"""Define the AFXProcedure class to handle interpolation dialog box events.

Carl Osterwisch, October 2021
"""

__version__ = 1.0

from abaqusGui import *
from abaqusConstants import *

###########################################################################
# Procedure definition
###########################################################################
class interpolationProcedure(AFXProcedure):
    "Class to launch the interpolate GUI"

    def __init__(self, owner):
        AFXProcedure.__init__(self, owner) # Construct the base class.
        cmd = AFXGuiCommand(mode=self,
                objectName='interpolateXY',
                method='pointsFromViewer',
                registerQuery=FALSE)

        self.pointKw1 = AFXObjectKeyword(cmd, 'points', True)

    def getFirstStep(self):
        step = AFXPickStep(self,
                keyword = self.pointKw1,
                prompt = 'Specify an x coordinate',
                entitiesToPick = AFXPickStep.XY_COORDINATE,
                numberToPick = AFXPickStep.ONE, # this seems to be ignored
                )
        return step


###########################################################################
# Register procedure in the toolset
###########################################################################
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()

toolset.registerGuiMenuButton(
        buttonText='Interpolate XYPlot',
        object=interpolationProcedure(toolset),
        kernelInitString='import interpolateXY',
        author='Carl Osterwisch',
        version=str(__version__),
        applicableModules=['Visualization'],
        description='Interpolate to find y values within XYPlot for x value of given coordinates'
        )
