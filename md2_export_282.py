# ***** BEGIN GPL LICENSE BLOCK *****

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Export .md2",
    "description": "Export to Quake2 file format, applies modifiers (.md2)",
    "author": "Sebastian Lieberknecht, Dao Nguyen and Bernd Meyer metaio GmbH (based on Damien Thebault and Erwan Mathieu's Blender2.4x exporter)",
    "version": (1, 7, 1),
    "blender": (2, 82, 0),
    "location": "File > Export > md2",
    "warning": '',  # used for warning icon and text in addons panel
    "wiki_url": "http://metaio.com",
    "tracker_url": "http://metaio.com",
    "category": "Import-Export"}

import bpy

from bpy_extras.io_utils import ExportHelper

from math import pi
import mathutils

import struct
import random
import os
import shutil

MD2_NORMALS = ((-0.525731, 0.000000, 0.850651),
               (-0.442863, 0.238856, 0.864188),
               (-0.295242, 0.000000, 0.955423),
               (-0.309017, 0.500000, 0.809017),
               (-0.162460, 0.262866, 0.951056),
               (0.000000, 0.000000, 1.000000),
               (0.000000, 0.850651, 0.525731),
               (-0.147621, 0.716567, 0.681718),
               (0.147621, 0.716567, 0.681718),
               (0.000000, 0.525731, 0.850651),
               (0.309017, 0.500000, 0.809017),
               (0.525731, 0.000000, 0.850651),
               (0.295242, 0.000000, 0.955423),
               (0.442863, 0.238856, 0.864188),
               (0.162460, 0.262866, 0.951056),
               (-0.681718, 0.147621, 0.716567),
               (-0.809017, 0.309017, 0.500000),
               (-0.587785, 0.425325, 0.688191),
               (-0.850651, 0.525731, 0.000000),
               (-0.864188, 0.442863, 0.238856),
               (-0.716567, 0.681718, 0.147621),
               (-0.688191, 0.587785, 0.425325),
               (-0.500000, 0.809017, 0.309017),
               (-0.238856, 0.864188, 0.442863),
               (-0.425325, 0.688191, 0.587785),
               (-0.716567, 0.681718, -0.147621),
               (-0.500000, 0.809017, -0.309017),
               (-0.525731, 0.850651, 0.000000),
               (0.000000, 0.850651, -0.525731),
               (-0.238856, 0.864188, -0.442863),
               (0.000000, 0.955423, -0.295242),
               (-0.262866, 0.951056, -0.162460),
               (0.000000, 1.000000, 0.000000),
               (0.000000, 0.955423, 0.295242),
               (-0.262866, 0.951056, 0.162460),
               (0.238856, 0.864188, 0.442863),
               (0.262866, 0.951056, 0.162460),
               (0.500000, 0.809017, 0.309017),
               (0.238856, 0.864188, -0.442863),
               (0.262866, 0.951056, -0.162460),
               (0.500000, 0.809017, -0.309017),
               (0.850651, 0.525731, 0.000000),
               (0.716567, 0.681718, 0.147621),
               (0.716567, 0.681718, -0.147621),
               (0.525731, 0.850651, 0.000000),
               (0.425325, 0.688191, 0.587785),
               (0.864188, 0.442863, 0.238856),
               (0.688191, 0.587785, 0.425325),
               (0.809017, 0.309017, 0.500000),
               (0.681718, 0.147621, 0.716567),
               (0.587785, 0.425325, 0.688191),
               (0.955423, 0.295242, 0.000000),
               (1.000000, 0.000000, 0.000000),
               (0.951056, 0.162460, 0.262866),
               (0.850651, -0.525731, 0.000000),
               (0.955423, -0.295242, 0.000000),
               (0.864188, -0.442863, 0.238856),
               (0.951056, -0.162460, 0.262866),
               (0.809017, -0.309017, 0.500000),
               (0.681718, -0.147621, 0.716567),
               (0.850651, 0.000000, 0.525731),
               (0.864188, 0.442863, -0.238856),
               (0.809017, 0.309017, -0.500000),
               (0.951056, 0.162460, -0.262866),
               (0.525731, 0.000000, -0.850651),
               (0.681718, 0.147621, -0.716567),
               (0.681718, -0.147621, -0.716567),
               (0.850651, 0.000000, -0.525731),
               (0.809017, -0.309017, -0.500000),
               (0.864188, -0.442863, -0.238856),
               (0.951056, -0.162460, -0.262866),
               (0.147621, 0.716567, -0.681718),
               (0.309017, 0.500000, -0.809017),
               (0.425325, 0.688191, -0.587785),
               (0.442863, 0.238856, -0.864188),
               (0.587785, 0.425325, -0.688191),
               (0.688191, 0.587785, -0.425325),
               (-0.147621, 0.716567, -0.681718),
               (-0.309017, 0.500000, -0.809017),
               (0.000000, 0.525731, -0.850651),
               (-0.525731, 0.000000, -0.850651),
               (-0.442863, 0.238856, -0.864188),
               (-0.295242, 0.000000, -0.955423),
               (-0.162460, 0.262866, -0.951056),
               (0.000000, 0.000000, -1.000000),
               (0.295242, 0.000000, -0.955423),
               (0.162460, 0.262866, -0.951056),
               (-0.442863, -0.238856, -0.864188),
               (-0.309017, -0.500000, -0.809017),
               (-0.162460, -0.262866, -0.951056),
               (0.000000, -0.850651, -0.525731),
               (-0.147621, -0.716567, -0.681718),
               (0.147621, -0.716567, -0.681718),
               (0.000000, -0.525731, -0.850651),
               (0.309017, -0.500000, -0.809017),
               (0.442863, -0.238856, -0.864188),
               (0.162460, -0.262866, -0.951056),
               (0.238856, -0.864188, -0.442863),
               (0.500000, -0.809017, -0.309017),
               (0.425325, -0.688191, -0.587785),
               (0.716567, -0.681718, -0.147621),
               (0.688191, -0.587785, -0.425325),
               (0.587785, -0.425325, -0.688191),
               (0.000000, -0.955423, -0.295242),
               (0.000000, -1.000000, 0.000000),
               (0.262866, -0.951056, -0.162460),
               (0.000000, -0.850651, 0.525731),
               (0.000000, -0.955423, 0.295242),
               (0.238856, -0.864188, 0.442863),
               (0.262866, -0.951056, 0.162460),
               (0.500000, -0.809017, 0.309017),
               (0.716567, -0.681718, 0.147621),
               (0.525731, -0.850651, 0.000000),
               (-0.238856, -0.864188, -0.442863),
               (-0.500000, -0.809017, -0.309017),
               (-0.262866, -0.951056, -0.162460),
               (-0.850651, -0.525731, 0.000000),
               (-0.716567, -0.681718, -0.147621),
               (-0.716567, -0.681718, 0.147621),
               (-0.525731, -0.850651, 0.000000),
               (-0.500000, -0.809017, 0.309017),
               (-0.238856, -0.864188, 0.442863),
               (-0.262866, -0.951056, 0.162460),
               (-0.864188, -0.442863, 0.238856),
               (-0.809017, -0.309017, 0.500000),
               (-0.688191, -0.587785, 0.425325),
               (-0.681718, -0.147621, 0.716567),
               (-0.442863, -0.238856, 0.864188),
               (-0.587785, -0.425325, 0.688191),
               (-0.309017, -0.500000, 0.809017),
               (-0.147621, -0.716567, 0.681718),
               (-0.425325, -0.688191, 0.587785),
               (-0.162460, -0.262866, 0.951056),
               (0.442863, -0.238856, 0.864188),
               (0.162460, -0.262866, 0.951056),
               (0.309017, -0.500000, 0.809017),
               (0.147621, -0.716567, 0.681718),
               (0.000000, -0.525731, 0.850651),
               (0.425325, -0.688191, 0.587785),
               (0.587785, -0.425325, 0.688191),
               (0.688191, -0.587785, 0.425325),
               (-0.955423, 0.295242, 0.000000),
               (-0.951056, 0.162460, 0.262866),
               (-1.000000, 0.000000, 0.000000),
               (-0.850651, 0.000000, 0.525731),
               (-0.955423, -0.295242, 0.000000),
               (-0.951056, -0.162460, 0.262866),
               (-0.864188, 0.442863, -0.238856),
               (-0.951056, 0.162460, -0.262866),
               (-0.809017, 0.309017, -0.500000),
               (-0.864188, -0.442863, -0.238856),
               (-0.951056, -0.162460, -0.262866),
               (-0.809017, -0.309017, -0.500000),
               (-0.681718, 0.147621, -0.716567),
               (-0.681718, -0.147621, -0.716567),
               (-0.850651, 0.000000, -0.525731),
               (-0.688191, 0.587785, -0.425325),
               (-0.587785, 0.425325, -0.688191),
               (-0.425325, 0.688191, -0.587785),
               (-0.425325, -0.688191, -0.587785),
               (-0.587785, -0.425325, -0.688191),
               (-0.688191, -0.587785, -0.425325))


class MD2Header:
    def __init__(self, skins, meshes, num_frames):
        self.version = 8

        self.skin_width = 2 ** 10 - 1  # 1023
        self.skin_height = 2 ** 10 - 1  # 1023

        self.num_skins = len(skins)
        self.num_xyz = 0
        self.num_st = 0
        self.num_tris = 0
        for mesh in meshes:
            self.num_xyz += len(mesh.vertices)
            self.num_st += len(mesh.loop_triangles) * 3
            self.num_tris += len(mesh.loop_triangles)
        print(self.num_tris)
        self.num_gl_commands = self.num_tris * (1 + 3 * 3) + 1

        self.num_frames = num_frames

        self.frame_size = 40 + 4 * self.num_xyz

        self.ofs_skins = 68  # size of the header
        self.ofs_st = self.ofs_skins + 64 * self.num_skins
        self.ofs_tris = self.ofs_st + 4 * self.num_st
        self.ofs_frames = self.ofs_tris + 12 * self.num_tris
        self.ofs_gl_commands = self.ofs_frames + self.frame_size * self.num_frames
        self.ofs_end = self.ofs_gl_commands + 4 * self.num_gl_commands

    def write(self, file):
        # write header
        pack = struct.pack('<4B16i',  # bin = struct.pack('<4s16i',
                           ord('I'),
                           ord('D'),
                           ord('P'),
                           ord('2'),
                           self.version,
                           self.skin_width,
                           self.skin_height,
                           self.frame_size,
                           self.num_skins,
                           self.num_xyz,
                           self.num_st,  # number of texture coordinates
                           self.num_tris,
                           self.num_gl_commands,
                           self.num_frames,
                           self.ofs_skins,
                           self.ofs_st,
                           self.ofs_tris,
                           self.ofs_frames,
                           self.ofs_gl_commands,
                           self.ofs_end)
        file.write(pack)


# noinspection PyBroadException
class MD2:
    def __init__(self, options, objects, scale=1.0):
        self.options = options
        self.objects = objects
        self.scale = scale
        self.bbox_min = None
        self.bbox_max = None
        return

    def pre_compute_bbox(self, header):
        # Since position are computed (integers value between 0-255 then multiplied by scale stored in frame)
        # In cas of animated object with fixed point, fixed point will move a bit each frame. By using the same
        # bbox it fixes the problem and give more smooth items
        bbox_min = None
        bbox_max = None

        for frame in range(1, header.num_frames + 1):
            bpy.context.scene.frame_set(frame)
            for obj in self.objects:
                mesh = obj.to_mesh(preserve_all_data_layers=True)
                mesh.transform(obj.matrix_world)
                mesh.transform(mathutils.Matrix.Rotation(-pi / 2, 4, 'Z'))
                (bbox_min, bbox_max) = Util.compute_bounding_box(mesh, bbox_min, bbox_max)

        self.bbox_min = bbox_min
        self.bbox_max = bbox_max

    def write(self, filename):
        meshes = [obj.data for obj in self.objects]
        print(meshes)
        skins = Util.get_skins(self.objects)

        num_frames = 1
        if self.options.fExportAnimation:
            num_frames = 1 + bpy.context.scene.frame_end - bpy.context.scene.frame_start

        header = MD2Header(skins, meshes, num_frames)

        file = open(filename, 'wb')
        try:
            header.write(file)

            self.write_skins(file, filename, skins)
            for mesh in meshes:
                self.write_texture_coordinates(file, header, mesh)
            self.write_triangles(file, meshes)

            if self.options.fExportAnimation:
                time_line_markers = []
                for marker in bpy.context.scene.timeline_markers:
                    time_line_markers.append(marker)

                # sort the markers. The marker with the frame number closest to 0 will be the first marker in the list.
                # The marker with the biggest frame number will be the last marker in the list
                time_line_markers.sort(key=lambda marker: marker.frame)
                marker_idx = 0

                # delete markers at same frame positions
                if len(time_line_markers) > 1:
                    marker_frame = time_line_markers[len(time_line_markers) - 1].frame
                    for i in range(len(time_line_markers) - 2, -1, -1):
                        if time_line_markers[i].frame == marker_frame:
                            del time_line_markers[i]
                        else:
                            marker_frame = time_line_markers[i].frame

                # BL: to fix: 1 is assumed to be the frame start (this is
                # hardcoded sometimes...)

                if self.options.useSameBoundingBox:
                    self.pre_compute_bbox(header)

                for frame in range(1, header.num_frames + 1):
                    bpy.context.scene.frame_set(frame)

                    if len(time_line_markers) != 0:
                        if marker_idx + 1 != len(time_line_markers):
                            if frame >= time_line_markers[marker_idx + 1].frame:
                                marker_idx += 1
                        name = time_line_markers[marker_idx].name
                    else:
                        name = 'frame'

                    self.write_frame(file, name + str(frame))
            else:
                self.write_frame(file)

            for mesh in meshes:
                self.write_gl_commands(file, mesh)
        finally:
            file.close()

    @staticmethod
    def write_gl_commands(file, mesh):
        for tri in mesh.loop_triangles:  # for face in mesh.faces:
            uvs = []
            for loop_index in tri.loops:
                try:
                    uv = mesh.uv_layers[0].data[loop_index].uv
                except:
                    uv = [0, 0]
                uvs.append(uv)

            pack = struct.pack('<i', 3)
            file.write(pack)
            # 0,2,1 for good cw/ccw (also flips/inverts normal)
            for vert in [0, 2, 1]:
                # (u,v) in blender -> (u,1-v)
                pack = struct.pack('<ffI',
                                   uvs[vert][0],
                                   (1.0 - uvs[vert][1]),
                                   tri.vertices[vert])

                file.write(pack)
        # NULL command
        pack = struct.pack('<I', 0)
        file.write(pack)

    @staticmethod
    def write_triangles(file, meshes):
        vertices_index = 0
        faces_index = 0
        for mesh in meshes:
            for face in mesh.loop_triangles:
                # 0,2,1 for good cw/ccw
                pack = struct.pack('<3H',
                                   vertices_index + face.vertices[0],
                                   vertices_index + face.vertices[2],
                                   vertices_index + face.vertices[1]
                                   )
                file.write(pack)  # vert index
                pack = struct.pack('<3H',
                                   (faces_index + face.index) * 3 + 0,
                                   (faces_index + face.index) * 3 + 2,
                                   (faces_index + face.index) * 3 + 1,
                                   )

                file.write(pack)  # uv index
            vertices_index += len(mesh.vertices)
            faces_index += len(mesh.loop_triangles)

    @staticmethod
    def write_texture_coordinates(file, header, mesh):
        for tri in mesh.loop_triangles:  # for face in mesh.faces:
            for loop_index in tri.loops:
                try:
                    uv = mesh.uv_layers[0].data[loop_index].uv
                except:
                    uv = [0, 0]

                # (u,v) in blender -> (u,1-v)
                pack = struct.pack('<2h',
                                   int(uv[0] * header.skin_width),
                                   int((1 - uv[1]) * header.skin_height),
                                   )
                file.write(pack)  # uv
            # (uv index is : face.index*3+i)

    def write_skins(self, file, filename, skins):
        # write skin file names
        for iSkin, skin in enumerate(skins):

            image_filename = bpy.path.abspath(skin)

            if self.options.fCopyTextureSxS:
                fn_sx_s = os.path.join(os.path.dirname(filename), os.path.basename(image_filename))

                if iSkin == 0 and self.options.fNameTextureToMD2Filename:
                    # rename first skin to basename
                    fn_sx_s = os.path.splitext(filename)[0] + os.path.splitext(image_filename)[1]

                print("Copying texture %s to %s" % (image_filename, fn_sx_s))
                try:
                    shutil.copy(image_filename, fn_sx_s)
                except:
                    print("Copying texture %s to %s failed." % (image_filename, fn_sx_s))

                image_filename = fn_sx_s  # for proper referencing in the MD2 file

            if len(image_filename) > 63 and not self.options.fExportOnlyTextureBasename:
                print(
                    "WARNING: The texture path '" + image_filename + "' is too long. It is automatically truncated to the file basename.")

            if len(image_filename) > 63 or self.options.fExportOnlyTextureBasename:
                image_filename = os.path.basename(image_filename)

            pack = struct.pack('<64s', bytes(image_filename[0:63], encoding='utf8'))
            file.write(pack)  # skin name

    def write_frame(self, file, frameName='frame'):
        meshes = []
        for obj in self.objects:
            mesh = obj.to_mesh(preserve_all_data_layers=True)
            mesh.transform(obj.matrix_world)
            mesh.transform(mathutils.Matrix.Rotation(-pi / 2, 4, 'Z'))
            meshes.append(mesh)
        # mesh.transform(mathutils.Matrix.Rotation(pi / 2, 4, 'X'))
        # mesh.transform(mathutils.Matrix.Rotation(pi, 4, 'Z'))

        bbox_min = self.bbox_min
        bbox_max = self.bbox_max

        if bbox_min is None:
            for mesh in meshes:
                (bbox_min, bbox_max) = Util.compute_bounding_box(mesh, bbox_min, bbox_max)

        [min_x, min_y, min_z] = bbox_min
        [max_x, max_y, max_z] = bbox_max

        # BL: some caching to speed it up:
        # -> sd_ gets the vertices between [0 and 255]
        #    which is our important quantization.
        sdx = (max_x - min_x) / 255.0
        sdy = (max_y - min_y) / 255.0
        sdz = (max_z - min_z) / 255.0
        isdx = 255.0 / (max_x - min_x)
        isdy = 255.0 / (max_y - min_y)
        isdz = 255.0 / (max_z - min_z)

        # note about the scale: self.object.scale is already applied via matrix_world
        pack = struct.pack('<6f16s',
                           # writing the scale of the model
                           self.scale * sdx,
                           self.scale * sdy,
                           self.scale * sdz,
                           # now the initial offset [= min of bounding box (correctly scaled)]
                           self.scale * min_x,
                           self.scale * min_y,
                           self.scale * min_z,
                           # and finally the name.
                           bytes(frameName, encoding='utf8'))

        file.write(pack)  # frame header

        # Vertices

        for mesh in meshes:
            for vert in mesh.vertices:
                best_normal_index = Util.find_closest_normal(vert.normal)
                # and now write the normal.
                pack = struct.pack('<4B',
                                   int((vert.co[0] - min_x) * isdx),
                                   int((vert.co[1] - min_y) * isdy),
                                   int((vert.co[2] - min_z) * isdz),
                                   best_normal_index)

                file.write(pack)  # write vertex and normal


class Util:
    @staticmethod
    def pick_name(base_name):
        name = '_MD2Obj_' + base_name + '_' + str(random.random())
        return name[0:20]

    # deletes an object from Blender (remove + unlink)
    @staticmethod
    def delete_object(obj):
        bpy.context.collection.objects.unlink(obj)
        bpy.data.objects.remove(obj)

    @staticmethod
    def backup_selection():
        # backup the current object selection and current active object
        selected_objects = bpy.context.selected_objects[:]
        active_object = bpy.context.active_object
        return active_object, selected_objects

    @staticmethod
    def restore_selection(active_object, selected_objects):
        bpy.context.view_layer.objects.active = active_object
        for obj in selected_objects:
            obj.select_set(state=True)

    # duplicates the given object and returns it
    @staticmethod
    def duplicate_object(obj, name):
        active_object, selected_objects = Util.backup_selection()

        # deselect all selected objects
        bpy.ops.object.select_all(action='DESELECT')
        # select the object which we want to duplicate
        obj.select_set(state=True)

        # duplicate the selected object
        bpy.ops.object.duplicate()

        # the duplicated object is automatically selected
        copy_obj = bpy.context.selected_objects[0]

        # rename the object with the given name
        copy_obj.name = name

        # select all objects which have been previously selected and make active the previous active object
        Util.restore_selection(active_object, selected_objects)

        return copy_obj

    @staticmethod
    def duplicate_and_apply_modifiers(obj, new_name):
        for o in bpy.context.scene.objects:
            if not o.hide_viewport:
                o.select_set(state=False)
        # select the object which we want to apply modifiers to
        obj.select_set(state=True)

        # duplicate the selected object
        bpy.ops.object.duplicate()

        # the duplicated object is automatically selected
        duplicate_object = bpy.context.selected_objects[0]

        # now apply all modifiers except the Armature modifier...
        for modifier in duplicate_object.modifiers:
            if modifier.type == "ARMATURE":
                # these must stay for the animation
                continue

            # all others can be applied.
            bpy.ops.object.modifier_apply(modifier=modifier.name)

        duplicate_object.name = new_name

        return duplicate_object

    # returns the mesh of the object and return object.data (mesh)
    @staticmethod
    def triangulate_mesh(obj):
        mesh = obj.data

        obj.select_set(state=True)
        # make the object the active object!
        bpy.context.view_layer.objects.active = obj

        bpy.ops.object.mode_set(mode="EDIT", toggle=False)
        bpy.ops.mesh.select_all(action="SELECT")

        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

        # FIXME
        mesh.calc_loop_triangles()

        print(mesh)
        return mesh

    @staticmethod
    def get_skins(objects):
        skins = []
        for obj in objects:
            for material in obj.data.materials:
                for texSlot in material.node_tree.nodes:
                    if not texSlot or texSlot.type != "TEX_IMAGE":
                        continue
                    if texSlot.image.filepath not in skins:
                        skins.append(texSlot.image.filepath)

        return skins

    @staticmethod
    def compute_bounding_box(mesh, bbox_min, bbox_max):
        bbox_min = bbox_min or [mesh.vertices[0].co[0], mesh.vertices[0].co[1], mesh.vertices[0].co[2]]
        bbox_max = bbox_max or [mesh.vertices[0].co[0], mesh.vertices[0].co[1], mesh.vertices[0].co[2]]

        for vert in mesh.vertices:
            for i in range(3):
                if vert.co[i] < bbox_min[i]:
                    bbox_min[i] = vert.co[i]
                if vert.co[i] > bbox_max[i]:
                    bbox_max[i] = vert.co[i]
        return bbox_min, bbox_max

    @staticmethod
    def find_closest_normal(normal):
        # find the closest normal for every vertex
        best_normal_index = 0
        max_dot = None
        for i in range(162):
            normal_candidate = MD2_NORMALS[i]
            # BL: what's the magic here??
            # Dot product
            dot = normal[1] * normal_candidate[0] + -normal[0] * normal_candidate[1] + normal[2] * normal_candidate[2]

            if i == 0 or dot > max_dot:
                max_dot = dot
                best_normal_index = i
        return best_normal_index

    @staticmethod
    def get_visible_mesh_objects():
        objects = []
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and not obj.hide_viewport:
                objects.append(obj)
        return objects


class ObjectInfo:
    def __init__(self, obj):
        self.vertices = -1
        self.status = ('', '')

        self.is_mesh = obj and obj.type == 'MESH'

        if self.is_mesh:
            self.skins = Util.get_skins([obj])

            tmp_object_name = Util.pick_name(obj.name)
            duplicated_object = None
            try:
                # apply the modifiers
                duplicated_object = Util.duplicate_and_apply_modifiers(obj, tmp_object_name)
                mesh = Util.triangulate_mesh(duplicated_object)

                self.status = (str(len(mesh.vertices)) + ' vertices', str(len(mesh.loop_triangles)) + ' faces')
                self.triangles_count = len(mesh.loop_triangles)
                self.vertices = len(mesh.vertices)

            finally:
                if duplicated_object is not None:
                    Util.delete_object(duplicated_object)

        print(self.status)


class OBJECT_OT_Export_MD2(bpy.types.Operator, ExportHelper):
    """Export to Quake2 file format (.md2)"""
    bl_idname = "export_quake.md2"
    bl_label = "Export to Quake2 file format (.md2)"

    filename: bpy.props.StringProperty(name="File Path",
                                       description="Filepath used for processing the script",
                                       maxlen=1024, default="")

    filename_ext = ".md2"

    rScaleFactor: bpy.props.FloatProperty(name="Scale for blenderUnits -> [mm]",
                                          description="Defaults to 10 (blender unit -> [mm])",
                                          default=10.0)

    fExportAnimation: bpy.props.BoolProperty(name="Export animation",
                                             description="default: False",
                                             default=False)

    useSameBoundingBox: bpy.props.BoolProperty(name="Use same bounding box for all animation frame",
                                               description="default: True",
                                               default=True)

    fExportOnlyTextureBasename: bpy.props.BoolProperty(name="Export only basenames (skin)",
                                                       description="default: True",
                                                       default=True)

    fCopyTextureSxS: bpy.props.BoolProperty(name="Copy texture(s) next to .md2",
                                            description="default: True",
                                            default=True)

    fNameTextureToMD2Filename: bpy.props.BoolProperty(name="Name first texture similar to .md2",
                                                      description="default: True",
                                                      default=True)

    # id_export   = 1
    # id_cancel   = 2
    # id_anim     = 3
    # id_update   = 4
    # id_help     = 5
    # id_basename = 6

    def __init__(self):
        self.objects = Util.get_visible_mesh_objects()

    def execute(self, context):
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)

        active_object, selected_objects = Util.backup_selection()
        # save the current frame to reset it after export
        frame = None
        if self.fExportAnimation:
            frame = bpy.context.scene.frame_current

        duplicate_objects = []
        try:
            for obj in self.objects:
                obj = Util.duplicate_and_apply_modifiers(obj, Util.pick_name(obj.name))
                Util.triangulate_mesh(obj)
                duplicate_objects.append(obj)

            md2 = MD2(self, duplicate_objects, self.rScaleFactor)
            md2.write(filepath)
        finally:
            Util.restore_selection(active_object, selected_objects)
            for obj in duplicate_objects:
                Util.delete_object(obj)
            if self.fExportAnimation:
                bpy.context.scene.frame_set(frame)

            self.report({'INFO'}, "Model exported")
        return {'FINISHED'}

    def invoke(self, context, event):
        active_object, selected_objects = Util.backup_selection()
        try:
            total_triangles_count = 0
            for obj in self.objects:
                info = ObjectInfo(obj)
                total_triangles_count += info.triangles_count

            if total_triangles_count * 3 > 2 ** 16:
                self.report({'ERROR'},
                            "Object has too many (triangulated) faces (%i), at most %i vertices are supported in md2" % (
                                total_triangles_count, (2 ** 16) / 3))
                return {'CANCELLED'}

            wm = context.window_manager
            wm.fileselect_add(self)
            return {'RUNNING_MODAL'}
        finally:
            Util.restore_selection(active_object, selected_objects)


def menu_cb(self, context):
    self.layout.operator(OBJECT_OT_Export_MD2.bl_idname, text="MD2 (.md2)")


classes = (
    OBJECT_OT_Export_MD2,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_cb)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.TOPBAR_MT_file_export.remove(menu_cb)


if __name__ == "__main__":
    register()
