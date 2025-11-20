import os

patches_dir = os.path.dirname(__file__)
patch_config_path = os.path.join(patches_dir, 'patches.cfg')

with open(patch_config_path, 'w') as f:
    f.write('kivy = ["patches/kivy_setup_py.patch"]\n')
