import contextlib
from naparikro.widgets.main_widget import ArkitektWidget

import napari
from mikro.schema import Representation, Sample
from naparikro.helpers.stage import StageHelper
from arkitekt.agents import AppAgent
from arkitekt import SearchWidget
import qasync
import numpy as np
import argparse
import asyncio
from rich.console import Console

console = Console()


async def main(viewer, **kwargs):
   
    agent = AppAgent(with_monitor=True, **kwargs)

    stage_helper = StageHelper(viewer)

    @agent.register(widgets={
        "rep": SearchWidget(query="""
            query Search($search: String){
                options: representations(name: $search) {
                    value: id
                    label: name
                }
            }
        """)
    })
    async def blower(rep: Representation) -> Representation:
        """Show Blower

        Shows the Image on Napari

        Args:
            rep (Representation): [description]

        Returns:
            Representation: [description]
        """
        print("hallo is doing this")
        await stage_helper.open_as_layer(rep)
        
        return rep

    @agent.register(widgets={
        "sample": SearchWidget(query="""
            query Search($search: String){
                options: samples(name: $search) {
                    value: id
                    label: name
                }
            }
        """)
    })
    async def upload(name: str = None, sample: Sample = None) -> Representation:
        """Upload an Active Image

        Uploads the curently active image on Napari

        Args:
            name (str, optional): How do you want to name the image?
            sample (Sample, optional): Which sample should we put the new image in?

        Returns:
            Representation: The uploaded image from the app
        """
        array = await stage_helper.get_active_layer_as_xarray()
        rep = await Representation.asyncs.from_xarray(array, name=name, sample=sample, tags=[])
        return rep

    try:
        await agent.aprovide()
    except Exception:
        console.print_exception()



def app_main(**kwargs):
    viewer = napari.Viewer()
    widget = ArkitektWidget()
    viewer.window.add_dock_widget(widget, area="right")
    app = napari.qt.get_app()
    loop = qasync.QSelectorEventLoop(app)
    asyncio.set_event_loop(loop)
    loop.create_task(main(viewer, **kwargs))
    napari.run()





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Which config file to use', default="bergen.yaml", type=str)
    args = parser.parse_args()

    app_main(config_path=args.config)
