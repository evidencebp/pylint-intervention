import base64
import math
import struct

import numpy as np

from .common import text2png, create_surface, line_segments, create_line
from . import common

GLTF_ELEMENT_ARRAY_BUFFER = 34963
GLTF_ARRAY_BUFFER = 34962
GLTF_TYPE_UNSIGNED_SHORT = 5123
GLTF_TYPE_UNSIGNED_INT = 5125
GLTF_TYPE_FLOAT = 5126
GLTF_WRAP_MIRRORED_REPEAT = 33648
GLTF_MINFILTER_LINEAR_MIPMAP_LINEAR = 9987
GLTF_MAGFILTER_LINEAR = 9729

# For more documentation look e.g. at:
# https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png
class GLTF(object):
    def __init__(self):
        self.d = {
            "asset" : {"version" : "2.0"}
        }
        for i in ['scenes', 'nodes', 'meshes', 'buffers', 'bufferViews', 'accessors', 'materials', 'textures', 'samplers', 'images', ]:
            self.d[i] = []
    def add(self, path, x):
        lst = self.d.get(path)
        id = len(lst)
        lst.append(x)
        return id

    def add_buffer_data(self, arrays, target, type, remove_view_target=False):
        # GLTF spec says little-endian
        buffer_format = "<"
        acc_id = []
        byte_offset = 0
        buffer_dict = {}
        b_id = self.add('buffers', buffer_dict)
        for x, tg, tp in zip(arrays, target, type):
            if tg == GLTF_ELEMENT_ARRAY_BUFFER:
                if max(x) < 2**16:
                    bin_format = GLTF_TYPE_UNSIGNED_SHORT
                    arr_format = "H"
                else:
                    bin_format = GLTF_TYPE_UNSIGNED_INT
                    arr_format = "I"
            else:
                bin_format = GLTF_TYPE_FLOAT
                arr_format = "f"
            arr_format = f"{len(x)}{arr_format}"
            buffer_format += arr_format
            n = struct.calcsize(arr_format)
            view_id = self.add('bufferViews', {
                    "buffer": b_id,
                    "byteOffset": byte_offset,
                    "byteLength": n,
                    "target": tg
                })
            if remove_view_target:
                del self.d['bufferViews'][view_id]['target']
            byte_offset += n
            if tp == 'SCALAR':
                dim = 1
                component_type = bin_format
            else:
                dim = int(tp[-1])
                component_type = GLTF_TYPE_FLOAT
            arr = np.array(x).reshape((-1,dim))
            acc_id.append(self.add("accessors", {
                "bufferView": view_id,
                "byteOffset": 0,
                "componentType": component_type,
                "count": len(x) // dim,
                "type": tp,
                "max": arr.max(0).tolist(),
                "min": arr.min(0).tolist(),
            }))
        buffer = struct.pack(buffer_format, *sum(arrays, []))
        buffer_url = "data:application/octet-stream;base64," + base64.b64encode(buffer).decode("ASCII")
        buffer_dict["uri"] = buffer_url
        buffer_dict["byteLength"] = len(buffer)

        return acc_id

def data2gltf(data, subdiv=16):

    COLORS = data['color_palette'] if "color_palette" in data else common.COLORS
    COLORS_LEN = len(COLORS)
    meters_per_unit = float(data.get('meters_per_unit', 0.1))

    gltf = GLTF()
    indices, vertices, normals = create_sphere(subdiv=subdiv)
    sphere_acc_id = gltf.add_buffer_data(
        [indices, vertices, normals],
        [GLTF_ELEMENT_ARRAY_BUFFER, GLTF_ARRAY_BUFFER, GLTF_ARRAY_BUFFER],
        "SCALAR VEC3 VEC3".split(),
    )
    arrow_radius = 0.01
    indices, vertices, normals = create_rotation(
        [(0,arrow_radius),(1-2*arrow_radius,arrow_radius),(1-2*arrow_radius,2*arrow_radius)], subdiv=subdiv)
    arrow_acc_id = gltf.add_buffer_data(
        [indices, vertices, normals],
        [GLTF_ELEMENT_ARRAY_BUFFER, GLTF_ARRAY_BUFFER, GLTF_ARRAY_BUFFER],
        "SCALAR VEC3 VEC3".split(),
    )
    grey_mat_id = gltf.add("materials", {
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.5,0.5,0.5,1.0],
            "metallicFactor": 0.1,
            "roughnessFactor": 0.4,
        },
        "doubleSided": True,
    })
    arrow_mesh_id = gltf.add("meshes", {
                "primitives": [{
                    "attributes": {
                        "POSITION": arrow_acc_id[1],
                        "NORMAL": arrow_acc_id[2],
                    },
                    "indices": arrow_acc_id[0],
                    "material": grey_mat_id
                }]
            })

    indices, vertices, normals, st = create_board()
    board_acc_id = gltf.add_buffer_data(
        [indices, vertices, normals, st],
        [GLTF_ELEMENT_ARRAY_BUFFER, GLTF_ARRAY_BUFFER, GLTF_ARRAY_BUFFER, GLTF_ARRAY_BUFFER],
        "SCALAR VEC3 VEC3 VEC2".split(),
    )
    sampler_id = gltf.add('samplers', {
            "magFilter": GLTF_MAGFILTER_LINEAR,
            "minFilter": GLTF_MINFILTER_LINEAR_MIPMAP_LINEAR,
            "wrapS": GLTF_WRAP_MIRRORED_REPEAT,
            "wrapT": GLTF_WRAP_MIRRORED_REPEAT
        })

    col_mat_ids = [ gltf.add("materials", {
                "pbrMetallicRoughness": {
                    "baseColorFactor": list(col) + [1.0],
                    "metallicFactor": 0.5,
                    "roughnessFactor": 0.1
                }
            })
            for col in COLORS
        ]
    col_mesh_id = [ gltf.add("meshes", {
                "primitives": [{
                    "attributes": {
                        "POSITION": sphere_acc_id[1],
                        "NORMAL": sphere_acc_id[2],
                    },
                    "indices": sphere_acc_id[0],
                    "material": mat_id
                }]
            })
            for mat_id in col_mat_ids
        ]

    data_node = dict(children=[])
    data_node_id = gltf.add('nodes', data_node)
    legend_node = dict(children=[], translation=[1,0,-1])
    legend_node_id = gltf.add('nodes', legend_node)
    axes_node = dict(children=[])  if 'axis_names' in data else {}
    axes_node_id = gltf.add('nodes', axes_node)

    animation = False
    if 'animation' in data:
        animation = data['animation']
        end_time_code = len(animation.get('time_labels')) - 1
        start_time_code = 0
        time_codes_per_second = animation.get('time_codes_per_second', 24)
        animation_input = np.arange(end_time_code+1) / time_codes_per_second
        animation_outputs = [
            np.array(_).reshape((-1, )).tolist()
            for _ in animation.get('data',[])
        ]
        animation_input_acc_id, *animation_output_acc_ids = gltf.add_buffer_data(
            [animation_input.tolist()] + animation_outputs,
            [GLTF_ARRAY_BUFFER] + [GLTF_ARRAY_BUFFER] * len(animation_outputs),
            ["SCALAR"] + ["VEC3"] * len(animation_outputs),
            remove_view_target=True,
        )
        animation_channels = []
        animation_samplers = []
        gltf.d["animations"] = [ dict(channels=animation_channels, samplers=animation_samplers) ]

    for i, row in enumerate(data.get('data', []) if data.get('type') != 'l' else []):
        x, y, z = row[:3]
        col = 0
        scale = 0.01
        if 'col' in data:
            col = data['col'][i] % COLORS_LEN
        if 'size' in data:
            scale *= data['size'][i]
        scale = [scale] * 3
        mesh_id = col_mesh_id[col]
        if 'label' in data:
            text = data['label'][i]
            h, w, img = text2png(text, color=COLORS[col])
            img_uri = "data:image/png;base64," + base64.b64encode(img).decode("ASCII")
            src_id = gltf.add("images", {
                "uri": img_uri
            })
            texture_id = gltf.add("textures", {
                "sampler": sampler_id,
                "source": src_id
            })
            mat_id = gltf.add('materials', {
                    "pbrMetallicRoughness": {
                        "baseColorTexture": {"index": texture_id},
                        "metallicFactor": 0.5,
                        "roughnessFactor": 0.1,
                    },
                    "alphaMode": "BLEND",
                    "doubleSided": True,
                })
            mesh_id = gltf.add('meshes',
                {
                    "primitives": [{
                        "attributes": {
                            "POSITION": board_acc_id[1],
                            "NORMAL": board_acc_id[2],
                            "TEXCOORD_0": board_acc_id[3],
                        },
                        "indices": board_acc_id[0],
                        "material": mat_id
                    }]
                })
            scale = [scale[0] * h, scale[1] * w, scale[2] ]
        current_node_id = gltf.add('nodes', {"mesh": mesh_id, "translation": [x, z, -y], "scale": scale, })
        data_node['children'].append(current_node_id)

        if animation:
            animation_samplers.append(dict(
                input=animation_input_acc_id,
                interpolation="LINEAR",
                output=animation_output_acc_ids[i],
            ))
            animation_channels.append(dict(
                target=dict(node=current_node_id, path='translation'),
                sampler=len(animation_samplers)-1,
            ))

    if 'surface' in data:
        surface = data['surface']
        indices, normals, vertices = create_surface(surface)
        surface_acc_id = gltf.add_buffer_data(
            [ _.flatten().tolist() for _ in [indices, vertices, normals] ],
            [GLTF_ELEMENT_ARRAY_BUFFER, GLTF_ARRAY_BUFFER, GLTF_ARRAY_BUFFER],
            "SCALAR VEC3 VEC3".split(),
        )
        mesh_id = gltf.add('meshes',
            {
                "primitives": [{
                    "attributes": {
                        "POSITION": surface_acc_id[1],
                        "NORMAL": surface_acc_id[2],
                        # "TEXCOORD_0": surface_acc_id[3],
                    },
                    "indices": surface_acc_id[0],
                    "material": grey_mat_id
                }]
            })
        data_node['children'].append(gltf.add('nodes', {
          "mesh" : mesh_id,
          # "translation": [x,z,-y],
          # "scale": scale,
        }))

    if 'lines' in data and 'data' in data:
        for i, line in enumerate(data['lines']):
            data_list = data.get('data', [])
            line_width = line.get('width', 1) / 500
            indices, vertices, normals = create_line(data_list, line, radius=line_width)
            line_acc_id = gltf.add_buffer_data(
                [indices, vertices, normals],
                [GLTF_ELEMENT_ARRAY_BUFFER, GLTF_ARRAY_BUFFER, GLTF_ARRAY_BUFFER],
                "SCALAR VEC3 VEC3".split(),
            )
            mat_id = col_mat_ids[ line.get('col', 0) % COLORS_LEN ]
            # n = len(data_list)
            mesh_id = gltf.add('meshes',
                {
                    "primitives": [{
                        "attributes": {
                            "POSITION": line_acc_id[1],
                            "NORMAL": line_acc_id[2],
                        },
                        "indices": line_acc_id[0],
                        "material": mat_id
                    }]
                })
            # for t,q,s in line_segments(data_list, line, n, flip_vector=True):
            #     data_node['children'].append(gltf.add('nodes', {
            #         "mesh": mesh_id,
            #         "translation": t,
            #         "scale": [1,s,1],
            #         "rotation": q,
            #     }))
                data_node['children'].append(gltf.add('nodes', {
                    "mesh": mesh_id,
                }))

    for i, text in enumerate(data.get('col_labels',[])):
        col = i % COLORS_LEN
        scale = [0.01] * 3
        x, y, z = 0,0,1-i*scale[1]*10
        h, w, img = text2png(text, color=COLORS[col])
        img_uri = "data:image/png;base64," + base64.b64encode(img).decode("ASCII")
        src_id = gltf.add("images", {
            "uri": img_uri
        })
        texture_id = gltf.add("textures", {
            "sampler": sampler_id,
            "source": src_id
        })
        mat_id = gltf.add('materials', {
                "pbrMetallicRoughness": {
                    "baseColorTexture": {"index": texture_id},
                    "metallicFactor": 0.5,
                    "roughnessFactor": 0.1,
                },
                "alphaMode": "BLEND",
                "doubleSided": True,
            })
        mesh_id = gltf.add('meshes',
            {
                "primitives": [{
                    "attributes": {
                        "POSITION": board_acc_id[1],
                        "NORMAL": board_acc_id[2],
                        "TEXCOORD_0": board_acc_id[3],
                    },
                    "indices": board_acc_id[0],
                    "material": mat_id
                }]
            })
        scale = [scale[0] * h, scale[1] * w, scale[2] ]
        legend_node['children'].append(gltf.add('nodes', {
          "mesh" : mesh_id,
          "translation": [x,z,-y],
          "scale": scale,
        }))
        # the sphere
        legend_node['children'].append(gltf.add('nodes', {
          "mesh" : col_mesh_id[col],
          "translation": [x-0.04,z+scale[1]/2,-y],
          "scale": [0.02] * 3,
        }))
    for i, text in enumerate(data.get('axis_names',[])):
        scale = [0.01] * 3
        translation = [0,0,0]
        translation[(2*i) % 3] = -1 if i==1 else 1
        rotation = [0,0,0,0]
        if i<2:
            rotation[0] = math.sqrt(2)/2 * (1-2*i)
            rotation[1 if i==0 else 3] = math.sqrt(2)/2
        else:
            rotation[1] = -1
        h, w, img = text2png(text, color=COLORS[0])
        img_uri = "data:image/png;base64," + base64.b64encode(img).decode("ASCII")
        src_id = gltf.add("images", {
            "uri": img_uri
        })
        texture_id = gltf.add("textures", {
            "sampler": sampler_id,
            "source": src_id
        })
        mat_id = gltf.add('materials', {
                "pbrMetallicRoughness": {
                    "baseColorTexture": {"index": texture_id},
                    "metallicFactor": 0.5,
                    "roughnessFactor": 0.1,
                },
                "alphaMode": "BLEND",
                "doubleSided": True,
            })
        mesh_id = gltf.add('meshes',
            {
                "primitives": [{
                    "attributes": {
                        "POSITION": board_acc_id[1],
                        "NORMAL": board_acc_id[2],
                        "TEXCOORD_0": board_acc_id[3],
                    },
                    "indices": board_acc_id[0],
                    "material": mat_id
                }]
            })
        scale = [scale[0] * h, scale[1] * w, scale[2] ]
        axes_node['children'].append(gltf.add('nodes', {
          "mesh" : mesh_id,
          "translation": translation,
          "scale": scale,
        }))
        axes_node['children'].append(gltf.add('nodes', {
          "mesh" : arrow_mesh_id,
          # "translation": [i,0,0],
          "rotation": rotation,
          # "scale": scale,
        }))
    root_node_id = gltf.add('nodes', {
        "children": [data_node_id, legend_node_id, axes_node_id],
        "scale": [meters_per_unit]*3,
    })
    gltf.add("scenes", {
          "nodes" : [ root_node_id, ]
        })
    return gltf.d


def create_board(subdiv=8):
    vertices = [ 0,0,0, 1,0,0, 1,1,0, 0,1,0 ]
    indices = [ 0,1,2 , 0,2,3 ]
    normals = [ 0,0,1 ] * (len(vertices) // 3)
    st = [ 0,1, 1,1, 1,0, 0,0 ]
    return indices, vertices, normals, st

def create_sphere(subdiv=8):
    """
    Divide into subdiv latitudinal stripes of 2*subdiv trapeces, and each into 2 triangles.
    :param subdiv:
    :return:
    """
    vertices = [] #[0.0,0.0,0.0] * ((subdiv-1)*(subdiv * 2)+2)
    # normals = [0.0] * len(vertices)
    indices = [] # [0,0,0] * ( subdiv * 2*subdiv * 2 )
    coord2index = []
    # calculate vertices and normals:
    i = 0
    vertices += [0,-1,0] # south pole
    coord2index.append([i])
    i += 1
    for lat in range(1,subdiv):
        alpha = math.pi * (lat / (subdiv)-0.5)
        y = math.sin(alpha)
        radius_lat = math.cos(alpha)
        coords = []
        for lon in range(2*subdiv):
            beta = math.pi * lon / subdiv
            x = math.sin(beta) * radius_lat
            z = math.cos(beta) * radius_lat
            vertices += [x,y,z]
            coords.append(i)
            i+=1
        coord2index.append(coords)
    vertices += [0,1,0] # north pole
    coord2index.append([i])
    # create triangles
    for lat in range(0,subdiv):
        a = coord2index[lat]
        if len(a) == 1:
            a = a*2*subdiv
        b = coord2index[lat+1]
        if len(b) == 1:
            b = b*2*subdiv
        for lon in range(2*subdiv):
            lon1 = (lon + 1) % (2*subdiv)
            if b[lon] != b[lon1]:
                indices += [ a[lon] , b[lon], b[lon1]]
            if a[lon] != a[lon1]:
                indices += [ b[lon1], a[lon1], a[lon] ]
    # in a sphere of radius 1 the vertices are also their normals
    normals = vertices
    return indices, vertices, normals

def create_rotation(profile, z_from_to=[0,1], subdiv=8):
    """
    Divide into subdiv latitudinal stripes of 2*subdiv trapeces, and each into 2 triangles.
    :param subdiv:
    :return:
    """
    vertices = [] #[0.0,0.0,0.0] * ((subdiv-1)*(subdiv * 2)+2)
    normals = []
    # normals = [0.0] * len(vertices)
    indices = [] # [0,0,0] * ( subdiv * 2*subdiv * 2 )
    coord2index = []
    # calculate vertices and normals:
    i = 0
    vertices += [0,z_from_to[0],0] # south pole
    normals += [0.0,-1.0,0.0]
    coord2index.append([i])
    i += 1
    for lat,(y,radius_lat)  in enumerate(profile):
        coords = []
        for lon in range(2*subdiv):
            beta = math.pi * lon / subdiv
            x = math.sin(beta) * radius_lat
            z = math.cos(beta) * radius_lat
            vertices += [x,y,z]
            normals += [x / math.sqrt(x**2+z**2), 0.0, z / math.sqrt(x**2+z**2)]
            coords.append(i)
            i+=1
        coord2index.append(coords)
    vertices += [0,z_from_to[1],0] # north pole
    normals += [0.0,1.0,0.0]
    coord2index.append([i])
    # create triangles
    for lat in range(len(profile)+1):
        a = coord2index[lat]
        if len(a) == 1:
            a = a*2*subdiv
        b = coord2index[lat+1]
        if len(b) == 1:
            b = b*2*subdiv
        for lon in range(2*subdiv):
            lon1 = (lon + 1) % (2*subdiv)
            if b[lon] != b[lon1]:
                indices += [ b[lon], a[lon], b[lon1]]
            if a[lon] != a[lon1]:
                indices += [ a[lon1], b[lon1], a[lon] ]
    return indices, vertices, normals
