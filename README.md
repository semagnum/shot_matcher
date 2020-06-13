# Shot Matcher

This addon improves the compositing workflow by matching two layers or shots together via color grading.  After analyzing the color ranges of two layers, the addon applies it to the compositor.  The controls for this addon can be found in the Image editor window on the right shelf, or in the Movie Clip editor on the left shelf.

Here's a list of the available operators/functions:

## Auto Calculator
This simply takes the max and min RGB values for the selected image or video.  There's also an alpha threshold option when you're working with transparency in your layers.  This helps prevent transparent pixels from throwing off the calculator.  And when you need more precision, the color picker can extract the maximum and minimum colors in an area.

Since it's unnecessary to analyze every frame of the movie clip, there's frame start, end and step fields.  Use these fields wisely to balance between an accurate analysis and a quick calculation time.  The frame start and end fields must be within the video's duration to analyze the video.  This is to prevent errors.

## Color Picker
While the color picker is on, left click and drag the mouse to color pick, right click to apply and finish, or "Escape" to cancel.  It will then take the "white" and "black" values picked and update the panel's color values.

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

# How to Use

1. Select your background and foreground layers.  The background is the image or video that will be "behind" the foreground layer in your final composition.  It's also the layer that the foreground's color range will be mapped to.  You can select the image or movie clip from the textbox or the "Use Current Image/Clip" button to get the file you are currently viewing.
2. For the background layer, analyze and get the colors representing black and white in the image. Use pixels of the picture/video that represent black or white colors for reference, preferably in the area that your foreground layer will be composited to.
    * For images, you can use either the auto calculator or the color picker.  For the calculator, simply press the button and let it pick the max and min RGB values in the image.  It can get close, but usually the color picker is best.  To use the color picker, first click "Reset Colors" in the Shot Matcher panel.  Click "Color Pick" and find the pixels meant to represent the colors white and black.  Hover over the area, hold down the left mouse button, and move the cursor to pick up the colors. You should see the white and black colors in the panel update as you do so. You simply click the left or right mouse button to accept your changes, or press "Escape" to cancel. Feel free to do it again and again to update the current white and black colors you have, or you can restart with "Reset Colors."
    * For movie clips, only the auto calculator is available.  There's three parameters: start frame, end frame, and frame step.  Whenever you run the analysis, the addon will iterate from "start frame" to "end frame," using the "frame step" as the increment value. For example, if the parameters above were (1, 250, 10), the addon will look at frames 1, 11, 21,...231, and 241.
    * Note: if you insist to color pick a movie clip, simply load the movie clip into Blender as an image.  On the side panel, you can change the current frame to your liking.
3. Repeat the previous step for the foreground layer.
4. Once you've gotten the values for each layer, select one of the node groups to generate.  The "alpha over" is for typical compositing, while the color balance one is helpful for shot matching.
5. If you need to update the colors, just adjust them and click the node button again, and it'll simply update the existing node or group instead of recreating it!  It's based on the node label or group name, so if you change those, the addon will create a new one instead of updating.

# Auto-saving and Purging Settings
Just for your information, the layer settings are saved for each image and movie clip you use.  The layers are saved whenever you change layers in the Shot Matcher panel (done by selecting a different image or movie in the dropdown), as well as when you save your Blender project.  Upon loading your Blender project, the addon will check if each layer setting can find the correlating image or movie clip.  If no matching image or movie clip can be found, the setting will be removed to save space.
