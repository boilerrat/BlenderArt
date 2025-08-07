"""
Fuzzy Sphere with Hard Lighting and Deep Shadows
===============================================

This script creates a 3D sphere with a fuzzy, velvety texture using procedural materials,
hard directional lighting, and deep shadows for dramatic effect.

To run this script in Blender:
1. Open Blender 4.x
2. Go to Scripting workspace
3. Open this file in the text editor
4. Click "Run Script" or press Alt+P

Artistic Parameters (modify these at the top):
- SPHERE_RADIUS: Size of the sphere
- FUZZ_DENSITY: How dense the fuzzy texture appears
- FUZZ_LENGTH: Length of the fuzzy fibers
- LIGHT_INTENSITY: Brightness of the main light
- SHADOW_SOFTNESS: How soft or hard the shadows are
- CAMERA_DISTANCE: How far the camera is from the sphere
"""

import bpy
import bmesh
from mathutils import Vector, Matrix
import random

# ============================================================================
# ARTISTIC PARAMETERS - Modify these for different effects
# ============================================================================

SPHERE_RADIUS = 2.0
FUZZ_DENSITY = 2.0  # Maximum fuzziness
FUZZ_LENGTH = 0.5   # Longer fuzzy fibers for more dramatic effect
LIGHT_INTENSITY = 15.0  # Much brighter to make sphere visible
SHADOW_SOFTNESS = 0.07  # Even harder shadows for more drama
CAMERA_DISTANCE = 12.0  # Much further for full sphere visibility
RENDER_SAMPLES = 750  # Higher quality render
CAMERA_ANGLE = "side"  # Options: "dramatic", "low_angle", "high_angle", "side", "cinematic", "hero"
LIGHTING_STYLE = "studio"  # Options: "cinematic", "studio", "dramatic"

# ============================================================================
# SCENE SETUP
# ============================================================================

def clear_scene():
    """Clear all objects from the scene"""
    # Remove all objects from the scene
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # Clear textures
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)
    
    # Clear meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    
    # Clear cameras
    for camera in bpy.data.cameras:
        bpy.data.cameras.remove(camera)
    
    # Clear lights
    for light in bpy.data.lights:
        bpy.data.lights.remove(light)

def setup_scene():
    """Set up the basic scene with camera and render settings"""
    scene = bpy.context.scene
    
    # Set render engine to Cycles for better material and lighting
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = RENDER_SAMPLES
    scene.cycles.use_denoising = True
    
    # Create target empty for camera tracking
    target_empty = bpy.data.objects.new("CameraTarget", None)
    target_empty.empty_display_type = 'PLAIN_AXES'
    target_empty.location = (0, 0, 0)  # Center of sphere
    bpy.context.scene.collection.objects.link(target_empty)
    
    # Set up camera
    camera = bpy.data.cameras.new("Camera")
    camera_obj = bpy.data.objects.new("Camera", camera)
    bpy.context.scene.collection.objects.link(camera_obj)
    
    # Position camera based on angle preference
    if CAMERA_ANGLE == "dramatic":
        # Low angle, dramatic view
        camera_obj.location = (4, -CAMERA_DISTANCE * 0.8, 1)
    elif CAMERA_ANGLE == "low_angle":
        # Extreme low angle
        camera_obj.location = (0, -CAMERA_DISTANCE * 0.7, 0.5)
    elif CAMERA_ANGLE == "high_angle":
        # Looking down
        camera_obj.location = (0, -CAMERA_DISTANCE * 0.7, 6)
    elif CAMERA_ANGLE == "side":
        # Side view
        camera_obj.location = (CAMERA_DISTANCE * 0.8, 0, 2)
    elif CAMERA_ANGLE == "cinematic":
        # Extreme cinematic angle - very low and tilted
        camera_obj.location = (6, -CAMERA_DISTANCE * 0.6, 0.5)
    elif CAMERA_ANGLE == "hero":
        # Hero shot - dramatic low angle with tilt
        camera_obj.location = (8, -CAMERA_DISTANCE * 0.5, 1)
    else:
        # Default dramatic angle
        camera_obj.location = (4, -CAMERA_DISTANCE * 0.8, 1)
    
    # Set up camera tracking to target empty
    track_constraint = camera_obj.constraints.new(type='TRACK_TO')
    track_constraint.target = target_empty
    track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_constraint.up_axis = 'UP_Y'
    
    # Set as active camera
    scene.camera = camera_obj
    
    # Set camera settings for dramatic effect
    camera.lens = 35  # Wider lens to capture more of the scene
    camera.dof.use_dof = True
    camera.dof.aperture_fstop = 4.0  # More depth of field to keep sphere in focus
    camera.dof.focus_distance = CAMERA_DISTANCE
    
    return target_empty

# ============================================================================
# SCENE OBJECTS CREATION
# ============================================================================

def create_fuzzy_sphere():
    """Create a sphere with fuzzy texture"""
    
    # Create the base sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=SPHERE_RADIUS,
        location=(0, 0, 0),
        segments=64,
        ring_count=32
    )
    sphere = bpy.context.active_object
    sphere.name = "FuzzySphere"
    
    # Add subdivision surface for smoother base
    subsurf = sphere.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3
    
    # Add displacement for fuzzy texture
    displace = sphere.modifiers.new(name="Displacement", type='DISPLACE')
    
    # Create noise texture for displacement
    noise_tex = bpy.data.textures.new("FuzzyNoise", type='CLOUDS')
    noise_tex.noise_scale = 0.3  # Smaller scale for more detailed fuzz
    noise_tex.noise_depth = 8     # More depth for more complex texture
    
    displace.texture = noise_tex
    displace.strength = FUZZ_LENGTH * FUZZ_DENSITY
    
    return sphere

def create_ground_plane():
    """Create a ground plane to show shadows"""
    
    # Create a much larger ground plane to avoid seeing corners
    bpy.ops.mesh.primitive_plane_add(
        size=50,
        location=(0, 0, -SPHERE_RADIUS - 0.1)  # Just below the sphere
    )
    ground = bpy.context.active_object
    ground.name = "Ground"
    
    # Create simple ground material
    ground_material = bpy.data.materials.new(name="GroundMaterial")
    ground_material.use_nodes = True
    nodes = ground_material.node_tree.nodes
    links = ground_material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Position nodes
    output.location = (300, 0)
    principled.location = (0, 0)
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Set up ground material properties
    principled.inputs['Base Color'].default_value = (0.08, 0.08, 0.12, 1.0)  # Dark blue-gray
    principled.inputs['Roughness'].default_value = 0.8
    principled.inputs['Specular IOR Level'].default_value = 0.05
    principled.inputs['Metallic'].default_value = 0.0
    
    # Assign material to ground
    ground.data.materials.append(ground_material)
    
    return ground

def setup_studio_background():
    """Set up a proper studio background using world environment"""
    
    # Get the world
    world = bpy.context.scene.world
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_links = world.node_tree.links
    
    # Clear existing world nodes
    world_nodes.clear()
    
    # Create gradient studio background
    background = world_nodes.new(type='ShaderNodeBackground')
    output = world_nodes.new(type='ShaderNodeOutputWorld')
    color_ramp = world_nodes.new(type='ShaderNodeValToRGB')
    tex_coord = world_nodes.new(type='ShaderNodeTexCoord')
    
    # Position nodes
    background.location = (300, 0)
    output.location = (500, 0)
    color_ramp.location = (-200, 0)
    tex_coord.location = (-400, 0)
    
    # Connect nodes for gradient background
    world_links.new(tex_coord.outputs['Generated'], color_ramp.inputs['Fac'])
    world_links.new(color_ramp.outputs['Color'], background.inputs['Color'])
    world_links.new(background.outputs['Background'], output.inputs['Surface'])
    
    # Set up gradient for dramatic studio look
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.05, 0.02, 0.08, 1.0)  # Deep purple at bottom
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (0.15, 0.25, 0.35, 1.0)  # Blue-gray at top
    
    # Set background strength
    background.inputs['Strength'].default_value = 1.0
    
    return world

# ============================================================================
# FUZZY MATERIAL CREATION
# ============================================================================

def create_fuzzy_material():
    """Create a fuzzy, velvety material"""
    
    # Create new material
    material = bpy.data.materials.new(name="FuzzyMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Position nodes
    output.location = (300, 0)
    principled.location = (0, 0)
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Set up fuzzy material properties
    principled.inputs['Base Color'].default_value = (0.9, 0.3, 0.2, 1.0)  # Vibrant coral/red
    principled.inputs['Roughness'].default_value = 0.95  # Maximum roughness for ultra-fuzzy look
    principled.inputs['Specular IOR Level'].default_value = 0.05   # Very low specular
    principled.inputs['Metallic'].default_value = 0.0   # Non-metallic
    
    # Add subsurface scattering for soft, fuzzy appearance
    principled.inputs['Subsurface Weight'].default_value = 0.4
    principled.inputs['Subsurface Radius'].default_value = (1.0, 0.4, 0.3)
    
    # Add bump mapping for additional texture
    bump = nodes.new(type='ShaderNodeBump')
    noise_tex = nodes.new(type='ShaderNodeTexNoise')
    
    bump.location = (-200, -200)
    noise_tex.location = (-400, -200)
    
    # Connect bump mapping
    links.new(noise_tex.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    
    # Set noise texture properties for more fuzzy appearance
    noise_tex.inputs['Scale'].default_value = 80.0  # More detailed texture
    noise_tex.inputs['Detail'].default_value = 12.0  # More detail levels
    noise_tex.inputs['Roughness'].default_value = 0.9  # More variation
    
    return material

# ============================================================================
# LIGHTING SETUP
# ============================================================================

def setup_hard_lighting():
    """Set up hard lighting with deep shadows"""
    
    if LIGHTING_STYLE == "cinematic":
        # Cinematic lighting with multiple lights
        # Main key light
        key_light_data = bpy.data.lights.new(name="KeyLight", type='SUN')
        key_light_data.energy = LIGHT_INTENSITY
        key_light_data.angle = SHADOW_SOFTNESS
        key_light_data.use_shadow = True
        key_light_data.shadow_soft_size = SHADOW_SOFTNESS
        
        key_light_obj = bpy.data.objects.new(name="KeyLight", object_data=key_light_data)
        bpy.context.scene.collection.objects.link(key_light_obj)
        
        # Position key light for dramatic effect - much closer and brighter
        key_light_obj.location = (4, -2, 6)
        key_light_obj.rotation_euler = (0.8, 0.2, -0.1)
        
        # Rim light for edge definition
        rim_light_data = bpy.data.lights.new(name="RimLight", type='SPOT')
        rim_light_data.energy = LIGHT_INTENSITY * 1.2
        rim_light_data.spot_size = 1.0
        rim_light_data.spot_blend = 0.5
        rim_light_data.use_shadow = True
        
        rim_light_obj = bpy.data.objects.new(name="RimLight", object_data=rim_light_data)
        bpy.context.scene.collection.objects.link(rim_light_obj)
        
        # Position rim light behind sphere - closer
        rim_light_obj.location = (-3, 1, 4)
        rim_light_obj.rotation_euler = (0.6, -0.1, 2.5)
        
        # Brighter fill light - positioned to light the background too
        fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
        fill_data.energy = LIGHT_INTENSITY * 0.6
        fill_data.size = 15.0
        
        fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
        bpy.context.scene.collection.objects.link(fill_obj)
        
        fill_obj.location = (0, 2, 8)
        fill_obj.rotation_euler = (-0.5, 0, 0)
        
    elif LIGHTING_STYLE == "studio":
        # Clean studio lighting
        main_light_data = bpy.data.lights.new(name="MainLight", type='SUN')
        main_light_data.energy = LIGHT_INTENSITY
        main_light_data.angle = SHADOW_SOFTNESS
        main_light_data.use_shadow = True
        main_light_data.shadow_soft_size = SHADOW_SOFTNESS
        
        main_light_obj = bpy.data.objects.new(name="MainLight", object_data=main_light_data)
        bpy.context.scene.collection.objects.link(main_light_obj)
        
        main_light_obj.location = (5, -3, 8)
        main_light_obj.rotation_euler = (0.8, 0.3, -0.5)
        
        # Soft fill light
        fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
        fill_data.energy = LIGHT_INTENSITY * 0.4
        fill_data.size = 10.0
        
        fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
        bpy.context.scene.collection.objects.link(fill_obj)
        
        fill_obj.location = (-4, 2, 5)
        fill_obj.rotation_euler = (-0.4, -0.2, 0.8)
        
    else:  # dramatic
        # Single dramatic light
        light_data = bpy.data.lights.new(name="DramaticLight", type='SUN')
        light_data.energy = LIGHT_INTENSITY * 1.5
        light_data.angle = SHADOW_SOFTNESS
        light_data.use_shadow = True
        light_data.shadow_soft_size = SHADOW_SOFTNESS
        
        light_obj = bpy.data.objects.new(name="DramaticLight", object_data=light_data)
        bpy.context.scene.collection.objects.link(light_obj)
        
        light_obj.location = (10, -5, 12)
        light_obj.rotation_euler = (0.5, 0.5, -0.2)
    
    # Note: World background is now handled by setup_studio_background()
    # This ensures proper studio lighting without physical background objects

# ============================================================================
# RENDER SETTINGS
# ============================================================================

def setup_render_settings():
    """Configure render settings for dramatic effect"""
    
    scene = bpy.context.scene
    render = scene.render
    
    # Set render resolution
    render.resolution_x = 1920
    render.resolution_y = 1080
    render.resolution_percentage = 100
    
    # Enable depth of field for artistic focus
    camera = scene.camera.data
    camera.dof.use_dof = True
    camera.dof.aperture_fstop = 2.8
    camera.dof.focus_distance = CAMERA_DISTANCE
    
    # Set color management for dramatic look
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'High Contrast'

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("Creating Fuzzy Sphere with Hard Lighting...")
    
    # Clear existing scene
    clear_scene()
    
    # Set up scene with camera tracking
    target_empty = setup_scene()
    
    # Create fuzzy sphere
    sphere = create_fuzzy_sphere()
    
    # Create and assign fuzzy material
    fuzzy_material = create_fuzzy_material()
    sphere.data.materials.append(fuzzy_material)
    
    # Create ground plane for shadows
    ground = create_ground_plane()
    
    # Set up studio background using world environment
    setup_studio_background()
    
    # Set up lighting
    setup_hard_lighting()
    
    # Configure render settings
    setup_render_settings()
    
    # Select the sphere for easy manipulation
    bpy.context.view_layer.objects.active = sphere
    sphere.select_set(True)
    
    print("Fuzzy sphere created successfully!")
    print("Artistic suggestions:")
    print("- Try adjusting FUZZ_DENSITY for different fuzzy levels")
    print("- Modify LIGHT_INTENSITY for more/less dramatic lighting")
    print("- Change SPHERE_RADIUS for different sphere sizes")
    print("- Experiment with different Base Color values in the material")
    print("- Try different CAMERA_ANGLE options: 'dramatic', 'low_angle', 'high_angle', 'side', 'cinematic', 'hero'")
    print("- Experiment with LIGHTING_STYLE: 'cinematic', 'studio', 'dramatic'")
    print("- Adjust CAMERA_DISTANCE for closer/farther views")

# Run the script
if __name__ == "__main__":
    main()
