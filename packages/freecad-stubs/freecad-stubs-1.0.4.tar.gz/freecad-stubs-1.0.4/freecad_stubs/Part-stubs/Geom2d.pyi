import typing

import FreeCAD
import Part
import Part.Geom2d


# Curve2dPy.xml
class Curve2d(Part.Geom2d.Geometry2d):
    """The abstract class Geom2dCurve is the root class of all curve objects."""

    @property
    def Closed(self) -> bool:
        """Returns true if the curve is closed."""

    @property
    def Continuity(self) -> str:
        """Returns the global continuity of the curve."""

    @property
    def FirstParameter(self) -> float:
        """Returns the value of the first parameter."""

    @property
    def LastParameter(self) -> float:
        """Returns the value of the last parameter."""

    @property
    def Periodic(self) -> bool:
        """Returns true if the curve is periodic."""

    def approximateBSpline(self, Tolerance: float, MaxSegments: int, MaxDegree: int, Order: str = 'C2', /):
        """
        Approximates a curve of any type to a B-Spline curve
        					approximateBSpline(Tolerance, MaxSegments, MaxDegree, [Order='C2']) -> B-Spline curve
        """

    def centerOfCurvature(self, float_pos: float, /):
        """Vector = centerOfCurvature(float pos) - Get the center of curvature at the given parameter [First|Last] if defined"""

    def curvature(self, pos: float, /):
        """Float = curvature(pos) - Get the curvature at the given parameter [First|Last] if defined"""

    @typing.overload
    def discretize(self, Number: int, First: float = None, Last: float = None): ...

    @typing.overload
    def discretize(self, Distance: float, First: float = None, Last: float = None): ...

    @typing.overload
    def discretize(self, Deflection: float, First: float = None, Last: float = None): ...

    @typing.overload
    def discretize(self, QuasiNumber: int, First: float = None, Last: float = None): ...

    @typing.overload
    def discretize(self, QuasiDeflection: float, First: float = None, Last: float = None):
        """
        Discretizes the curve and returns a list of points.
        The function accepts keywords as argument:
        discretize(Number=n) => gives a list of 'n' equidistant points
        discretize(QuasiNumber=n) => gives a list of 'n' quasi equidistant points (is faster than the method above)
        discretize(Distance=d) => gives a list of equidistant points with distance 'd'
        discretize(Deflection=d) => gives a list of points with a maximum deflection 'd' to the curve
        discretize(QuasiDeflection=d) => gives a list of points with a maximum deflection 'd' to the curve (faster)
        discretize(Angular=a,Curvature=c,[Minimum=m]) => gives a list of points with an angular deflection of 'a'
                                            and a curvature deflection of 'c'. Optionally a minimum number of points
                                            can be set which by default is set to 2.

        Optionally you can set the keywords 'First' and 'Last' to define a sub-range of the parameter range
        of the curve.

        If no keyword is given then it depends on whether the argument is an int or float.
        If it's an int then the behaviour is as if using the keyword 'Number', if it's float
        then the behaviour is as if using the keyword 'Distance'.

        Example:

        import Part
        c=PartGeom2d.Circle2d()
        c.Radius=5
        p=c.discretize(Number=50,First=3.14)
        s=Part.Compound([Part.Vertex(i) for i in p])
        Part.show(s)


        p=c.discretize(Angular=0.09,Curvature=0.01,Last=3.14,Minimum=100)
        s=Part.Compound([Part.Vertex(i) for i in p])
        Part.show(s)
        """

    def intersectCC(self, arg1: Part.Geom2d.Curve2d, arg2: float = None, /):
        """Returns all intersection points between this curve and the given curve."""

    def length(self, uMin: float = None, uMax: float = None, Tol: float = None, /):
        """
        Computes the length of a curve
        length([uMin,uMax,Tol]) -> Float
        """

    def normal(self, pos: float, /):
        """Vector = normal(pos) - Get the normal vector at the given parameter [First|Last] if defined"""

    def parameter(self, arg1: object, /):
        """
        Returns the parameter on the curve
        of the nearest orthogonal projection of the point.
        """

    def parameterAtDistance(self, abscissa: float, startingParameter: float = None, /):
        """
        Returns the parameter on the curve of a point at the given distance from a starting parameter. 
        parameterAtDistance([abscissa, startingParameter]) -> Float the
        """

    def reverse(self):
        """Changes the direction of parametrization of the curve."""

    def tangent(self, arg1: float, /):
        """Computes the tangent of parameter u on this curve"""

    def toBSpline(self, Float: float = None, Float2: float = None, /):
        """
        Converts a curve of any type (only part from First to Last)
        					toBSpline([Float=First, Float=Last]) -> B-Spline curve
        """

    @typing.overload
    def toShape(self): ...

    @typing.overload
    def toShape(self, arg1: float, arg2: float, /): ...

    @typing.overload
    def toShape(self, arg1: Part.GeometrySurface, /): ...

    @typing.overload
    def toShape(self, arg1: Part.GeometrySurface, arg2: float, arg3: float, /): ...

    @typing.overload
    def toShape(self, arg1: Part.Face, /): ...

    @typing.overload
    def toShape(self, arg1: Part.Face, arg2: float, arg3: float, /):
        """Return the shape for the geometry."""

    def value(self, arg1: float, /):
        """Computes the point of parameter u on this curve"""


# ArcOfEllipse2dPy.xml
class ArcOfEllipse2d(Part.Geom2d.ArcOfConic2d):
    """Describes a portion of an ellipse"""

    def __init__(self, arg1: Part.Geom2d.Ellipse2d, arg2: float, arg3: float, arg4: bool = None, /):
        """Describes a portion of an ellipse"""

    @property
    def Ellipse(self) -> object:
        """The internal ellipse representation"""

    @property
    def MajorRadius(self) -> float:
        """The major radius of the ellipse."""

    @MajorRadius.setter
    def MajorRadius(self, value: float): ...

    @property
    def MinorRadius(self) -> float:
        """The minor radius of the ellipse."""

    @MinorRadius.setter
    def MinorRadius(self, value: float): ...


# ArcOfConic2dPy.xml
class ArcOfConic2d(Part.Geom2d.Curve2d):
    """Describes an abstract arc of conic in 2d space"""

    @property
    def Eccentricity(self) -> float:
        """
        returns the eccentricity value of the conic e.
                    e = 0 for a circle
                    0 < e < 1 for an ellipse  (e = 0 if MajorRadius = MinorRadius)
                    e > 1 for a hyperbola
                    e = 1 for a parabola
        """

    @property
    def Location(self) -> object:
        """Location of the conic."""

    @Location.setter
    def Location(self, value: object): ...

    @property
    def XAxis(self) -> object:
        """The X axis direction of the circle"""

    @XAxis.setter
    def XAxis(self, value: object): ...

    @property
    def YAxis(self) -> object:
        """The Y axis direction of the circle"""

    @YAxis.setter
    def YAxis(self, value: object): ...


# Conic2dPy.xml
class Conic2d(Part.Geom2d.Curve2d):
    """Describes an abstract conic in 2d space"""

    @property
    def Eccentricity(self) -> float:
        """
        returns the eccentricity value of the conic e.
                    e = 0 for a circle
                    0 < e < 1 for an ellipse  (e = 0 if MajorRadius = MinorRadius)
                    e > 1 for a hyperbola
                    e = 1 for a parabola
        """

    @property
    def Location(self) -> object:
        """Location of the conic."""

    @Location.setter
    def Location(self, value: object): ...

    @property
    def XAxis(self) -> object:
        """The X axis direction of the circle"""

    @XAxis.setter
    def XAxis(self, value: object): ...

    @property
    def YAxis(self) -> object:
        """The Y axis direction of the circle"""

    @YAxis.setter
    def YAxis(self, value: object): ...


# Geometry2dPy.xml
class Geometry2d(FreeCAD.PyObjectBase):
    """
    The abstract class Geometry for 2D space is the root class of all geometric objects.
    It describes the common behavior of these objects when:
    - applying geometric transformations to objects, and
    - constructing objects by geometric transformation (including copying).
    """

    def copy(self):
        """Create a copy of this geometry"""

    @typing.overload
    def mirror(self, arg1: object, /): ...

    @typing.overload
    def mirror(self, arg1: object, arg2: object, /):
        """Performs the symmetrical transformation of this geometric object"""

    def rotate(self, arg1: object, arg2: float, /):
        """Rotates this geometric object at angle Ang (in radians) around a point"""

    def scale(self, arg1: object, arg2: float, /):
        """Applies a scaling transformation on this geometric object with a center and scaling factor"""

    def transform(self, arg1: object, /):
        """Applies a transformation to this geometric object"""

    def translate(self, arg1: object, /):
        """Translates this geometric object"""


# Circle2dPy.xml
class Circle2d(Part.Geom2d.Conic2d):
    """
    Describes a circle in 3D space
    To create a circle there are several ways:
    Part.Geom2d.Circle2d()
        Creates a default circle with center (0,0) and radius 1

    Part.Geom2d.Circle2d(circle)
        Creates a copy of the given circle

    Part.Geom2d.Circle2d(circle, Distance)
        Creates a circle parallel to given circle at a certain distance

    Part.Geom2d.Circle2d(Center,Radius)
        Creates a circle defined by center and radius

    Part.Geom2d.Circle2d(Point1,Point2,Point3)
        Creates a circle defined by three non-linear points
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, Circle: Part.Geom2d.Circle2d): ...

    @typing.overload
    def __init__(self, Circle: Part.Geom2d.Circle2d, Distance: float): ...

    @typing.overload
    def __init__(self, Center: object, Radius: float): ...

    @typing.overload
    def __init__(self, Point1: object, Point2: object, Point3: object):
        """
        Describes a circle in 3D space
        To create a circle there are several ways:
        Part.Geom2d.Circle2d()
            Creates a default circle with center (0,0) and radius 1

        Part.Geom2d.Circle2d(circle)
            Creates a copy of the given circle

        Part.Geom2d.Circle2d(circle, Distance)
            Creates a circle parallel to given circle at a certain distance

        Part.Geom2d.Circle2d(Center,Radius)
            Creates a circle defined by center and radius

        Part.Geom2d.Circle2d(Point1,Point2,Point3)
            Creates a circle defined by three non-linear points
        """

    @property
    def Radius(self) -> float:
        """The radius of the circle."""

    @Radius.setter
    def Radius(self, value: float): ...


# ArcOfParabola2dPy.xml
class ArcOfParabola2d(Part.Geom2d.ArcOfConic2d):
    """Describes a portion of a parabola"""

    def __init__(self, arg1: Part.Geom2d.Parabola2d, arg2: float, arg3: float, arg4: bool = None, /):
        """Describes a portion of a parabola"""

    @property
    def Focal(self) -> float:
        """The focal length of the parabola."""

    @Focal.setter
    def Focal(self, value: float): ...

    @property
    def Parabola(self) -> object:
        """The internal parabola representation"""


# Line2dSegmentPy.xml
class Line2dSegment(Part.Geom2d.Curve2d):
    """
    Describes a line segment in 2D space
    To create a line there are several ways:
    Part.Geom2d.Line2dSegment()
        Creates a default line

    Part.Geom2d.Line2dSegment(Line)
        Creates a copy of the given line

    Part.Geom2d.Line2dSegment(Point1,Point2)
        Creates a line that goes through two given points
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, Line: Part.Geom2d.Line2dSegment, /): ...

    @typing.overload
    def __init__(self, Point1: object, Point2: object, /):
        """
        Describes a line segment in 2D space
        To create a line there are several ways:
        Part.Geom2d.Line2dSegment()
            Creates a default line

        Part.Geom2d.Line2dSegment(Line)
            Creates a copy of the given line

        Part.Geom2d.Line2dSegment(Point1,Point2)
            Creates a line that goes through two given points
        """

    @property
    def EndPoint(self) -> object:
        """Returns the end point of this line segment."""

    @EndPoint.setter
    def EndPoint(self, value: object): ...

    @property
    def StartPoint(self) -> object:
        """Returns the start point of this line segment."""

    @StartPoint.setter
    def StartPoint(self, value: object): ...

    def setParameterRange(self, arg1: float, arg2: float, /):
        """Set the parameter range of the underlying line segment geometry"""


# Ellipse2dPy.xml
class Ellipse2d(Part.Geom2d.Conic2d):
    """
    Describes an ellipse in 2D space
    				To create an ellipse there are several ways:
                    Part.Geom2d.Ellipse2d()
    					Creates an ellipse with major radius 2 and minor radius 1 with the
                        center in (0,0)

                    Part.Geom2d.Ellipse2d(Ellipse)
    					Create a copy of the given ellipse

                    Part.Geom2d.Ellipse2d(S1,S2,Center)
                        Creates an ellipse centered on the point Center,
    					its major axis is defined by Center and S1,
    					its major radius is the distance between Center and S1, and
    					its minor radius is the distance between S2 and the major axis.

                    Part.Geom2d.Ellipse2d(Center,MajorRadius,MinorRadius)
    					Creates an ellipse with major and minor radii MajorRadius and
                        MinorRadius
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, Ellipse: Part.Geom2d.Ellipse2d): ...

    @typing.overload
    def __init__(self, S1: object, S2: object, Center: object): ...

    @typing.overload
    def __init__(self, Center: object, MajorRadius: float, MinorRadius: float):
        """
        Describes an ellipse in 2D space
        				To create an ellipse there are several ways:
                        Part.Geom2d.Ellipse2d()
        					Creates an ellipse with major radius 2 and minor radius 1 with the
                            center in (0,0)

                        Part.Geom2d.Ellipse2d(Ellipse)
        					Create a copy of the given ellipse

                        Part.Geom2d.Ellipse2d(S1,S2,Center)
                            Creates an ellipse centered on the point Center,
        					its major axis is defined by Center and S1,
        					its major radius is the distance between Center and S1, and
        					its minor radius is the distance between S2 and the major axis.

                        Part.Geom2d.Ellipse2d(Center,MajorRadius,MinorRadius)
        					Creates an ellipse with major and minor radii MajorRadius and
                            MinorRadius
        """

    @property
    def Focal(self) -> float:
        """The focal distance of the ellipse."""

    @property
    def Focus1(self) -> object:
        """
        The first focus is on the positive side of the major axis of the ellipse;
        the second focus is on the negative side.
        """

    @property
    def Focus2(self) -> object:
        """
        The first focus is on the positive side of the major axis of the ellipse;
        the second focus is on the negative side.
        """

    @property
    def MajorRadius(self) -> float:
        """The major radius of the ellipse."""

    @MajorRadius.setter
    def MajorRadius(self, value: float): ...

    @property
    def MinorRadius(self) -> float:
        """The minor radius of the ellipse."""

    @MinorRadius.setter
    def MinorRadius(self, value: float): ...


# ArcOfCircle2dPy.xml
class ArcOfCircle2d(Part.Geom2d.ArcOfConic2d):
    """Describes a portion of a circle"""

    @typing.overload
    def __init__(self, arg1: Part.Geom2d.Circle2d, arg2: float, arg3: float, arg4: bool = None, /): ...

    @typing.overload
    def __init__(self, arg1: object, arg2: object, arg3: object, /):
        """Describes a portion of a circle"""

    @property
    def Circle(self) -> object:
        """The internal circle representation"""

    @property
    def Radius(self) -> float:
        """The radius of the circle."""

    @Radius.setter
    def Radius(self, value: float): ...


# ArcOfHyperbola2dPy.xml
class ArcOfHyperbola2d(Part.Geom2d.ArcOfConic2d):
    """Describes a portion of an hyperbola"""

    def __init__(self, arg1: Part.Geom2d.Hyperbola2d, arg2: float, arg3: float, arg4: bool = None, /):
        """Describes a portion of an hyperbola"""

    @property
    def Hyperbola(self) -> object:
        """The internal hyperbola representation"""

    @property
    def MajorRadius(self) -> float:
        """The major radius of the hyperbola."""

    @MajorRadius.setter
    def MajorRadius(self, value: float): ...

    @property
    def MinorRadius(self) -> float:
        """The minor radius of the hyperbola."""

    @MinorRadius.setter
    def MinorRadius(self, value: float): ...


# Hyperbola2dPy.xml
class Hyperbola2d(Part.Geom2d.Conic2d):
    """
    Describes a hyperbola in 2D space
                    To create a hyperbola there are several ways:
                    Part.Geom2d.Hyperbola2d()
                        Creates a hyperbola with major radius 2 and minor radius 1 with the
                        center in (0,0)

                    Part.Geom2d.Hyperbola2d(Hyperbola)
    					Create a copy of the given hyperbola

                    Part.Geom2d.Hyperbola2d(S1,S2,Center)
                        Creates a hyperbola centered on the point Center, S1 and S2,
    					its major axis is defined by Center and S1,
    					its major radius is the distance between Center and S1, and
    					its minor radius is the distance between S2 and the major axis.

                    Part.Geom2d.Hyperbola2d(Center,MajorRadius,MinorRadius)
                        Creates a hyperbola with major and minor radii MajorRadius and
                        MinorRadius and located at Center
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, Hyperbola: Part.Geom2d.Hyperbola2d): ...

    @typing.overload
    def __init__(self, S1: object, S2: object, Center: object): ...

    @typing.overload
    def __init__(self, Center: object, MajorRadius: float, MinorRadius: float):
        """
        Describes a hyperbola in 2D space
                        To create a hyperbola there are several ways:
                        Part.Geom2d.Hyperbola2d()
                            Creates a hyperbola with major radius 2 and minor radius 1 with the
                            center in (0,0)

                        Part.Geom2d.Hyperbola2d(Hyperbola)
        					Create a copy of the given hyperbola

                        Part.Geom2d.Hyperbola2d(S1,S2,Center)
                            Creates a hyperbola centered on the point Center, S1 and S2,
        					its major axis is defined by Center and S1,
        					its major radius is the distance between Center and S1, and
        					its minor radius is the distance between S2 and the major axis.

                        Part.Geom2d.Hyperbola2d(Center,MajorRadius,MinorRadius)
                            Creates a hyperbola with major and minor radii MajorRadius and
                            MinorRadius and located at Center
        """

    @property
    def Focal(self) -> float:
        """The focal distance of the hyperbola."""

    @property
    def Focus1(self) -> object:
        """
        The first focus is on the positive side of the major axis of the hyperbola;
        the second focus is on the negative side.
        """

    @property
    def Focus2(self) -> object:
        """
        The first focus is on the positive side of the major axis of the hyperbola;
        the second focus is on the negative side.
        """

    @property
    def MajorRadius(self) -> float:
        """The major radius of the hyperbola."""

    @MajorRadius.setter
    def MajorRadius(self, value: float): ...

    @property
    def MinorRadius(self) -> float:
        """The minor radius of the hyperbola."""

    @MinorRadius.setter
    def MinorRadius(self, value: float): ...


# BSplineCurve2dPy.xml
class BSplineCurve2d(Part.Geom2d.Curve2d):
    """Describes a B-Spline curve in 3D space"""

    def __init__(self):
        """Describes a B-Spline curve in 3D space"""

    @property
    def Degree(self) -> int:
        """Returns the polynomial degree of this B-Spline curve."""

    @property
    def EndPoint(self) -> object:
        """Returns the end point of this B-Spline curve."""

    @property
    def FirstUKnotIndex(self) -> object:
        """
        Returns the index in the knot array of the knot
        corresponding to the first or last parameter
        of this B-Spline curve.
        """

    @property
    def KnotSequence(self) -> list:
        """Returns the knots sequence of this B-Spline curve."""

    @property
    def LastUKnotIndex(self) -> object:
        """
        Returns the index in the knot array of the knot
        corresponding to the first or last parameter
        of this B-Spline curve.
        """

    @property
    def MaxDegree(self) -> int:
        """
        Returns the value of the maximum polynomial degree of any
        B-Spline curve curve. This value is 25.
        """

    @property
    def NbKnots(self) -> int:
        """Returns the number of knots of this B-Spline curve."""

    @property
    def NbPoles(self) -> int:
        """Returns the number of poles of this B-Spline curve."""

    @property
    def StartPoint(self) -> object:
        """Returns the start point of this B-Spline curve."""

    def approximate(self, Points: object, DegMax: int = None, Continuity: str = None, Tolerance: float = None, DegMin: int = None, ParamType: str = None, Parameters: object = None, LengthWeight: float = None, CurvatureWeight: float = None, TorsionWeight: float = None):
        """
        Replaces this B-Spline curve by approximating a set of points.
        					The function accepts keywords as arguments.

        					approximate2(Points = list_of_points)

        					Optional arguments :

        					DegMin = integer (3) : Minimum degree of the curve.
        					DegMax = integer (8) : Maximum degree of the curve.
        					Tolerance = float (1e-3) : approximating tolerance.
        					Continuity = string ('C2') : Desired continuity of the curve.
        					Possible values : 'C0','G1','C1','G2','C2','C3','CN'

        					LengthWeight = float, CurvatureWeight = float, TorsionWeight = float
        					If one of these arguments is not null, the functions approximates the
        					points using variational smoothing algorithm, which tries to minimize
        					additional criterium:
        					LengthWeight*CurveLength + CurvatureWeight*Curvature + TorsionWeight*Torsion
        					Continuity must be C0, C1 or C2, else defaults to C2.

        					Parameters = list of floats : knot sequence of the approximated points.
        					This argument is only used if the weights above are all null.

        					ParamType = string ('Uniform','Centripetal' or 'ChordLength')
        					Parameterization type. Only used if weights and Parameters above aren't specified.

        					Note : Continuity of the spline defaults to C2. However, it may not be applied if
        					it conflicts with other parameters ( especially DegMax ).
        """

    def buildFromPoles(self, arg1: object, arg2: bool = None, arg3: int = None, arg4: bool = None, /):
        """Builds a B-Spline by a list of poles."""

    def buildFromPolesMultsKnots(self, poles: object, mults: object = None, knots: object = None, periodic: bool = None, degree: int = None, weights: object = None):
        """
        Builds a B-Spline by a lists of Poles, Mults, Knots.
        				arguments: poles (sequence of Base.Vector), [mults , knots, periodic, degree, weights (sequence of float), CheckRational]

        				Examples:
        				from FreeCAD import Base
        				import Part
        				V=Base.Vector
        				poles=[V(-10,-10),V(10,-10),V(10,10),V(-10,10)]

        				# non-periodic spline
        				n=Part.BSplineCurve()
        				n.buildFromPolesMultsKnots(poles,(3,1,3),(0,0.5,1),False,2)
        				Part.show(n.toShape())

        				# periodic spline
        				p=Part.BSplineCurve()
        				p.buildFromPolesMultsKnots(poles,(1,1,1,1,1),(0,0.25,0.5,0.75,1),True,2)
        				Part.show(p.toShape())

        				# periodic and rational spline
        				r=Part.BSplineCurve()
        				r.buildFromPolesMultsKnots(poles,(1,1,1,1,1),(0,0.25,0.5,0.75,1),True,2,(1,0.8,0.7,0.2))
        				Part.show(r.toShape())
        """

    @typing.overload
    def getCardinalSplineTangents(self, Points: object, Parameter: float): ...

    @typing.overload
    def getCardinalSplineTangents(self, Points: object, Parameters: object):
        """Compute the tangents for a Cardinal spline"""

    def getKnot(self, arg1: int, /):
        """Get a knot of the B-Spline curve."""

    def getKnots(self):
        """Get all knots of the B-Spline curve."""

    def getMultiplicities(self):
        """Returns the multiplicities table M of the knots of this B-Spline curve."""

    def getMultiplicity(self, arg1: int, /):
        """
        Returns the multiplicity of the knot of index
        from the knots table of this B-Spline curve.
        """

    def getPole(self, arg1: int, /):
        """Get a pole of the B-Spline curve."""

    def getPoles(self):
        """Get all poles of the B-Spline curve."""

    def getPolesAndWeights(self):
        """Returns the table of poles and weights in homogeneous coordinates."""

    def getResolution(self, arg1: float, /):
        """
        Computes for this B-Spline curve the parametric tolerance (UTolerance)
        for a given 3D tolerance (Tolerance3D).
        If f(t) is the equation of this B-Spline curve, the parametric tolerance
        ensures that:
        |t1-t0| < UTolerance ===> |f(t1)-f(t0)| < Tolerance3D
        """

    def getWeight(self, arg1: int, /):
        """Get a weight of the B-Spline curve."""

    def getWeights(self):
        """Get all weights of the B-Spline curve."""

    def increaseDegree(self, arg1: int, /):
        """
        increase(Int=Degree)
        Increases the degree of this B-Spline curve to Degree.
        As a result, the poles, weights and multiplicities tables
        are modified; the knots table is not changed. Nothing is
        done if Degree is less than or equal to the current degree.
        """

    def increaseMultiplicity(self, int_start: int, int_end: int, int_mult: int = None, /):
        """
        increaseMultiplicity(int index, int mult)
        				increaseMultiplicity(int start, int end, int mult)
        				Increases multiplicity of knots up to mult.

        				index: the index of a knot to modify (1-based)
        				start, end: index range of knots to modify.
        				If mult is lower or equal to the current multiplicity nothing is done. If mult is higher than the degree the degree is used.
        """

    def incrementMultiplicity(self, int_start: int, int_end: int, int_mult: int, /):
        """
        incrementMultiplicity(int start, int end, int mult)
        				Raises multiplicity of knots by mult.

        				start, end: index range of knots to modify.
        """

    def insertKnot(self, u: float, mult: int = 1, tol: float = 0.0, /):
        """
        insertKnot(u, mult = 1, tol = 0.0)
        				Inserts a knot value in the sequence of knots. If u is an existing knot the
        				multiplicity is increased by mult.
        """

    def insertKnots(self, list_of_floats: object, list_of_ints: object, tol: float = 0.0, bool_add: bool = True, /):
        """
        insertKnots(list_of_floats, list_of_ints, tol = 0.0, bool_add = True)
        				Inserts a set of knots values in the sequence of knots.

        				For each u = list_of_floats[i], mult = list_of_ints[i]

        				If u is an existing knot the multiplicity is increased by mult if bool_add is
        				True, otherwise increased to mult.

        				If u is not on the parameter range nothing is done.

        				If the multiplicity is negative or null nothing is done. The new multiplicity
        				is limited to the degree.

        				The tolerance criterion for knots equality is the max of Epsilon(U) and ParametricTolerance.
        """

    def interpolate(self, Points: object, PeriodicFlag: bool = None, Tolerance: float = None, InitialTangent: object = None, FinalTangent: object = None, Tangents: object = None, TangentFlags: object = None, Parameters: object = None):
        """
        Replaces this B-Spline curve by interpolating a set of points.
        					The function accepts keywords as arguments.

        					interpolate(Points = list_of_points)

        					Optional arguments :

        					PeriodicFlag = bool (False) : Sets the curve closed or opened.
        					Tolerance = float (1e-6) : interpolating tolerance

        					Parameters : knot sequence of the interpolated points.
        					If not supplied, the function defaults to chord-length parameterization.
        					If PeriodicFlag == True, one extra parameter must be appended.

        					EndPoint Tangent constraints :

        					InitialTangent = vector, FinalTangent = vector
        					specify tangent vectors for starting and ending points
        					of the BSpline. Either none, or both must be specified.

        					Full Tangent constraints :

        					Tangents = list_of_vectors, TangentFlags = list_of_bools
        					Both lists must have the same length as Points list.
        					Tangents specifies the tangent vector of each point in Points list.
        					TangentFlags (bool) activates or deactivates the corresponding tangent.
        					These arguments will be ignored if EndPoint Tangents (above) are also defined.

        					Note : Continuity of the spline defaults to C2. However, if periodic, or tangents
        					are supplied, the continuity will drop to C1.
        """

    def isClosed(self):
        """
        Returns true if the distance between the start point and end point of
        					this B-Spline curve is less than or equal to gp::Resolution().
        """

    def isPeriodic(self):
        """Returns true if this BSpline curve is periodic."""

    def isRational(self):
        """
        Returns true if this B-Spline curve is rational.
        					A B-Spline curve is rational if, at the time of construction,
        					the weight table has been initialized.
        """

    def join(self, arg1: Part.Geom2d.BSplineCurve2d, /):
        """Build a new spline by joining this and a second spline."""

    def makeC1Continuous(self, arg1: float = None, /):
        """
        makeC1Continuous(tol = 1e-6, ang_tol = 1e-7)
        					Reduces as far as possible the multiplicities of the knots of this BSpline
        					(keeping the geometry). It returns a new BSpline, which could still be C0.
        					tol is a geometrical tolerance.
        					The tol_ang is angular tolerance, in radians. It sets tolerable angle mismatch
        					of the tangents on the left and on the right to decide if the curve is G1 or
        					not at a given point.
        """

    def movePoint(self, U: float, P: object, Index1: int, Index2: int, /):
        """
        movePoint(U, P, Index1, Index2)
        				Moves the point of parameter U of this B-Spline curve to P.
        Index1 and Index2 are the indexes in the table of poles of this B-Spline curve
        of the first and last poles designated to be moved.

        Returns: (FirstModifiedPole, LastModifiedPole). They are the indexes of the
        first and last poles which are effectively modified.
        """

    def removeKnot(self, Index: int, M: int, tol: float, /):
        """
        removeKnot(Index, M, tol)

        					Reduces the multiplicity of the knot of index Index to M.
        					If M is equal to 0, the knot is removed.
        					With a modification of this type, the array of poles is also modified.
        					Two different algorithms are systematically used to compute the new
        					poles of the curve. If, for each pole, the distance between the pole
        					calculated using the first algorithm and the same pole calculated using
        					the second algorithm, is less than Tolerance, this ensures that the curve
        					is not modified by more than Tolerance. Under these conditions, true is
        					returned; otherwise, false is returned.

        					A low tolerance is used to prevent modification of the curve.
        					A high tolerance is used to 'smooth' the curve.
        """

    def segment(self, u1: float, u2: float, /):
        """
        segment(u1,u2)
        					Modifies this B-Spline curve by segmenting it.
        """

    def setKnot(self, arg1: int, arg2: float, arg3: int = None, /):
        """Set a knot of the B-Spline curve."""

    def setKnots(self, arg1: object, /):
        """Set knots of the B-Spline curve."""

    def setNotPeriodic(self):
        """
        Changes this B-Spline curve into a non-periodic curve.
        If this curve is already non-periodic, it is not modified.
        """

    def setOrigin(self, arg1: int, /):
        """
        Assigns the knot of index Index in the knots table
        as the origin of this periodic B-Spline curve. As a consequence,
        the knots and poles tables are modified.
        """

    def setPeriodic(self):
        """Changes this B-Spline curve into a periodic curve."""

    def setPole(self, arg1: int, arg2: object, arg3: float = None, /):
        """
        Modifies this B-Spline curve by assigning P
        to the pole of index Index in the poles table.
        """

    def setWeight(self, arg1: int, arg2: float, /):
        """Set a weight of the B-Spline curve."""

    def toBezier(self):
        """Build a list of Bezier splines."""

    def toBiArcs(self, tolerance: float, /):
        """
        Build a list of arcs and lines to approximate the B-spline.
        					toBiArcs(tolerance) -> list.
        """


# BezierCurve2dPy.xml
class BezierCurve2d(Part.Geom2d.Curve2d):
    """
    Describes a rational or non-rational Bezier curve in 2d space:
    				-- a non-rational Bezier curve is defined by a table of poles (also called control points)
    				-- a rational Bezier curve is defined by a table of poles with varying weights
    """

    @property
    def Degree(self) -> int:
        """
        Returns the polynomial degree of this Bezier curve,
        which is equal to the number of poles minus 1.
        """

    @property
    def EndPoint(self) -> object:
        """Returns the end point of this Bezier curve."""

    @property
    def MaxDegree(self) -> int:
        """
        Returns the value of the maximum polynomial degree of any
        Bezier curve curve. This value is 25.
        """

    @property
    def NbPoles(self) -> int:
        """Returns the number of poles of this Bezier curve."""

    @property
    def StartPoint(self) -> object:
        """Returns the start point of this Bezier curve."""

    def getPole(self, arg1: int, /):
        """Get a pole of the Bezier curve."""

    def getPoles(self):
        """Get all poles of the Bezier curve."""

    def getResolution(self, arg1: float, /):
        """
        Computes for this Bezier curve the parametric tolerance (UTolerance)
        for a given 3D tolerance (Tolerance3D).
        If f(t) is the equation of this Bezier curve, the parametric tolerance
        ensures that:
        |t1-t0| < UTolerance ===> |f(t1)-f(t0)| < Tolerance3D
        """

    def getWeight(self, arg1: int, /):
        """Get a weight of the Bezier curve."""

    def getWeights(self):
        """Get all weights of the Bezier curve."""

    def increase(self, Int: int, /):
        """
        increase(Int=Degree)
        Increases the degree of this Bezier curve to Degree.
        As a result, the poles and weights tables are modified.
        """

    def insertPoleAfter(self, arg1: int, arg2: object, arg3: float = None, /):
        """Inserts after the pole of index."""

    def insertPoleBefore(self, arg1: int, arg2: object, arg3: float = None, /):
        """Inserts before the pole of index."""

    def isClosed(self):
        """
        Returns true if the distance between the start point and end point of
        					this Bezier curve is less than or equal to gp::Resolution().
        """

    def isPeriodic(self):
        """Returns false."""

    def isRational(self):
        """Returns false if the weights of all the poles of this Bezier curve are equal."""

    def removePole(self, arg1: int, /):
        """
        Removes the pole of index Index from the table of poles of this Bezier curve.
        If this Bezier curve is rational, it can become non-rational.
        """

    def segment(self, arg1: float, arg2: float, /):
        """Modifies this Bezier curve by segmenting it."""

    def setPole(self, arg1: int, arg2: object, arg3: float = None, /):
        """Set a pole of the Bezier curve."""

    def setPoles(self, arg1: object, /):
        """Set the poles of the Bezier curve."""

    def setWeight(self, arg1: int, arg2: float, /):
        """Set a weight of the Bezier curve."""


# OffsetCurve2dPy.xml
class OffsetCurve2d(Part.Geom2d.Curve2d):
    def __init__(self, arg1: Part.Geom2d.Curve2d, arg2: float, /): ...

    @property
    def BasisCurve(self) -> object:
        """Sets or gets the basic curve."""

    @property
    def OffsetValue(self) -> float:
        """Sets or gets the offset value to offset the underlying curve."""


# Parabola2dPy.xml
class Parabola2d(Part.Geom2d.Conic2d):
    """Describes a parabola in 2D space"""

    def __init__(self):
        """Describes a parabola in 2D space"""

    @property
    def Focal(self) -> float:
        """
        The focal distance is the distance between
        the apex and the focus of the parabola.
        """

    @Focal.setter
    def Focal(self, value: float): ...

    @property
    def Focus(self) -> object:
        """
        The focus is on the positive side of the
        'X Axis' of the local coordinate system of the parabola.
        """

    @property
    def Parameter(self) -> float:
        """
        Compute the parameter of this parabola
        which is the distance between its focus
        and its directrix. This distance is twice the focal length.
        """


# Line2dPy.xml
class Line2d(Part.Geom2d.Curve2d):
    """
    Describes an infinite line in 2D space
    To create a line there are several ways:
    Part.Geom2d.Line2d()
        Creates a default line

    Part.Geom2d.Line2d(Line)
        Creates a copy of the given line

    Part.Geom2d.Line2d(Point,Dir)
        Creates a line that goes through two given points
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, Line: Part.Geom2d.Line2d, /): ...

    @typing.overload
    def __init__(self, Point: object, Dir: object, /):
        """
        Describes an infinite line in 2D space
        To create a line there are several ways:
        Part.Geom2d.Line2d()
            Creates a default line

        Part.Geom2d.Line2d(Line)
            Creates a copy of the given line

        Part.Geom2d.Line2d(Point,Dir)
            Creates a line that goes through two given points
        """

    @property
    def Direction(self) -> object:
        """Returns the direction of this line."""

    @Direction.setter
    def Direction(self, value: object): ...

    @property
    def Location(self) -> object:
        """Returns the location of this line."""

    @Location.setter
    def Location(self, value: object): ...
