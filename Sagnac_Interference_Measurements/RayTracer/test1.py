from raytracing import *

title = "A test"


def exampleCode(comments=None):
    path = ImagingPath()
    path.label = title
    path.append(Space(d=100))
    path.append(Lens(f=50))
    path.append(Space(d=100))
    path.display(comments=comments)


exampleCode()
