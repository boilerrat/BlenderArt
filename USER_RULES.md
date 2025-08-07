# User Rules for Blender Python Art Assistant

## Project Context
You are working on a Blender Python Art Assistant project focused on creating automated art pipelines for generating stylized 2D and 3D artworks through repeatable, scriptable processes.

## Core Principles

### Blender Python Development
- **API Usage**: Use Blender's Python API (bpy) for all code generation
- **Version**: Assume Blender 4.x in scripting mode
- **Modularity**: Prioritize modular scripts with clearly defined functions
- **Documentation**: Include in-line comments explaining each key operation
- **Programmatic Approach**: Avoid UI interaction (no GUI clicks or panel navigation)
- **Scene Creation**: Favor programmatic scene creation: meshes, lights, cameras, materials, render settings

### Artistic Focus
- **Output Quality**: Optimize for artistic output, not performance
- **Visual Suggestions**: Suggest visual outcomes (e.g., "this script will generate a low-poly forest with stylized lighting")
- **Experimentation**: Offer suggestions for experiments (e.g., "try noise-based displacement on the z-axis for terrain variation")
- **Complete Scripts**: Output full working scripts unless snippets are specifically requested

### Technical Standards
- **Modern API**: Never use deprecated bpy.ops unless required. Prefer bpy.data and bpy.context
- **Math Utilities**: Use mathutils for vectors and matrices
- **Clean Code**: Respect clean code practices: reusable functions, meaningful variable names, no redundant code
- **Error Handling**: If errors occur, explain the fix and reprint the corrected version

## Project Focus Areas

Your projects may involve:
- Stylized landscapes
- Generative geometry
- Particle systems
- Animation loops
- NPR (non-photorealistic rendering) shaders
- Importing assets (e.g., PNGs as planes or textures)

## Code Delivery Standards

Whenever you provide code:
- Wrap it in a complete Python script
- Mention where and how to run it inside Blender
- Include proper error handling and cleanup
- Provide clear documentation of artistic parameters
- Suggest variations and experimentation options

## Blender-Specific Best Practices

- Use bpy.context.scene for scene management
- Leverage bpy.data for data access and manipulation
- Implement proper cleanup functions to avoid memory leaks
- Use mathutils.Vector and mathutils.Matrix for transformations
- Structure scripts with clear setup, execution, and cleanup phases
- Include artistic parameters as easily modifiable variables at the top of scripts

## File Organization
- Create organized script collections for different art styles
- Use descriptive filenames that indicate the artistic output
- Group related scripts in directories by theme (landscapes, characters, abstract, etc.)
- Maintain a library of reusable utility functions

## Artistic Parameters
- Make artistic parameters easily adjustable at the top of scripts
- Include comments explaining what each parameter affects
- Provide reasonable default values that produce good results
- Suggest ranges for experimentation

## Error Prevention
- Always check if objects exist before manipulating them
- Use try-except blocks for operations that might fail
- Provide clear error messages for common issues
- Include cleanup code to reset the scene state

## Performance Considerations
- Optimize for artistic quality over rendering speed
- Use efficient data structures for large scenes
- Consider memory usage when generating complex geometry
- Provide options for different quality levels
