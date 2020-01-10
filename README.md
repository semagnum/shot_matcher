# Shot Matcher

This addon improves the compositing workflow by matching two layers or shots together via color grading.  After analyzing the color ranges of two layers, the addon applies it to the compositor.  The controls for this addon can be found in the UV/Image editor window on the right shelf, or in the Movie Clip editor on the left shelf.

Here's a list of the available operators/functions:

## The Calculator
This simply takes the white and black RGB values for the selected image or video.  There's also an alpha threshold option when you're working with transparency in your layers.  This helps prevent transparent pixels from throwing off the calculator.  And when you need more precision, the color picker can extract the maximum and minimum colors in an area.

Since it's unnecessary to analyze every frame of the movie clip, there's frame start, end and step fields.  Use these fields wisely, so you can balance between getting an accurate analysis while keeping the calculation time low.  For the movie clip editor, the frame start and end fields must be within the length of the video in order to be analyzed.  This is to prevent the frame analyzer to look at empty/missing frames.

## Color Picker
While the color picker is on, hold Ctrl while you move the mouse to color pick, left click or right click to apply and finish, or "Escape" to cancel.  It will then take the "white" and "black" values picked and update the panel's color values.

This is useful for when you need the black or white values of a certain area.  Some areas of an image have different color ranges, like when there is multiple lights of different types in a shot.  Use the color picker to isolate these areas.  The picker compares its results to the black and white values you currently have, so if you don't find a darker black or whiter white, the current values will stay as it is.

Note: this feature is only available for the image editor.  If you'd need to color pick a movie clip frame, here's a workaround.  You can load video files into the UV editor, switch to the frame in the right panel (Image > Offset value field).

### Reset Color Picker
This is for your color picker, in case you accidentally picked an area that throws off your black or white values.  This resets your min color to absolute white, and your max color to absolute black.

## Applying to the Compositor

### Color Balance Node
Adds a color balance node to your compositor, mapping the black and white values from the foreground to the background.  This is for keeping color ranges consistent between images or clips.

### Alpha Over Node
Adds a color matching node group to your compositor, mapping the black and white values from the foreground to the background. This is for merging the layers into one image.
