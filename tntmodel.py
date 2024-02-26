import bpy
from struct import unpack, iter_unpack

def geometry_import(operator, context, file):
    """
    Import only geometry blocks. Materials not supported at this moment.
    """
    with open(file, "rb") as bs:
        
        name = file.split("\\")[-1].split(".")[0]
        tnt_buffer = bs.read()
        geom_blocks = list()
        
        # igly thing
        past_offset = 0
        while True:
            offset = tnt_buffer.find(b"\x12\x01\x00\x00", past_offset)
            if offset == -1: break

            geom_blocks.append(offset)
            past_offset = offset + 4
            
        
        for submesh_id, geominfo_offset in enumerate(geom_blocks):
            bs.seek(geominfo_offset)
            
            _, num_vertices, num_faces, buffer_size = unpack("<4I", bs.read(16))
            assert(buffer_size == 32)
            
            bs.seek(488, 1)
            vertices = iter_unpack("<3f3f2f", bs.read(num_vertices * buffer_size))
            
            positions = list()
            normals = list()
            uv = list()
            for vertex in vertices:
                positions.append([vertex[0], vertex[2], vertex[1]])
                normals.append([vertex[3], vertex[5], vertex[4]])
                uv.append([vertex[6], 1-vertex[7]])
                
            faces = list((a, c, b) for (a, b, c) in iter_unpack("<3H", bs.read(num_faces * 2)))
            faces_flat = list()
            for face in faces:
                faces_flat.extend(face)
            
            me = bpy.data.meshes.new(f"{name}_{submesh_id}")
            me.from_pydata(positions, [], faces)
            
            me.uv_layers.new()
            for face_id, loop in enumerate(me.uv_layers[0].data):
                loop.uv = uv[faces_flat[face_id]]
            
            me.update()
            
            obj = bpy.data.objects.new(f"{name}_{submesh_id}", me)
            context.collection.objects.link(obj)
            
        return {'FINISHED'}