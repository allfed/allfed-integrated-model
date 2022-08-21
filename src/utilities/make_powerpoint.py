# from __future__ import print_function
from pptx import Presentation

from datetime import date

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN


# Functions go here
class MakePowerpoint:
    def __init__(self):
        pass

    def create_title_slide(self, the_title):
        self.prs = Presentation()
        # Create a title slide first
        title_slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        subtitle.text = "Generated on {:%m-%d-%Y}".format(date.today())

        # Use the output from analyze_ppt to understand which layouts and placeholders
        # to use
        title.text = the_title

    def insert_slide(self, title_below, description, figure_save_loc):
        slide_layout = self.prs.slide_layouts[5]
        slide = self.prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        title.text = title_below
        slide.shapes.add_picture(
            image_file=figure_save_loc,
            left=Inches(0.5),
            top=Inches(2),
            width=Inches(6),
            height=Inches(5),
        )

        textbox = slide.shapes.add_textbox(
            left=Inches(7), top=Inches(2), width=Inches(3), height=Inches(5)
        )

        tf = textbox.text_frame

        para = tf.add_paragraph()
        para.text = description
        para.alignment = PP_ALIGN.LEFT
        para.font.size = Pt(10)

    def save_ppt(self, pres_name):
        self.prs.save(pres_name)


if __name__ == "__main__":
    the_title = "the_title"
    mp = MakePowerpoint()
    mp.create_title_slide(the_title)

    mp.insert_slide(
        "title_below",
        "description",
        "../../results/large_reports/" + the_title + ".png",
    )
    mp.save_ppt("baseline.pptx")
