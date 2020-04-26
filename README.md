
**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report




---

### Reflection

My pipeline first chops a video into images, that i then convert into grayscale. 

<img src="Output\grayscale.jpg"/>

On this I apply Gaussian smoothing, and then find the Canny edges, with the threshhold being 50 to 150. 

<img src="Output\Canny.jpg"/>


Afterward I want to specify the area in which I want to look for the lanes, I do this by isolating an area in which the lanes will appear in the image. 

<img src="Output\mask.jpg"/>

Finally I will look for lanes, since the Canny edges gave me a series of dots I used the Hough space to find the lanes, at this point I want to turn the lane markings into a linear equation which will mark the edge of my lane with a single straght line. To do this I first calculated the slopes of every line found, then filter out all the ones that dont satisfy my threshhold. next I sort the lines into right and left lane lines, I did this simply by sorting the end points of all lines depending on whether their position is before or after the middle point of the image. Now I need to isolate the end point of the lines and use the least squares method to get a single line that I will then draw onto the image itself.

<img src="Output\finalimg.jpg"/>

### 2. Possible improvments


One great shortcoming is that the code with struggle to place curved lines, another is that any damage to the road or faded lines might affect the output.

### 3. Potential Shortcomings

A possible improvement could be done to the way the lines are detected.

Another could be the way the the final line is calculated.