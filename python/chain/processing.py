from logging import Logger
from abc import ABC, abstractmethod
from .builtin import ChainElement, ProcessingResult
from settingstree import SettingsNode, TextWidget
import numpy as np
import cv2

log = Logger(__name__)


class PreProcessingUnit(ChainElement):
    @abstractmethod
    def process(self, frame, *args, **kwargs):
        """
        This method is doing something with your frame (e.g. resizing) and returns the new frame.
        :param frame: A frame you want to pre-process.
        :return: pre-processed frame.
        """


class ProcessingUnit(ChainElement):
    @abstractmethod
    def process(self, frame, *args, **kwargs):
        """
        This method takes a frame and figures out the steering angle.
        :param frame: A frame you want to process.
        :return: Steering angle.
        """


class ColorConversionPreProcessingUnit(PreProcessingUnit):
    def process(self, frame, *args, **kwargs):
        frame_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return ProcessingResult(args=(frame_converted,))


class ROIPreProcessingUnit(PreProcessingUnit):
    VERBOSE_NAME = 'Viewport'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.x1 = SettingsNode(key='x1', widget=TextWidget, verbose_name='Left')
        self.x2 = SettingsNode(key='x2', widget=TextWidget, verbose_name='Right')
        self.y1 = SettingsNode(key='y1', widget=TextWidget, verbose_name='Top')
        self.y2 = SettingsNode(key='y2', widget=TextWidget, verbose_name='Bottom')

    def process(self, frame, *args, **kwargs):
        roi_frame = frame[int(self.y1.value):int(self.y2.value), int(self.x1.value):int(self.x2.value)]
        return ProcessingResult(args=(roi_frame,))


class CVLaneDetectionProcessingUnit(ProcessingUnit):
    def process(self, frame, *args, **kwargs):
        angle = 0
        # TODO: Also send image with drawn lanes to webapp.
        return ProcessingResult()
