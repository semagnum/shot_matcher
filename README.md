# Color Matching Analyzer

The purpose of this addon is to speed up the compositing workflow with color matching analysis and calculating.  This can then be implemented into the compositor.  All the controls for this addon can be found in the UV editor window on the right shelf (click "n" if the shelf isn't visible).

## Calculate Picture
This simply takes the white and black RGB values for the selected image.  It's a good start, but keep in mind that heavily saturated colors can throw off the calculation.  For example, if the image's black pixels are RGB(0.1, 0.1, 0.1), but there's a heavily saturated red pixel with a RGB(0.99, 0.01, 0.01), the calculated min color will be RGB (0.1, 0.01, 0.01), which technically isn't the black value.  That's where the color picker comes in.

## Min/Max Color Picker
You use this just like a Blender color picker: hold Ctrl while you move the mouse to color pick, left click or right click to apply and finish, or "Escape" to cancel.  It will then take the lowest and highest R, G, and B values and update the panel's color values.

This is useful for when you need a black or white value of a certain area.  Some areas of an image have different color ranges than other parts.  So the color picker is helpful to isolate these areas.  The picker compares its results to the black and white values you currently have, so if you don't find a darker black or whiter white, it'll stay as it is.

## Reset
This is for your color picker, in case you accidentally pick an area that will throw off your black or white values.  This resets your min color to absolute white, and your max color to absolute black.

## Add to Compositor
Adds a color matching node group to your compositor, applying the black and white values you just calculated or picked!
