# Shot Matcher

This addon improves the compositing workflow by matching two layers or shots together via color grading.  After analyzing the color ranges of two layers, the addon applies it to the compositor.  The controls for this addon can be found in the Image editor window on the right shelf, or in the Movie Clip editor on the left shelf.

Here's a list of the available operators/functions:

## Auto Calculator
This simply takes the max and min RGB values for the selected image or video.  There's also an alpha threshold option when you're working with transparency in your layers.  This helps prevent transparent pixels from throwing off the calculator.  And when you need more precision, the color picker can extract the maximum and minimum colors in an area.

Since it's unnecessary to analyze every frame of the movie clip, there's frame start, end and step fields.  Use these fields wisely to balance between an accurate analysis and a quick calculation time.  The frame start and end fields must be within the video's duration to analyze the video.  This is to prevent errors.

## Color Picker
While the color picker is on, hold Ctrl while you move the mouse to color pick, left click or right click to apply and finish, or "Escape" to cancel.  It will then take the "white" and "black" values picked and update the panel's color values.

Tips:
- This is useful to get black or white values of a certain area of the picture.
- The picker compares its results to the black and white values you currently have, so if you don't find a darker black or whiter white, the current values will stay as it is.
- The picker takes your alpha threshold settings into account, so you can pick only the opaque parts of images.

Note: this feature is only available for the image editor.  If you'd need to color pick a movie clip frame, here's a workaround.  You can open video files as images, and then you can analayze frames from the image editor.

### Reset Color Picker
This is for your color picker, in case you accidentally picked an area that throws off your black or white values.  This resets your min color to absolute white, and your max color to absolute black.

### Set as Selected
This allows you to set the current image or video you're viewing as the background or foreground layer.  The Shot Matcher's can analyze any image or video refrenced in the Blender file, regardless of whether it's visible.

## Applying to the Compositor

### Color Balance Node
Adds a color balance node to your compositor, mapping the black and white values from the foreground to the background.  This is for keeping color ranges consistent between images or clips.

### Alpha Over Node
Adds a color matching node group to your compositor, mapping the black and white values from the foreground to the background. This is for merging the layers into one image.
