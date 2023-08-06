from tkinter import Tk
from tkinter import filedialog as fd
import logging

from PySimultan import DataModel
from PySimultanRadiation import TemplateParser


if __name__ == '__main__':

    Tk().withdraw()
    project_filename = fd.askopenfilename(title='Select a SIMULTAN Project...')
    if project_filename is None:
        logging.error('No file selected')

    template_filename = fd.askopenfilename(title='Select a Template-File...')
    if template_filename is None:
        logging.error('No file selected')

    template_parser = TemplateParser(template_filepath=template_filename)
    data_model = DataModel(project_path=project_filename)
    typed_data = data_model.get_typed_data(template_parser=template_parser, create_all=True)

    geo_model = template_parser.typed_geo_models[123]

    my_scene = Scene(vertices=geo_model.vertices,
                     edges=geo_model.edges,
                     edge_loops=geo_model.edge_loops,
                     faces=geo_model.faces,
                     volumes=geo_model.volumes,
                     terrain_height=14.2)

    mesh = my_scene.generate_shading_analysis_mesh()

    print('done')
