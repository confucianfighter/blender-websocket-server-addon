import bpy
import bmesh
import json

y = 0
def create_json_from_mesh(obj):
    mesh_data = {
        "name": obj.name,
        "vertices": [],
        "triangles": [],
        "normals": [],
        "position": list(obj.location),
        "rotation_euler": list(obj.rotation_euler),
        "scale": list(obj.scale),
    }

    # Add vertices data
    for vertex in obj.data.vertices:
        vertex_data = [vertex.co.x, vertex.co.y, vertex.co.z]
        mesh_data["vertices"].append(vertex_data)
        normal_data = [vertex.normal.x, vertex.normal.y, vertex.normal.z]
        mesh_data["normals"].append(normal_data)

    # Add triangles data
    for poly in obj.data.polygons:
        verts_in_face = [v for v in poly.vertices]
        mesh_data["triangles"].append(verts_in_face)

    return mesh_data

def add_cube():
    global y
    x, z = 0, 0

    # Create a cube
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    obj = bpy.context.active_object
    # add a split modifier
    # Add Edge Split modifier
    bpy.ops.object.modifier_add(type='EDGE_SPLIT')

    # Access and configure the modifier (optional)
    edge_split_modifier = obj.modifiers['EdgeSplit']
    edge_split_modifier.split_angle = 1.0472  # 60 degrees in radians

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier='EdgeSplit')
    y += 1

    # Get a BMesh representation
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Triangulate
    bmesh.ops.triangulate(bm, faces=bm.faces[:])

    # Update the mesh with new data
    bm.to_mesh(mesh)
    bm.free() 

    print("Converted to triangles.")

    # Printing vertices
    # print("\nVertices:")
    # for vertex in obj.data.vertices:
    #     print(f"Vertex {vertex.index}: {vertex.co}")

    # # Printing triangles
    # print("\nTriangles:")
    # for poly in obj.data.polygons:
    #     verts_in_face = [v for v in poly.vertices]
    #     print(f"Triangle {poly.index}: Vertices {verts_in_face}")
    # else:
    #     print("No active mesh object selected.")
    #     # Save the current Blender file
    return create_json_from_mesh(obj)
    #bpy.ops.wm.save_mainfile()

# Example usage
def duplicate_faces(obj):
    
    # Use bmesh to access and modify the mesh data
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    new_verts = []
    faces = []
    for face in bm.faces:
        # Duplicate vertices for each face
        face_verts = [bm.verts.new(v.co) for v in face.verts]
        new_verts.extend(face_verts)

        # Create a new face with the duplicated vertices
        faces.append(face_verts)

    for face in faces:
        bm.faces.new(face)
    
    # Remove original geometry
    bmesh.ops.delete(bm, geom=bm.faces, context='FACES_ONLY')
    bmesh.ops.delete(bm, geom=bm.verts, context='VERTS')

    # Update the mesh with new data
    bm.to_mesh(obj.data)
    bm.free()