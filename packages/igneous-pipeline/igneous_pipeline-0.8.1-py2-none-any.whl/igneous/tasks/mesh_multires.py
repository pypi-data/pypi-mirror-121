from typing import Optional

from collections import defaultdict

import json
import math
import os
import random
import re
import struct

import numpy as np
from tqdm import tqdm

from cloudfiles import CloudFiles

from cloudvolume import CloudVolume, view
from cloudvolume.lib import Vec, Bbox, jsonify
import mapbuffer
from mapbuffer import MapBuffer
from taskqueue import queueable

import cc3d
import DracoPy
import fastremap
import zmesh



# chunk_shape: 3x float32le, specifies the x, y, and z extents 
#     of finest octree node in the "stored model" coordinate space.
# grid_origin: 3x float32le, specifies the x, y, and z origin of the octree decomposition in the "stored model" coordinate space.
# num_lods: uint32le, specifies the number of levels of detail.
# lod_scales: num_lods float32le, specifies the scale in "stored model" spatial units corresponding to each level of detail. Each scale value is multiplied by the lod_scale_multiplier value from the info JSON file.
# vertex_offsets: num_lods*3 float32le, as a C order [vertex_offsets, 3] array specifying an offset (in the "stored model" coordinate space) to add to vertex positions for each level of detail.
# num_fragments_per_lod: num_lods uint32le, specifies the number of fragments (octree nodes) for each level of detail.
# For each lod in the range [0, num_lods):
#     fragment_positions: num_fragments_per_lod[lod]*3 uint32le, C order [3, numFragments_per_lod[lod]] array specifying the x, y, and z coordinates of the octree nodes for the given lod. The node positions must be in x, y, z Z-curve order. The node corresponds to the axis-aligned bounding box within the "stored model" coordinate space with an origin of: grid_origin + [x, y, z] * chunk_shape * (2**lod) and a shape of chunk_shape * (2**lod).
#     fragment_offfsets: ``num_fragments_per_lod[lod]uint32le, specifies the size in bytes of the encoded mesh fragment in the [mesh fragment data file](#multi-resolution-mesh-fragment-data-file-format) corresponding to each octree node in thefragment_positions` array. The starting offset of the encoded mesh data corresponding to a given octree node is equal to the sum of all prior `fragment_positions` values.

def create_multires_manifest(
  chunk_shape:tuple, grid_origin:tuple, 
  num_lods:int, lods_scales:list,
  vertex_offsets:list, num_fragments_per_lod:list,
  fragment_positions, fragment_offsets,
):
  chunk_shape = np.array(chunk_shape, dtype=np.float32)
  grid_origin = np.array(grid_origin, dtype=np.float32)
  
    grid_origin.astype('<f').tobytes()
    struct.pack('<I', num_lods)
    lod_scales.astype('<f').tobytes()
    vertex_offsets.astype('<f').tobytes(order='C')
    num_fragments_per_lod.astype('<I').tobytes()

    for frag_pos, frag_offset in zip(fragment_positions, fragment_offsets):
        manifestdata.write(frag_pos.T.astype('<I').tobytes(order='C'))
        manifestdata.write(frag_offset.astype('<I').tobytes(order='C'))






@queueable
def MultiResMeshTask(
  cloudpath:str, shape:tuple, offset:tuple, 
  cache_control:bool = False,
  draco_compression_level:int = 1,
  draco_create_metadata:bool = False,
  dust_threshold:Optional[int] = None,
  encoding:str = 'precomputed',
  fill_missing:bool = False,
  max_simplification_error:int = kwargs.get('max_simplification_error', 40),
  simplification_factor:int = kwargs.get('simplification_factor', 100),
  mesh_dir:Optional[str] = None,
  # mip = kwargs.get('mip', 0),
  progress = kwargs.get('progress', False),
  remap_table = kwargs.get('remap_table', None),
  spatial_index:bool = False,
  # sharded:bool = kwargs.get('sharded', False),
  timestamp:Optional[int] = None,
  agglomerate:Optional[bool] = True,
  stop_layer:Optional[int] = kwargs.get('stop_layer', 2),
  compress:str = 'gzip',
):