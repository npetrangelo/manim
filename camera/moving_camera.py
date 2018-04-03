from __future__ import absolute_import

from camera.camera import Camera

class MovingCamera(Camera):
    """
    Stays in line with the height, width and position
    of a given mobject
    """
    CONFIG = {
        "aligned_dimension" : "width" #or height
    }
    def __init__(self, frame, **kwargs):
        """
        frame is a Mobject, (should be a rectangle) determining 
        which region of space the camera displys
        """
        self.frame = frame
        Camera.__init__(self, **kwargs)

    def capture_mobjects(self, *args, **kwargs):
        self.space_center = self.frame.get_center()
        self.realign_frame_shape()
        Camera.capture_mobjects(self, *args, **kwargs)

    def realign_frame_shape(self):
        height, width = self.frame_shape
        if self.aligned_dimension == "height":
            self.frame_shape = (self.frame.get_height(), width)
        else:
            self.frame_shape = (height, self.frame.get_width())
        self.resize_frame_shape(0 if self.aligned_dimension == "height" else 1)
