from pythonforandroid.recipes.pyjnius import PyjniusRecipe

class PatchedPyjniusRecipe(PyjniusRecipe):
    """
    This is a custom recipe to apply a patch to pyjnius.
    """
    # We use the same version as the original recipe we want to patch
    version = '1.6.1'

    # This is the name of our custom recipe, which is the same as the original one
    name = 'pyjnius'

    # This is the list of patches to apply to the source code
    # p4a will automatically apply these patches.
    patches = ['pyjnius_long_fix.patch']
    

# This is the entry point for p4a to find our recipe
recipe = PatchedPyjniusRecipe()