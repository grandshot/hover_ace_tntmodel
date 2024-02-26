from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

import bpy

bl_info = {
    "name": "Hover Ace Demo TNTMODEL format",
    "author": "StreamThread",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "File > Import",
    "description": "A simple geometry importer of Hover Ace Demo TNTMODEL's.",
    "category": "Import-Export"
}

if "bpy" in locals():
    import importlib
    if "tntmodel" in locals():
        importlib.reload(tntmodel)

class ImportTNTMODEL(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.tntmodel"
    bl_label = 'Import TNTMODEL'
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".TNTMODEL"
    filter_glob: StringProperty(default="*.TNTMODEL", options={'HIDDEN'})
    
    
    def execute(self, context):
        from . import tntmodel
        return tntmodel.geometry_import(self, context, self.filepath)


def menu_func_import(self, context):
    self.layout.operator(ImportTNTMODEL.bl_idname, text="Hover Ace Demo (.TNTMODEL)")
       
        
def register():
    bpy.utils.register_class(ImportTNTMODEL)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    
def unregister():
    bpy.utils.unregister_class(ImportTNTMODEL)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)