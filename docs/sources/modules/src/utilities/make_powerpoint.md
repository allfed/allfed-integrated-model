#


## MakePowerpoint
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/make_powerpoint.py/#L15)
```python 

```




**Methods:**


### .create_title_slide
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/make_powerpoint.py/#L22)
```python
.create_title_slide(
   the_title
)
```

---
Creates a title slide with the given title and today's date as the subtitle.


**Args**

* **the_title** (str) : The title to be displayed on the slide.


**Returns**

None

### .insert_slide
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/make_powerpoint.py/#L49)
```python
.insert_slide(
   title_below, description, figure_save_loc
)
```

---
Inserts a slide into the PowerPoint presentation with a title, description, and figure.


**Args**

* **title_below** (str) : The title of the slide.
* **description** (str) : The description of the slide.
* **figure_save_loc** (str) : The file path of the figure to be added to the slide.


**Returns**

None

### .save_ppt
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/make_powerpoint.py/#L94)
```python
.save_ppt(
   pres_name
)
```

---
Saves the PowerPoint presentation with the given name.


**Args**

* **self**  : the PowerPoint presentation object
* **pres_name** (str) : the name of the PowerPoint presentation to save


**Returns**

None

### .insert_slide_with_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/make_powerpoint.py/#L107)
```python
.insert_slide_with_feed(
   title_below, description, figure_save_loc, feed_figure_save_loc
)
```

---
Inserts a slide with a title, two images, and a textbox with a description.


**Args**

* **title_below** (str) : The title of the slide.
* **description** (str) : The description to be added to the textbox.
* **figure_save_loc** (str) : The file path of the first image to be added.
* **feed_figure_save_loc** (str) : The file path of the second image to be added.


**Returns**

None

### .save_ppt
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/make_powerpoint.py/#L94)
```python
.save_ppt(
   pres_name
)
```

---
Saves the PowerPoint presentation with the given name.


**Args**

* **self**  : the PowerPoint presentation object
* **pres_name** (str) : the name of the PowerPoint presentation to save


**Returns**

None
