# from __future__ import print_function
import collections
import collections.abc
from pptx import Presentation
import pptx

from datetime import date
import matplotlib.pyplot as plt

# Functions go here
class MakePowerpoint:
    def init(self):
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
        graph_slide_layout = self.prs.slide_layouts[8]
        slide = self.prs.slides.add_slide(graph_slide_layout)
        title = slide.shapes.title
        title.text = title_below
        placeholder = slide.placeholders[1]
        pic = placeholder.insert_picture(figure_save_loc)
        subtitle = slide.placeholders[2]
        subtitle.text = description

    # def add_slide_from_fig(self, fig, plt, save_title_string, title_below, description):

    #     # commented stuff doesn't really work...
    #     # a = fig.get_axes()
    #     # ax = a[0]
    #     # the_title = ax.title.get_text()

    #     self.insert_slide(title_below, description, save_)

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
