import platform
from abc import ABC, abstractmethod
from settingstree import Settings, SettingsNode
from settingstree.widgets.nodewidgets import NodeSubtree
from . import capturing, processing, controller
from .builtin import ChainElement, ProcessingResult


class ProcessingChain(ABC):
    # Use this chain if platform string matches platform.system()
    platform = 'Linux'

    def __init__(self, settings: Settings):
        super().__init__()
        self.chain_elements = []
        self._settings = settings

    @classmethod
    def get_platform_specific_chain(cls):
        """
        Returns the chain for the current platform.
        :rtype: ProcessingChain
        """
        # TODO: Recursive search (multi inheritance)
        # TODO: Respect settingstree (user could use another chain for his system)
        for subclass in cls.__subclasses__():
            if subclass.platform == platform.system():
                return subclass

    def register(self, chain_element):
        """
        This method adds the given chain_element to the internal list with chain_elements.
        :param chain_element:
        :return:
        """
        if not isinstance(chain_element, ChainElement):
            raise TypeError('chain_element needs to be an instance of chain.ChainElement!')

        self.chain_elements.append(chain_element)

        # Collect element specific settings from chain_element.
        chain_element_settings_subtree = chain_element.collect_settings()
        if chain_element_settings_subtree.has_children():
            self._settings.root.add_child(chain_element_settings_subtree)

    def run(self):
        """
        This method iterates through all registered chain_elements. It calls the process method and passes the output
        to the next chain element.
        """
        mid_result = ProcessingResult([], {})

        for element in self.chain_elements:
            mid_result = element.process(*mid_result.args, **mid_result.kwargs)

        # TODO: add field content_for_websocket to ProcessingResult. This than gets returned to the api which sends it
        #  to the browser via websocket.
        # TODO: find a way to send data via websocket from inside a chain_element.


class CVChainWindows(ProcessingChain):
    platform = 'Windows'

    def __init__(self, settings):
        super().__init__(settings)

        self.register(capturing.ImageGrabDevice())
        self.register(processing.ColorConversionPreProcessingUnit())
        self.register(processing.ROIPreProcessingUnit())
        self.register(processing.CVLaneDetectionProcessingUnit())
        self.register(controller.VjoyController())


class CVChainLinux(ProcessingChain):
    platform = 'Linux'

    def __init__(self, settings):
        super().__init__(settings)

        self.register(capturing.PyscreenshotDevice())
        self.register(processing.ColorConversionPreProcessingUnit())
        self.register(processing.ROIPreProcessingUnit())
        self.register(processing.CVLaneDetectionProcessingUnit())
        # self.register()
