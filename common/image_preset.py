from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import List, Tuple


class ImageType(Enum):
    JPG = '|format-jpeg|jpegquality-70', 'image/jpeg'
    PNG = '|format-png', 'image/png'
    WEBP = '|format-webp', 'image/webp'


class PageBreakpointsPx(IntEnum):
    """Keep in sync with _breakpoints.scss"""
    zero = 0
    tablet_portrait = 769
    tablet_landscape = 1025
    laptop = 1367
    fhd = 1921


class ImageSizeSelector:
    def __init__(self, min_page_width_px, scaling_type, *dimensions) -> None:
        self.min_page_width_px = min_page_width_px
        self.scaling_type = scaling_type
        self.dimensions = list(dimensions)


SizeAndDensity = namedtuple('SizeAndDensity', ['size', 'density'])


@dataclass
class ImageRenderSourceSet:
    image_size_densities: List[SizeAndDensity]
    image_type: ImageType
    min_page_width_px: int = 0


@dataclass
class ImageRenderPreset:
    """Options in order of precedence"""
    sizes: List[ImageSizeSelector]
    default_set: str
    image_types: Tuple[ImageType] = (ImageType.WEBP, ImageType.JPG)
    image_densities: Tuple[int] = (1, 2)

    @property
    def default_image(self) -> str:
        return self.default_set

    @property
    def image_alternatives(self) -> List[ImageRenderSourceSet]:
        renders = []
        for im_type in self.image_types:
            for im_size in self.sizes:
                variants = []
                for im_dens in self.image_densities:
                    size_str = '{}-{}'.format(im_size.scaling_type,
                                              'x'.join(str(d * im_dens) for d in im_size.dimensions))
                    variants.append(SizeAndDensity(size_str, im_dens))
                renders.append(ImageRenderSourceSet(variants, im_type, im_size.min_page_width_px))
        return renders


class ImagePresets(Enum):
    PAGE_HEADER = ImageRenderPreset([
        ImageSizeSelector(PageBreakpointsPx.fhd, 'max', 2560, 600),
        ImageSizeSelector(PageBreakpointsPx.laptop, 'max', 1920, 600),
        ImageSizeSelector(PageBreakpointsPx.tablet_landscape, 'max', 1366, 600),
        ImageSizeSelector(PageBreakpointsPx.zero, 'max', 768, 600),
    ], ('max-1920x600' + ImageType.JPG.value[0]))

    PAGE_FOOTER = ImageRenderPreset([
        ImageSizeSelector(PageBreakpointsPx.fhd, 'max', 2560, 200),
        ImageSizeSelector(PageBreakpointsPx.laptop, 'max', 1920, 200),
        ImageSizeSelector(PageBreakpointsPx.tablet_landscape, 'max', 1366, 200),
        ImageSizeSelector(PageBreakpointsPx.zero, 'max', 768, 200),
    ], ('max-1920x600' + ImageType.JPG.value[0]))

    THEME_HEADER = ImageRenderPreset([
        ImageSizeSelector(PageBreakpointsPx.fhd, 'max', 1280, 600),
        ImageSizeSelector(PageBreakpointsPx.laptop, 'max', 960, 600),
        ImageSizeSelector(PageBreakpointsPx.tablet_landscape, 'max', 1366, 600),
        ImageSizeSelector(PageBreakpointsPx.zero, 'max', 768, 600),
    ], ('max-1920x600' + ImageType.JPG.value[0]))
