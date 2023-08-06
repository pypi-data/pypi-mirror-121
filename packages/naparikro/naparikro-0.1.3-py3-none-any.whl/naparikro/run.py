import contextlib
from naparikro.widgets.main_widget import ArkitektWidget

import napari
from naparikro.helpers.stage import StageHelper
from arkitekt.agents import AppAgent
from arkitekt import SearchWidget
import numpy as np
import argparse



def app_main(**kwargs):
    viewer = napari.Viewer()
    widget = ArkitektWidget(viewer, **kwargs)
    viewer.window.add_dock_widget(widget, area="left", name="Arkitekt")
    napari.run()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Which config file to use', default="bergen.yaml", type=str)
    args = parser.parse_args()

    app_main(config_path=args.config)
