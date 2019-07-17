# Color Matching Analyzer

The purpose of this addon is to speed up the compositing workflow with color matching analysis.  This can then be implemented into the compositor.  The controls for this addon can be found in the UV/Image editor window on the right shelf (click "n" if the shelf isn't visible), or on the left shelf of the Movie Clip editor.

Here's a list of the available operators/functions:

## The Calculator
This simply takes the white and black RGB values for the selected image or video.  It takes the HSV value of the color into account, so saturated colors shouldn't throw off the analyzer as much.  However, sometimes you need more precision, which is why I included the color picker.

Since it's unnecessary to analyze every frame of the movie clip, there's frame start, end and step fields.  Use these fields wisely, so you can balance between getting an accurate analysis while not increasing calculation time.  For the movie clip editor, the frame start and end fields must be within the length of the video in order to be enabled.  This is to prevent the frame analyzer to look at empty/missing frames.

## Color Picker
You use this just like a Blender color picker: hold Ctrl while you move the mouse to color pick, left click or right click to apply and finish, or "Escape" to cancel.  It will then take the lowest and highest R, G, and B values and update the panel's color values.

This is useful for when you need a black or white value of a certain area.  Some areas of an image have different color ranges than other parts.  So the color picker is helpful to isolate these areas.  The picker compares its results to the black and white values you currently have, so if you don't find a darker black or whiter white, it'll stay as it is.

Note: this feature is only available for the image editor.  If you'd need to color pick a movie clip frame, here's a workaround.  You can load video files into the UV editor, switch to the frame in the right panel (Image > Offset value field).

## Reset
This is for your color picker, in case you accidentally pick an area that will throw off your black or white values.  This resets your min color to absolute white, and your max color to absolute black.

## Add to Compositor
Adds a color matching node group to your compositor, applying the black and white values you just calculated or picked!
