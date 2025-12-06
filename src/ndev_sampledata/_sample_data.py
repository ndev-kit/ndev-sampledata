"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/building_a_plugin/guides.html#sample-data

Replace code below according to your needs.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pooch
from bioio import BioImage
from bioio_imageio import Reader as ImageIOReader
from bioio_ome_tiff import Reader as OmeTiffReader
from ndevio._napari_reader import napari_reader_function

if TYPE_CHECKING:
    from napari.types import LayerDataTuple

sample_dir = Path(__file__).parent / "samples"


def ndev_logo() -> list[LayerDataTuple]:
    img = BioImage(sample_dir / "ndev-logo.png", reader=ImageIOReader)
    data = img.data.squeeze()
    metadata = {
        "name": "ndev logo",
        "blending": "translucent",
        "rgb": True,
    }
    return [(data, metadata)]


def neuron_2d_4ch() -> list[LayerDataTuple]:
    img = BioImage(
        sample_dir / "neuron-4Ch-crop.tiff",
        reader=OmeTiffReader,
    )
    scale = (img.physical_pixel_sizes.Y, img.physical_pixel_sizes.X)
    ch0 = (
        img.get_image_data("YX", C=0),
        {
            "name": "NCOA4",
            "blending": "translucent_no_depth",
            "colormap": "cyan",
            "scale": scale,
        },
    )
    ch1 = (
        img.get_image_data("YX", C=1),
        {
            "name": "Ferritin",
            "blending": "additive",
            "colormap": "yellow",
            "scale": scale,
        },
    )
    ch2 = (
        img.get_image_data("YX", C=2),
        {
            "name": "Phalloidin",
            "blending": "additive",
            "colormap": "magenta",
            "scale": scale,
        },
    )
    ch3 = (
        img.get_image_data("YX", C=3),
        {
            "name": "DAPI",
            "blending": "additive",
            "colormap": "red",
            "scale": scale,
        },
    )
    return [ch0, ch1, ch2, ch3]


def scratch_assay() -> list[LayerDataTuple]:
    img = BioImage(
        sample_dir / "scratch-assay-labeled-10T-2Ch.tiff",
        reader=OmeTiffReader,
    )
    scale = (img.physical_pixel_sizes.Y, img.physical_pixel_sizes.X)
    ch0 = (
        img.get_image_data("TYX", C=0),
        {
            "name": "H3342",  # img.channel_names[0],
            "blending": "translucent_no_depth",
            "contrast_limits": (400, 3500),
            "colormap": "cyan",
            "scale": scale,
        },
        "image",
    )
    ch1 = (
        img.get_image_data("TYX", C=1),
        {
            "name": "Oblique",  # img.channel_names[1],
            "blending": "additive",
            "colormap": "gray",
            "scale": scale,
        },
        "image",
    )
    ch2 = (
        img.get_image_data("TYX", C=2),
        {
            "name": "nuclei",  # img.channel_names[2],
            "blending": "additive",
            "opacity": 0.5,
            "scale": scale,
        },
        "labels",
    )
    ch3 = (
        img.get_image_data("TYX", C=3),
        {
            "name": "cytoplasm",  # img.channel_names[3],
            "blending": "additive",
            "opacity": 0.5,
            "scale": scale,
        },
        "labels",
    )
    return [ch0, ch1, ch2, ch3]


def neocortex() -> list[LayerDataTuple]:
    img = BioImage(
        sample_dir / "neocortex-3Ch-crop.tiff",
        reader=OmeTiffReader,
    )
    scale = (img.physical_pixel_sizes.Y, img.physical_pixel_sizes.X)
    ch0 = (
        img.get_image_data("YX", C=0),
        {
            "name": "CTIP2",  # img.channel_names[0],
            "blending": "translucent_no_depth",
            "colormap": "cyan",
            "scale": scale,
        },
    )
    ch1 = (
        img.get_image_data("YX", C=1),
        {
            "name": "BRN2",  # img.channel_names[1],
            "blending": "additive",
            "colormap": "yellow",
            "scale": scale,
        },
    )
    ch2 = (
        img.get_image_data("YX", C=2),
        {
            "name": "ROR",  # img.channel_names[2],
            "blending": "additive",
            "colormap": "magenta",
            "scale": scale,
        },
    )
    return [ch0, ch1, ch2]


def neuron_raw() -> list[LayerDataTuple]:
    # use pooch to get the download from remote URL if not present locally
    neuron_raw_path = pooch.retrieve(
        url="doi:10.5281/zenodo.17836129/neuron-4Ch_raw.tiff",
        known_hash="md5:5d3e42bca2085e8588b6f23cf89ba87c",
        fname="neuron-4Ch_raw.tiff",
        path=sample_dir,
    )

    return napari_reader_function(
        path=neuron_raw_path,
        reader=OmeTiffReader,
        in_memory=True,
        layer_type="image",
    )


def neuron_labels() -> list[LayerDataTuple]:
    return napari_reader_function(
        path=sample_dir / "neuron-4Ch_labels.tiff",
        reader=OmeTiffReader,
        in_memory=True,
        layer_type="labels",
    )


def neuron_labels_processed() -> list[LayerDataTuple]:
    return napari_reader_function(
        path=sample_dir / "neuron-4Ch_labels_processed.tiff",
        reader=OmeTiffReader,
        in_memory=True,
        layer_type="labels",
    )
