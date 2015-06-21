from vespa.utilities.util import Enum
import math

# if meshtype is hierarchical, posA will be fixed
MeshType = Enum(['dynamic', 'hierarchical'])

# #############################################################################
# ############################ Common Constraint ##############################
# #############################################################################


class Constraint(object):
    """
    Base Constraint Config Object
    """
    def __init__(self, agents, tolerance, meshtype, ndim, *args, **kwargs):
        self.agents = agents
        self.tolerance = tolerance
        self.meshtype = meshtype
        self.ndim = ndim

    def resolve(self, *args, **kwargs):
        """
        resolves the defined constraint and returns the new positions
        the arguments should only be the positional values of the agents
        returns the target position of the agents in the same order as the
        parameters
        """
        raise NotImplementedError

# #############################################################################
# ########################### Distance Constraints ############################
# #############################################################################


class FixedDistance(Constraint):
    def __init__(self, agents, length, tolerance, meshtype, ndim):
        super(FixedDistance, self).__init__(agents, tolerance, meshtype, ndim)
        self.length = length


class FixedDistance1D(FixedDistance):
    def __init__(self, agents, length, tolerance=0, meshtype=MeshType.hierarchical, ndim=1):
        super(FixedDistance1D, self).__init__(agents, length, tolerance, meshtype, ndim)

    def resolve(self, posA, posB):
        if self.meshtype == MeshType.hierarchical:
            diff = posB[0] - posA[0]
            if abs(abs(diff) - self.length) < self.tolerance:
                return posA, posB
            return [posA, [posA[0] + math.copysign(self.length, diff)]]


class FixedDistance2D(FixedDistance):
    def __init__(self, agents, length, tolerance=0, meshtype=MeshType.hierarchical, ndim=2):
        super(FixedDistance2D, self).__init__(agents, length, tolerance, meshtype, ndim)
    
    def resolve(self, posA, posB):
        # maintains relative angle
        if self.meshtype == MeshType.hierarchical:
            lsq = self.length * self.length
            xdiff = float(posB[0] - posA[0])
            ydiff = float(posB[1] - posA[1])
            if abs(lsq - xdiff * ydiff) < self.tolerance * self.tolerance:
                return posA, posB
            theta = (math.atan(ydiff/xdiff) +
                     math.pi/2 - math.copysign(math.pi, xdiff)/2)
            tx = self.length * math.cos(theta)
            ty = self.length * math.sin(theta)
            return posA, [tx, ty]


# #############################################################################
# ################################ Coincident #################################
# #############################################################################

# TODO
