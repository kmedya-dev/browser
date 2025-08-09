from pythonforandroid.recipes.pyjnius import PyjniusRecipe
from pythonforandroid.toolchain import Recipe

class PyjniusFixRecipe(PyjniusRecipe):
    """
    This is a custom recipe to apply a patch to pyjnius.
    """
    # We use the same version as the original recipe we want to patch
    version = '1.6.1'

    # This is the name of our custom recipe
    name = 'pyjnius_fix'

    # This is the list of patches to apply to the source code
    # p4a will automatically apply these patches.
    patches = ['pyjnius_long_fix.patch']

    # We need to tell p4a that this recipe conflicts with the original pyjnius recipe
    conflicts = ['pyjnius']

# This is the entry point for p4a to find our recipe
recipe = PyjniusFixRecipe()
