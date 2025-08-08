"""
Studio Geometric Shapes - Blender Python Art Script
Creates a professional studio scene with three geometric shapes:
- Cube with metallic texture
- Tetrahedron with crystalline texture
- Sphere with organic texture

Each shape has unique materials, colors, and dramatic studio lighting.
Now includes multiple dramatic cameras (Main, Wide, Close, Top) aimed at the scene.
"""

import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix

# ============================================================================
# ARTISTIC PARAMETERS - Adjust these for different visual outcomes
# ============================================================================

# Scene setup
SCENE_NAME = "Studio_Geometric_Shapes"
RENDER_ENGINE = 'CYCLES'  # 'CYCLES' or 'EEVEE'
RENDER_SAMPLES = 1000  # Higher for better quality

# Shape parameters
SHAPE_SCALE = 1.5
SHAPE_SPACING = 4.0
FLOOR_HEIGHT = -2.0

# Material parameters
CUBE_COLOR = (0.8, 0.2, 0.3, 1.0)  # Deep red
TETRAHEDRON_COLOR = (0.2, 0.6, 0.8, 1.0)  # Electric blue
SPHERE_COLOR = (0.3, 0.8, 0.4, 1.0)  # Emerald green

# Lighting parameters
KEY_LIGHT_INTENSITY = 1500
FILL_LIGHT_INTENSITY = 800
RIM_LIGHT_INTENSITY = 1200
BACK_LIGHT_INTENSITY = 600

# Camera parameters
CAMERA_DISTANCE = 12
CAMERA_HEIGHT = 3
CAMERA_ANGLE = 15  # degrees

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_tetrahedron():
    """Create a tetrahedron mesh"""
    # Create a new mesh and bmesh
    mesh = bpy.data.meshes.new("Tetrahedron")
    bm = bmesh.new()
    
    # Add vertices for a tetrahedron
    vertices = [
        Vector((1, 1, 1)),
        Vector((-1, -1, 1)),
        Vector((-1, 1, -1)),
        Vector((1, -1, -1))
    ]
    
    # Add vertices to bmesh
    bmesh_verts = [bm.verts.new(v) for v in vertices]
    
    # Create faces (triangles)
    faces = [
        [bmesh_verts[0], bmesh_verts[1], bmesh_verts[2]],
        [bmesh_verts[0], bmesh_verts[2], bmesh_verts[3]],
        [bmesh_verts[0], bmesh_verts[3], bmesh_verts[1]],
        [bmesh_verts[1], bmesh_verts[3], bmesh_verts[2]]
    ]
    
    for face_verts in faces:
        bm.faces.new(face_verts)
    
    # Update bmesh and create object
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new("Tetrahedron", mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def create_metallic_material(name, base_color, metallic=1.0, roughness=0.1):
    """Create a metallic material with PBR properties"""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create principled BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = base_color
    principled.inputs['Metallic'].default_value = metallic
    principled.inputs['Roughness'].default_value = roughness
    
    # Create material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    material_output.location = (300, 0)
    
    # Link nodes
    links.new(principled.outputs['BSDF'], material_output.inputs['Surface'])
    
    return material

def create_crystalline_material(name, base_color):
    """Create a crystalline/glass-like material"""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create principled BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = base_color
    principled.inputs['Transmission'].default_value = 0.8
    principled.inputs['IOR'].default_value = 1.45
    principled.inputs['Roughness'].default_value = 0.0
    principled.inputs['Alpha'].default_value = 0.9
    
    # Enable alpha blending
    material.blend_method = 'BLEND'
    
    # Create material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    material_output.location = (300, 0)
    
    # Link nodes
    links.new(principled.outputs['BSDF'], material_output.inputs['Surface'])
    
    return material

def create_organic_material(name, base_color):
    """Create an organic/subsurface material"""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create principled BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = base_color
    principled.inputs['Subsurface'].default_value = 0.1
    principled.inputs['Subsurface Color'].default_value = (0.8, 0.9, 0.7, 1.0)
    principled.inputs['Roughness'].default_value = 0.3
    
    # Create material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    material_output.location = (300, 0)
    
    # Link nodes
    links.new(principled.outputs['BSDF'], material_output.inputs['Surface'])
    
    return material

def setup_studio_lighting():
    """Create dramatic studio lighting setup"""
    # Key light (main light)
    key_light = bpy.data.lights.new(name="Key_Light", type='AREA')
    key_light.energy = KEY_LIGHT_INTENSITY
    key_light.size = 2.0
    key_light.color = (1.0, 0.95, 0.9)  # Warm white
    
    key_light_obj = bpy.data.objects.new(name="Key_Light", object_data=key_light)
    bpy.context.collection.objects.link(key_light_obj)
    key_light_obj.location = (8, -4, 6)
    key_light_obj.rotation_euler = (math.radians(45), math.radians(-30), 0)
    
    # Fill light (softer, fills shadows)
    fill_light = bpy.data.lights.new(name="Fill_Light", type='AREA')
    fill_light.energy = FILL_LIGHT_INTENSITY
    fill_light.size = 3.0
    fill_light.color = (0.9, 0.95, 1.0)  # Cool white
    
    fill_light_obj = bpy.data.objects.new(name="Fill_Light", object_data=fill_light)
    bpy.context.collection.objects.link(fill_light_obj)
    fill_light_obj.location = (-6, -2, 4)
    fill_light_obj.rotation_euler = (math.radians(30), math.radians(45), 0)
    
    # Rim light (backlight for separation)
    rim_light = bpy.data.lights.new(name="Rim_Light", type='SPOT')
    rim_light.energy = RIM_LIGHT_INTENSITY
    rim_light.spot_size = math.radians(30)
    rim_light.color = (1.0, 1.0, 0.9)  # Slightly warm
    
    rim_light_obj = bpy.data.objects.new(name="Rim_Light", object_data=rim_light)
    bpy.context.collection.objects.link(rim_light_obj)
    rim_light_obj.location = (0, 8, 5)
    rim_light_obj.rotation_euler = (math.radians(-60), 0, 0)
    
    # Back light (for dramatic shadows)
    back_light = bpy.data.lights.new(name="Back_Light", type='AREA')
    back_light.energy = BACK_LIGHT_INTENSITY
    back_light.size = 4.0
    back_light.color = (0.8, 0.8, 1.0)  # Cool blue
    
    back_light_obj = bpy.data.objects.new(name="Back_Light", object_data=back_light)
    bpy.context.collection.objects.link(back_light_obj)
    back_light_obj.location = (0, -8, 3)
    back_light_obj.rotation_euler = (math.radians(15), 0, 0)

def _ensure_camera_target():
    """Create or reuse a camera target Empty at the origin."""
    name = "Studio_Camera_Target"
    target = bpy.data.objects.get(name)
    if target is None:
        target = bpy.data.objects.new(name, None)
        target.empty_display_type = 'PLAIN_AXES'
        target.location = (0.0, 0.0, 0.0)
        bpy.context.collection.objects.link(target)
    return target


def _add_camera(name, location, lens=50, fstop=2.8):
    """Create a camera, position it, add a Track To constraint, and tune DOF."""
    cam_data = bpy.data.cameras.new(name=name)
    cam_obj = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam_obj)

    # Place camera and aim at the target
    cam_obj.location = location
    target = _ensure_camera_target()
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    # Camera settings
    cam_data.lens = lens
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = fstop
    # Focus roughly on the origin based on distance
    cam_data.dof.focus_distance = (Vector(location) - Vector((0.0, 0.0, 0.0))).length

    return cam_obj


def setup_cameras():
    """Add multiple dramatic cameras and set the main as active."""
    main_loc = (CAMERA_DISTANCE, -CAMERA_DISTANCE, CAMERA_HEIGHT)
    wide_loc = (CAMERA_DISTANCE * 1.6, -CAMERA_DISTANCE * 1.2, CAMERA_HEIGHT * 0.4)
    close_loc = (CAMERA_DISTANCE * 0.75, -CAMERA_DISTANCE * 0.5, CAMERA_HEIGHT * 0.9)
    top_loc = (0.0, -CAMERA_DISTANCE * 1.2, CAMERA_DISTANCE * 1.2)

    cam_main = _add_camera("Studio_Camera_Main", main_loc, lens=50, fstop=2.8)
    _add_camera("Studio_Camera_Wide", wide_loc, lens=28, fstop=4.0)
    _add_camera("Studio_Camera_Close", close_loc, lens=85, fstop=1.8)
    _add_camera("Studio_Camera_Top", top_loc, lens=50, fstop=4.0)

    bpy.context.scene.camera = cam_main

def create_floor():
    """Create a reflective floor"""
    # Create floor plane
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, FLOOR_HEIGHT))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    
    # Create floor material
    floor_material = bpy.data.materials.new(name="Floor_Material")
    floor_material.use_nodes = True
    nodes = floor_material.node_tree.nodes
    links = floor_material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create principled BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Dark gray
    principled.inputs['Roughness'].default_value = 0.2
    principled.inputs['Metallic'].default_value = 0.0
    
    # Create material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    material_output.location = (300, 0)
    
    # Link nodes
    links.new(principled.outputs['BSDF'], material_output.inputs['Surface'])
    
    # Assign material to floor
    floor.data.materials.append(floor_material)

def setup_render_settings():
    """Configure render settings for studio quality"""
    scene = bpy.context.scene
    
    # Set render engine
    scene.render.engine = RENDER_ENGINE
    
    if RENDER_ENGINE == 'CYCLES':
        scene.cycles.samples = RENDER_SAMPLES
        # Enable denoising if supported
        if hasattr(scene.cycles, 'use_denoising'):
            scene.cycles.use_denoising = True
        
        # Pick a denoiser that exists on this build (prefer OIDN, else OPTIX)
        try:
            denoiser_prop = bpy.types.CyclesRenderSettings.bl_rna.properties.get('denoiser')
            if denoiser_prop:
                available = [item.identifier for item in denoiser_prop.enum_items]
                preferred = 'OPENIMAGEDENOISE' if 'OPENIMAGEDENOISE' in available else (
                    'OPTIX' if 'OPTIX' in available else None
                )
                if preferred is None and len(available) > 0:
                    preferred = available[0]
                if preferred:
                    scene.cycles.denoiser = preferred
        except Exception:
            # Silently continue if denoiser property isn't available on this Blender build
            pass
    else:  # EEVEE
        scene.eevee.taa_render_samples = RENDER_SAMPLES
        scene.eevee.use_soft_shadows = True
    
    # Set render resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    # Enable motion blur and depth of field
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5

# ============================================================================
# MAIN SCRIPT EXECUTION
# ============================================================================

def create_studio_geometric_shapes():
    """Main function to create the studio geometric shapes scene"""
    
    # Clear existing scene
    clear_scene()
    
    # Setup render settings
    setup_render_settings()
    
    # Create floor
    create_floor()
    
    # Create cube
    bpy.ops.mesh.primitive_cube_add(size=2, location=(-SHAPE_SPACING, 0, 0))
    cube = bpy.context.active_object
    cube.name = "Studio_Cube"
    cube.scale = (SHAPE_SCALE, SHAPE_SCALE, SHAPE_SCALE)
    
    # Create tetrahedron
    tetrahedron = create_tetrahedron()
    tetrahedron.location = (0, 0, 0)
    tetrahedron.scale = (SHAPE_SCALE, SHAPE_SCALE, SHAPE_SCALE)
    
    # Create sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(SHAPE_SPACING, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = "Studio_Sphere"
    sphere.scale = (SHAPE_SCALE, SHAPE_SCALE, SHAPE_SCALE)
    
    # Create materials
    cube_material = create_metallic_material("Cube_Material", CUBE_COLOR)
    tetrahedron_material = create_crystalline_material("Tetrahedron_Material", TETRAHEDRON_COLOR)
    sphere_material = create_organic_material("Sphere_Material", SPHERE_COLOR)
    
    # Assign materials
    cube.data.materials.append(cube_material)
    tetrahedron.data.materials.append(tetrahedron_material)
    sphere.data.materials.append(sphere_material)
    
    # Setup lighting
    setup_studio_lighting()
    
    # Setup multiple dramatic cameras
    setup_cameras()
    
    # Enable shadows for all lights
    for light in bpy.data.lights:
        light.use_shadow = True
        if light.type == 'AREA':
            light.shadow_soft_size = 0.5
    
    print("Studio geometric shapes scene created successfully!")
    print("Scene includes:")
    print("- Metallic red cube")
    print("- Crystalline blue tetrahedron") 
    print("- Organic green sphere")
    print("- Dramatic studio lighting with shadows")
    print("- Professional camera setup")

# ============================================================================
# SCRIPT EXECUTION
# ============================================================================

if __name__ == "__main__":
    create_studio_geometric_shapes()
