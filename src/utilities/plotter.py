"""
################################ plotter.py ###################################
##                                                                            #
##            A set of utility functions useful for plotting                  #
##                                                                            #
###############################################################################
"""

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
import os
import pandas as pd
from src.utilities.make_powerpoint import MakePowerpoint

from pathlib import Path
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

import git

plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"

repo_root = git.Repo(".", search_parent_directories=True).working_dir

# in some linux win manager setups matplotlib plotting doesn't seem to play nice
# matplotlib.use('Svg')
# matplotlib.use('QtAgg')


# font = {"family": 'normal', "weight": "bold", "size": 7}
font = {"weight": "bold", "size": 7}
if "normal" in matplotlib.font_manager.findSystemFonts():
    font["family"] = "normal"
elif "sans-serif" in matplotlib.font_manager.findSystemFonts():
    font["family"] = "sans-serif"
    print("Warning: primary font not found, using sans-serif font")
else:
    font["family"] = "Arial"  # or any other available font family
    print("Warning: primary font not found, using Arial font")


matplotlib.rc("font", **font)


class Plotter:
    def __init__(self):
        """
        Initializes a new instance of the Plotter class.
        Args:
            None
        Returns:
            None
        """
        pass

    @classmethod
    def plot_fig_1ab(
        crs,
        interpreter,
        xlim,
        newtitle="",
        plot_figure=True,
        add_slide_with_fig=True,
        description="",
    ):
        """
        Plots two figures: one for food availability and one for available food macronutrition.
        Args:
            crs (object): an object of class CRS
            interpreter (object): an object of class Interpreter
            xlim (int): the maximum limit for the x-axis
            newtitle (str): the title of the plot
            plot_figure (bool): whether to plot the figure or not
            add_slide_with_fig (bool): whether to add a slide with the figure or not
            description (str): the description of the slide to be added
        Returns:
            None
        """

        # If plot_figure and add_slide_with_fig are both False, return
        if (not plot_figure) and (not add_slide_with_fig):
            return

        # Check if the nutrition plot needs to be added
        ADD_THE_NUTRITION_PLOT = interpreter.include_protein or interpreter.include_fat

        # Set the x-axis limit
        xlim = min(xlim, len(interpreter.time_months_middle))

        # Get the legend for the plot
        legend = Plotter.get_people_fed_legend(interpreter, True)

        # Create a new figure
        fig = plt.figure()

        # Set the color palette
        pal = [
            "#1e7ecd",
            "#71797E",
            "#e75480",
            "#76d7ea",
            "#056608",
            "#f3f4e3",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        # Loop through the two subplots
        for i, label in enumerate(("a", "b")):
            # If the nutrition plot needs to be added, add a subplot for it
            if ADD_THE_NUTRITION_PLOT:
                ax = fig.add_subplot(1, 2, i + 1)
            # Otherwise, add a subplot for the food availability plot
            else:
                if label == "b":
                    continue
                ax = fig.add_subplot(1, 1, 1)

            # Set the x-axis limit
            ax.set_xlim([0.5, xlim])

            # Get the y-data for the plot
            ykcals = []
            ykcals.append(interpreter.fish_kcals_equivalent.kcals)
            ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
            ykcals.append(interpreter.scp_kcals_equivalent.kcals)
            ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
            ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
            ykcals.append(
                (
                    interpreter.grazing_milk_kcals_equivalent.kcals
                    + interpreter.grain_fed_milk_kcals_equivalent.kcals
                )
            )
            ykcals.append(
                (
                    interpreter.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                    + interpreter.grain_fed_meat_kcals_equivalent.kcals
                )
            )
            ykcals.append(interpreter.immediate_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

            # If the current subplot is for the food availability plot
            if label == "a":
                # If the nutrition plot needs to be added, add the label to the top left corner
                if ADD_THE_NUTRITION_PLOT:
                    ax.text(
                        -0.06,
                        1.1,
                        label,
                        transform=ax.transAxes,
                        fontsize=11,
                        fontweight="bold",
                        va="top",
                        ha="right",
                    )
                # Plot the stacked area chart
                ax.stackplot(
                    interpreter.time_months_middle,
                    np.array(ykcals),
                    labels=legend,
                    colors=pal,
                )

                # Get the maximum y-value for the plot
                # Either plot the max y anywhere in the plot, or just within region plotted
                PLOT_MAXIMUM_VALUE = False
                if PLOT_MAXIMUM_VALUE:
                    maxy = max([sum(x[0:xlim]) for x in ykcals])
                else:
                    maxy = 0
                    maxy = max(maxy, sum([x[i] for x in ykcals]))
                maxy += maxy / 20

                # Set the y-axis limit
                ax.set_ylim([0, maxy])

                # Set the y-axis label
                plt.ylabel("Kcals / capita / day")

            # If the current subplot is for the available food macronutrition plot
            if label == "b":
                # If the nutrition plot doesn't need to be added, skip this subplot
                if not ADD_THE_NUTRITION_PLOT:
                    continue

                # Add the label to the top left corner
                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )

                # Set the x-axis label
                plt.xlabel("Months since May nuclear winter onset")

                # Plot the kcals fed
                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.kcals_fed,
                    color="blue",
                    linestyle="solid",
                )

                # If protein is included, plot the protein fed
                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.protein_fed,
                        color="red",
                        linestyle="dotted",
                    )

                # If fat is included, plot the fat fed
                if interpreter.include_fat:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.fat_fed,
                        color="green",
                        linestyle="dashed",
                    )

                # Set the y-axis label
                ax.set_ylabel("Percent of minimum recommendation")

            # If the current subplot is for the food availability plot
            if label == "a":
                # If the nutrition plot needs to be added, set the legend location
                if ADD_THE_NUTRITION_PLOT:
                    legend_loc = (-0.15, -0.4)
                # Otherwise, set the legend location
                else:
                    legend_loc = (0, -0.2)

                # Get the handles and labels for the legend
                handles, labels = ax.get_legend_handles_labels()

                # Add the legend to the plot
                plt.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=legend_loc,
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels),
                )

            # If the current subplot is for the available food macronutrition plot
            if label == "b":
                # Add the legend to the plot
                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=["Calories", "Fat", "Protein"],
                )

            # If the current subplot is for the food availability plot
            if label == "a":
                # If the nutrition plot needs to be added, set the title
                if ADD_THE_NUTRITION_PLOT:
                    plt.title("Food availability")
                # Otherwise, set the title with the newtitle argument
                else:
                    plt.title("Food availability, " + newtitle)

            # If the current subplot is for the available food macronutrition plot
            if label == "b":
                # Set the title
                plt.title("Available food macronutrition")

            # Set the x-axis label
            plt.xlabel("Months since May nuclear winter onset")

        # Set the figure size
        fig.set_figheight(8)
        fig.set_figwidth(8)

        # Set the layout
        plt.tight_layout()

        # If the nutrition plot needs to be added, set the figure title
        if ADD_THE_NUTRITION_PLOT:
            fig.suptitle(newtitle)

        # Set the path string for saving the figure
        path_string = str(Path(repo_root) / "results" / "large_reports" / "no_trade")

        # Set the save location for the figure
        saveloc = path_string + newtitle + ".png"
        feed_saveloc = path_string + newtitle + "_feed.png"

        # Save the figure
        plt.savefig(
            saveloc,
            dpi=300,
        )

        # If add_slide_with_fig is True and show_feed_biofuels is True, add a slide with the feed biofuels figure
        if add_slide_with_fig:
            if interpreter.show_feed_biofuels:
                crs.mp.insert_slide_with_feed(
                    title_below=newtitle
                    + ": Percent fed:"
                    + str(round(interpreter.percent_people_fed, 1))
                    + "%",
                    description=description,
                    figure_save_loc=saveloc,
                    feed_figure_save_loc=feed_saveloc,
                )
            # Otherwise, add a slide with the figure
            else:
                crs.mp.insert_slide(
                    title_below=newtitle
                    + ": Percent fed:"
                    + str(round(interpreter.percent_people_fed, 1))
                    + "%",
                    description=description,
                    figure_save_loc=saveloc,
                )

        # If plot_figure is True, show the figure
        if plot_figure:
            plt.show()
        # plt.close()

    @classmethod
    def plot_feed(
        crs,
        interpreter,
        xlim,
        newtitle="",
        plot_figure=True,
        add_slide_with_fig=True,
        description="",
    ):
        """
        Plots feed and biofuel usage and macronutrition used.

        Args:
            crs: The CRS object
            interpreter: The Interpreter object
            xlim: The limit of the x-axis
            newtitle: The title of the plot
            plot_figure: Whether to plot the figure or not
            add_slide_with_fig: Whether to add slide with figure or not
            description: The description of the plot

        Returns:
            None

        Example:
            >>>
            >>> plot_feed(crs, interpreter, 10, "Feed and Biofuel Usage", True, True, "Feed and Biofuel Usage plot")

        """
        print("feed")
        if (not plot_figure) and (not add_slide_with_fig):
            return

        ADD_THE_NUTRITION_PLOT = interpreter.include_protein or interpreter.include_fat

        xlim = min(xlim, len(interpreter.time_months_middle))
        legend = Plotter.get_feed_biofuels_legend(interpreter)
        fig = plt.figure()
        pal = [
            "#71797E",  # CS
            "#e75480",  # SCP
            "#056608",  # seaweeed
            "#a5d610",  # OG
            "#e7d2ad",  # stored food
            "#71797E",  # CS
            "#e75480",  # SCP
            "#056608",  # seaweeed
            "#a5d610",  # OG
            "#e7d2ad",  # stored food
        ]
        hatches_list = [
            "",
            "",
            "",
            "",
            "",
            "xx",
            "xx",
            "xx",
            "xx",
            "xx",
        ]
        # custom_handles = [
        #     Patch(facecolor=pal[i], hatch=hatches_list[i] * 2, label=legend[i])
        #     for i in range(len(legend))
        # ]

        for i, label in enumerate(("a", "b")):
            if ADD_THE_NUTRITION_PLOT:
                ax = fig.add_subplot(1, 2, i + 1)
            else:
                if label == "b":
                    continue
                ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim([0.5, xlim])

            ykcals = []
            ykcals.append(interpreter.cell_sugar_feed_kcals_equivalent.kcals)
            ykcals.append(interpreter.scp_feed_kcals_equivalent.kcals)
            ykcals.append(interpreter.seaweed_feed_kcals_equivalent.kcals)
            ykcals.append(interpreter.outdoor_crops_feed_kcals_equivalent.kcals)
            ykcals.append(interpreter.stored_food_feed_kcals_equivalent.kcals)
            ykcals.append(interpreter.cell_sugar_biofuels_kcals_equivalent.kcals)
            ykcals.append(interpreter.scp_biofuels_kcals_equivalent.kcals)
            ykcals.append(interpreter.seaweed_biofuels_kcals_equivalent.kcals)
            ykcals.append(interpreter.outdoor_crops_biofuels_kcals_equivalent.kcals)
            ykcals.append(interpreter.stored_food_biofuels_kcals_equivalent.kcals)

            if label == "a":
                if ADD_THE_NUTRITION_PLOT:
                    ax.text(
                        -0.06,
                        1.1,
                        label,
                        transform=ax.transAxes,
                        fontsize=11,
                        fontweight="bold",
                        va="top",
                        ha="right",
                    )

                stack_plots = ax.stackplot(
                    interpreter.time_months_middle,
                    np.array(ykcals),
                    labels=legend,
                    colors=pal,
                )
                # Add hatches to the biofuel patches
                for stack_plot, hatch in zip(stack_plots, hatches_list):
                    stack_plot.set_hatch(hatch)

                # get the sum of all the ydata up to xlim month,
                # then find max month
                # maxy = max(sum([x[0:xlim] for x in ykcals]))
                # maxy = max([sum(x[0:xlim]) for x in ykcals])
                print("xlim")
                print(xlim)
                maxy = max([sum(x[0:xlim]) for x in ykcals])

                maxy = 0
                for i in range(xlim):
                    maxy = max(maxy, sum([x[i] for x in ykcals]))

                maxy += maxy / 20
                ax.set_ylim([0, maxy])
                # ax.set_ylim([0, maxy])

                plt.ylabel("Kcals / capita / day")
            if label == "b":
                if not ADD_THE_NUTRITION_PLOT:
                    continue
                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )
                plt.xlabel("Months since May nuclear winter onset")

                # note: nonhuman consumption is pre-waste, because it is assumed to occur
                # before the waste happens

                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.nonhuman_consumption.kcals,
                    color="blue",
                    linestyle="solid",
                )

                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.nonhuman_consumption.protein,
                        color="red",
                        linestyle="dotted",
                    )

                if interpreter.include_fat:
                    # 1 gram of fat is 9 kcals.
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.nonhuman_consumption.fat,
                        color="green",
                        linestyle="dashed",
                    )

                ax.set_ylabel("Percent of minimum human recommendation as feed")
                # ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            if label == "a":
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                if ADD_THE_NUTRITION_PLOT:
                    legend_loc = (-0.15, -0.4)
                else:
                    legend_loc = (0, -0.2)
                plt.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=legend_loc,
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels),
                )

            if label == "b":
                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=["Calories", "Fat", "Protein"],
                )

            if label == "a":
                if ADD_THE_NUTRITION_PLOT:
                    plt.title("Feed + Biofuel Usage")
                else:
                    plt.title("Feed + Biofuel Usage, " + newtitle)

            if label == "b":
                plt.title("Feed + Biofuel macronutrition used")

            plt.xlabel("Months since May nuclear winter onset")

        # plt.rcParams["figure.figsize"] = [12.50, 10]

        fig.set_figheight(8)
        fig.set_figwidth(8)
        plt.tight_layout()
        if ADD_THE_NUTRITION_PLOT:
            fig.suptitle(newtitle)
        path_string = str(Path(repo_root) / "results" / "large_reports" / "no_trade")

        saveloc = path_string + newtitle + "_feed.png"
        plt.savefig(
            saveloc,
            dpi=300,
        )
        if plot_figure:
            plt.show()
        # else:
        # plt.close()

    @classmethod
    def plot_fig_1ab_updated(
        crs,
        worlds,
        ratios,
        xlim,
    ):
        """
        Plots two figures (a and b) side by side, each with 5 subplots, for a total of 10 subplots.
        Each subplot shows a choropleth map of a world's caloric needs ratio, with a title indicating
        the world's name and the percentage of caloric needs met.
        Args:
            crs (str): Coordinate reference system for the choropleth maps.
            worlds (dict): A dictionary of geopandas.GeoDataFrame objects, each representing a world.
            ratios (dict): A dictionary of the percentage of caloric needs met for each world.
            xlim (tuple): A tuple of the minimum and maximum longitude values to display in the maps.
        Returns:
            None
        """
        fig = plt.figure(figsize=(10, 10))

        scenario_labels = list(worlds.keys())
        gs = gridspec.GridSpec(
            6,
            4,
            wspace=0,
            hspace=0,
            width_ratios=[1, 2, 1, 2],
            height_ratios=[2, 2, 2, 2, 2, 0.5],
        )

        # Define indices for the subplots in figures a and b
        figure_a_text_indices = [0, 4, 8, 12, 16]
        figure_a_indices = [1, 5, 9, 13, 17]
        figure_b_text_indices = [2, 6, 10, 14, 18]
        figure_b_indices = [3, 7, 11, 15, 19]

        # Loop through all subplots
        for i in range(22):
            if i == 21:
                # Add colorbar for figure b
                ax = fig.add_subplot(gs[5, :])
                a = np.array([[0, 1]])
                plt.imshow(a, cmap="viridis")
                plt.gca().set_visible(False)
                plt.colorbar(
                    orientation="horizontal",
                    ax=ax,
                    label="Fraction of minimum caloric needs met",
                    aspect=30,
                    fraction=0.5,
                )

            if i in figure_a_text_indices:
                # Add text for figure a
                row_index = i // 4
                scenario_label = scenario_labels[row_index]
                ax = fig.add_subplot(gs[row_index, 0])

            if i in figure_a_indices:
                # Add choropleth map for figure a
                row_index = (i - 1) // 4
                scenario_label = scenario_labels[row_index]
                ax = fig.add_subplot(gs[row_index, 1])
            elif i in figure_b_text_indices:
                # Add text for figure b
                row_index = (i - 2) // 4
                scenario_label = scenario_labels[row_index + 5]
                ax = fig.add_subplot(gs[row_index, 2])
            elif i in figure_b_indices:
                # Add choropleth map for figure b
                row_index = (i - 3) // 4
                scenario_label = scenario_labels[row_index + 5]
                ax = fig.add_subplot(gs[row_index, 3])

            ratio = ratios[scenario_label]
            world = worlds[scenario_label]

            ax.axis("off")

            if i in figure_a_text_indices or i in figure_b_text_indices:
                # Add title text to the subplot
                ax.text(
                    0.6,
                    0.5,
                    (scenario_label + "\n\nNeeds met: " + str(int(ratio)) + "%"),
                    fontweight="bold",
                    bbox={
                        "facecolor": "white",
                        "alpha": 1,
                        "edgecolor": "none",
                        "pad": 1,
                    },
                    ha="center",
                    va="center",
                )
            if i in figure_a_indices or i in figure_b_indices:
                # Add choropleth map to the subplot
                world.plot(
                    ax=ax,
                    column="needs_ratio",
                    cmap="viridis",
                )

                world.boundary.plot(ax=ax, color="Black", linewidth=0.1)
                ax.axes.get_xaxis().set_ticks([])
                ax.axes.get_yaxis().set_ticks([])

        # Save and display the figure
        plt.savefig(
            Path(repo_root) / "results" / "fig_1ab.png",
            dpi=300,
            facecolor=fig.get_facecolor(),
            transparent=False,
            edgecolor="none",
        )

        plt.tight_layout()
        plt.show()

    def helper_for_plotting_fig_3abcde(interpreter, xlim, gs, row, fig, max_y_percent):
        """
        This function plots the figure 3abcde for the model output.

        Args:
            interpreter (Interpreter): An instance of the Interpreter class.
            xlim (int): The maximum limit of the x-axis.
            gs (GridSpec): The GridSpec object for the figure.
            row (int): The row number of the subplot.
            fig (Figure): The Figure object for the plot.
            max_y_percent (int): The maximum limit of the y-axis in percentage.

        Returns:
            GridSpec: The GridSpec object for the figure.
            Figure: The Figure object for the plot.
        """

        # Set the maximum limit of the x-axis to the minimum of xlim and the length of the time_months_middle list.
        xlim = min(xlim, len(interpreter.time_months_middle))

        # Define the legend and color palette for the plot.
        legend = Plotter.get_people_fed_legend(interpreter, True)
        pal = [
            "#1e7ecd",  # fish
            "#71797E",  # CS
            "#e75480",  # SCP
            "#76d7ea",  # greenhouses
            "#056608",  # seaweeed
            "#f3f4e3",  # milk
            "#ff0606",  # meat
            "#a5d610",  # immediate OG
            "#ffeb7a",  # new stored OG
            "#e7d2ad",  # stored food
        ]

        # Loop through the labels "a" and "b".
        for i, label in enumerate(("a", "b")):
            ykcals = []

            # Append the kcals equivalent for each food source to the ykcals list.
            ykcals.append(interpreter.fish_kcals_equivalent.kcals)
            ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
            ykcals.append(interpreter.scp_kcals_equivalent.kcals)
            ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
            ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
            ykcals.append(
                (
                    interpreter.grazing_milk_kcals_equivalent.kcals
                    + interpreter.grain_fed_milk_kcals_equivalent.kcals
                )
            )
            ykcals.append(
                (
                    interpreter.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                    + interpreter.grain_fed_meat_kcals_equivalent.kcals
                )
            )
            ykcals.append(interpreter.immediate_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

            # If the label is "a", create a subplot for the stackplot.
            if label == "a":
                ax = fig.add_subplot(gs[row, 1])

                # If the row is 3, add the legend to the stackplot.
                if row == 3:
                    ax.stackplot(
                        interpreter.time_months_middle,
                        np.array(ykcals),
                        labels=legend,
                        colors=pal,
                    )
                else:
                    ax.stackplot(
                        interpreter.time_months_middle,
                        np.array(ykcals),
                        colors=pal,
                    )

                # If the row is 3, add the x-axis label to the plot.
                if row == 3:
                    plt.xlabel("Months since May nuclear winter onset", fontsize=9)

                # Set the maximum limit of the y-axis to the maximum of the sum of all the ydata up to xlim month.
                maxy = 0
                for i in range(xlim):
                    if max_y_percent != -1:
                        maxy = max_y_percent / 100 * 2100
                    else:
                        maxy = max(maxy, sum([x[i] for x in ykcals]))

                ax.set_ylim([0, maxy])
                plt.ylabel("Kcals / capita / day", fontsize=9)

            # If the label is "b", create a subplot for the line plot.
            if label == "b":
                ax = fig.add_subplot(gs[row, 2])

                # Plot the kcals fed.
                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.kcals_fed,
                    color="blue",
                    linestyle="solid",
                )

                # If include_protein is True, plot the protein fed.
                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.protein_fed,
                        color="red",
                        linestyle="dotted",
                    )

                # If include_fat is True, plot the fat fed.
                if interpreter.include_fat:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.fat_fed,
                        color="green",
                        linestyle="dashed",
                    )

                # If max_y_percent is not -1, set the maximum limit of the y-axis to max_y_percent.
                if max_y_percent != -1:
                    ax.set_ylim([0, max_y_percent])

                ax.set_ylabel("% min recommended", fontsize=9)
                ax.set_xlim([0.5, xlim])

                # If the label is "a", add the title and legend to the plot.
                if label == "a":
                    if row == 1:
                        plt.title(
                            "Needs Met, Caloric\n", fontsize=10, fontweight="bold"
                        )

                    # Get the handles and labels for the legend.
                    handles, labels = ax.get_legend_handles_labels()

                    # If the row is 3, add the legend to the plot.
                    if row == 3:
                        plt.legend(
                            loc="center left",
                            frameon=False,
                            bbox_to_anchor=(0, -1.1),
                            shadow=False,
                            handles=reversed(handles),
                            labels=reversed(labels),
                        )

                # If the label is "b", add the title and legend to the plot.
                if label == "b":
                    if row == 3:
                        ax.legend(
                            loc="center left",
                            frameon=False,
                            bbox_to_anchor=(-0.05, -0.6),
                            shadow=False,
                            labels=["Calories", "Fat", "Protein"],
                        )
                    if row == 1:
                        plt.title(
                            "Needs Met, All Macronutrients\n",
                            fontsize=10,
                            fontweight="bold",
                        )

                # If the row is 3, add the x-axis label to the plot.
                if row == 3:
                    plt.xlabel("Months since May nuclear winter onset", fontsize=9)

        # Return the GridSpec and Figure objects.
        return gs, fig

    def helper_for_plotting_fig_2abcde(
        ax,
        interpreter,
        xlim,
        title,
        add_ylabel=True,
        add_xlabel=True,
        ylim_constraint=100000,
    ):
        """
        Helper function for plotting figures 2a, 2b, 2c, 2d, and 2e.

        Args:
            ax (matplotlib.axes.Axes): The axes object to plot on.
            interpreter (Interpreter): The interpreter object containing the data to plot.
            xlim (int): The maximum x-axis limit.
            title (str): The title of the plot.
            add_ylabel (bool, optional): Whether to add a y-axis label. Defaults to True.
            add_xlabel (bool, optional): Whether to add an x-axis label. Defaults to True.
            ylim_constraint (int, optional): The maximum y-axis limit. Defaults to 100000.

        Returns:
            tuple: A tuple containing the axes object, the legend, and the color palette.

        Example:
            >>> ax, legend, pal = helper_for_plotting_fig_2abcde(ax, interpreter, xlim, title)
        """

        # Set the x-axis limit to the minimum of xlim and the length of the time_months_middle array
        xlim = min(xlim, len(interpreter.time_months_middle))

        # Define the legend and color palette
        legend = Plotter.get_people_fed_legend(interpreter, True)
        pal = [
            "#1e7ecd",
            "#71797E",
            "#e75480",
            "#76d7ea",
            "#056608",
            "#f3f4e3",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        # Get the kcals for each food source and append them to the ykcals list
        ykcals = []
        ykcals.append(interpreter.fish_kcals_equivalent.kcals)
        ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
        ykcals.append(interpreter.scp_kcals_equivalent.kcals)
        ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
        ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
        ykcals.append(
            (
                interpreter.grazing_milk_kcals_equivalent.kcals
                + interpreter.grain_fed_milk_kcals_equivalent.kcals
            )
        )
        ykcals.append(
            (
                interpreter.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                + interpreter.grain_fed_meat_kcals_equivalent.kcals
            )
        )
        ykcals.append(interpreter.immediate_outdoor_crops_kcals_equivalent.kcals)
        ykcals.append(interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals)
        ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

        # Stack the ykcals data and plot it
        ax.stackplot(
            interpreter.time_months_middle,
            np.array(ykcals),
            colors=pal,
        )

        # Get the maximum y-value up to the xlim month
        maxy = 0
        for i in range(xlim):
            maxy = max(maxy, sum([x[i] for x in ykcals]))

        # Set the y-axis limit to the minimum of maxy and ylim_constraint
        ax.set_ylim([0, min(maxy, ylim_constraint)])
        ax.set_xlim([0, xlim])

        # Add axis labels if specified
        if add_ylabel:
            plt.ylabel("Kcals / capita / day", fontsize=9)
        if add_xlabel:
            plt.xlabel("Months since May nuclear winter onset", fontsize=9)

        # Set the plot title
        plt.title(
            title,
            fontweight="bold",
            fontsize=9,
        )

        # Get the handles for the legend
        handles, labels = ax.get_legend_handles_labels()

        # Return the axes object, legend, and color palette
        return ax, legend, pal

    @classmethod
    def plot_fig_2abcde_updated(
        crs,
        lists_of_lists,
        xlim,
    ):
        """
        Plots a figure with multiple subplots, each containing a map and text.
        Args:
            crs (str): coordinate reference system
            lists_of_lists (list): a list of lists containing data to be plotted
            xlim (tuple): a tuple containing the minimum and maximum x-axis limits
        Returns:
            None
        """
        # set up the figure and grid
        fig = plt.figure(figsize=(10, 10))
        fig.set_facecolor("white")
        gs = gridspec.GridSpec(
            7,
            3,
            wspace=0.3,
            hspace=0.5,
            width_ratios=[0.25, 2, 2],
            height_ratios=[0.5, 2, 2, 2, 2, 2, 3],
            left=0.02,
            right=0.98,
            top=0.98,
            bottom=0.02,
        )

        # set up the indices for the subplots
        figure_a_indices = [0, 1, 2, 3, 4]
        figure_b_indices = [5, 6, 7, 8, 9]
        ax = []

        # add the first two subplots
        ax = fig.add_subplot(gs[0, 1])
        ax.text(
            0.5,
            0.5,
            ("Example Scenario"),
            fontweight="bold",
            bbox={
                "facecolor": "white",
                "alpha": 1,
                "edgecolor": "none",
                "pad": 1,
            },
            ha="center",
            va="center",
            fontsize=10,
        )
        ax.axis("off")

        ax = fig.add_subplot(gs[0, 2])
        ax.text(
            0.5,
            0.5,
            ("Example Scenario + Resilient Foods"),
            fontweight="bold",
            bbox={
                "facecolor": "white",
                "alpha": 1,
                "edgecolor": "none",
                "pad": 1,
            },
            fontsize=10,
            ha="center",
            va="center",
        )
        ax.axis("off")

        # loop through the data and add the remaining subplots
        for i in range(10):
            people_fed = int(lists_of_lists[i][0])
            country_name = lists_of_lists[i][1]
            interpreter = lists_of_lists[i][2]
            scenario_label = lists_of_lists[i][3]
            print(country_name)

            # add the colorbar subplot
            if i == 10:
                ax = fig.add_subplot(gs[5, :])
                a = np.array([[0, 1]])
                plt.imshow(a, cmap="viridis")
                plt.gca().set_visible(False)
                plt.colorbar(
                    orientation="horizontal",
                    ax=ax,
                    label="Fraction minimum caloric needs met",
                    aspect=30,
                    fraction=0.5,
                )

            # add the subplots for figure a
            if i in figure_a_indices:
                add_ylabel = True
                row_index = i
                ax.axis("off")
                ax = fig.add_subplot(gs[row_index + 1, 0])
                ax.text(
                    0.5,
                    0.5,
                    country_name,  # + "\n\nNeeds met: " + str(people_fed) + "%"),
                    fontweight="bold",
                    bbox={
                        "facecolor": "white",
                        "alpha": 1,
                        "edgecolor": "none",
                        "pad": 1,
                    },
                    ha="center",
                    va="center",
                    rotation=90,
                    fontsize=10,
                )

                ax.axis("off")
                ax = fig.add_subplot(gs[row_index + 1, 1])
                # figure a
            # add the subplots for figure b
            elif i in figure_b_indices:
                add_ylabel = False
                row_index = i - 5
                ax.axis("off")
                ax = fig.add_subplot(gs[row_index + 1, 2])
                # xticks = ax.get_xticks()
                # ax.set_xticklabels(xticks, rotation=0, fontsize=9)
                # ax.xaxis.set_major_formatter(lambda x, pos: str(round(x / 12, 0)))

            # set the y-axis limit for Indonesia
            if country_name == "Indonesia" and "Resilient" in scenario_label:
                ylim_constraint = 3020
            else:
                ylim_constraint = 100000

            # add the plots to the subplots
            if i in figure_a_indices or i in figure_b_indices:
                if row_index == 4:
                    add_xlabel = True
                else:
                    add_xlabel = False
                ax, legend, pal = Plotter.helper_for_plotting_fig_2abcde(
                    ax,
                    interpreter,
                    xlim,
                    "Needs met: " + str(people_fed) + "%",
                    add_ylabel,
                    add_xlabel,
                    ylim_constraint=ylim_constraint,
                )
                # xticks = ax.get_xticks()
                ax = fig.add_subplot(gs[row_index + 1, 2])
                # ax.set_xticklabels(xticks, rotation=0, fontsize=9)
                # ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
                # ax.xaxis.set_major_formatter(lambda x, pos: str(round(x / 12, 0)))

        # add the legend subplot
        ax.axis("off")
        ax = fig.add_subplot(gs[6, :])
        legend_elements = []
        for i in range(len(legend)):
            # flip order
            flipped_i = len(legend) - i - 1
            adjusted_legend = legend[flipped_i].replace("\n", " ")
            legend_elements.append(
                Line2D([0], [0], color=pal[flipped_i], label=adjusted_legend)
            )
            # legend_elements.append(PolyCollection([0], [0], color=pal[i], label=legend[i]))

        # legend_dict = dict(linewidth=3)

        leg = ax.legend(
            handles=legend_elements,
            loc="center",
            ncol=1,
            bbox_to_anchor=(0.5, 0.5),
            framealpha=0,
        )

        for legobj in leg.legendHandles:
            legobj.set_linewidth(5.0)

        # leg.get_frame().set_alpha(None)
        # leg.get_frame().set_facecolor(None)

        # ax.legend(bbox_to_anchor=(1, 1))
        # for i in r
        # leg.get_lines()[0].set_linewidth(6)
        # for i in range(1, 4):
        # line = plt.plot(i * np.arange(1, 10))[0]
        # ax.plot(-i * np.arange(1, 10), ls="--", color=line.get_color())

        # save the figure
        ax.axis("off")
        plt.savefig(
            Path(repo_root) / "results" / "fig_2abcde.png",
            dpi=300,
            facecolor=fig.get_facecolor(),
            transparent=False,
            edgecolor="none",
        )

        plt.tight_layout()
        # fig.set_dpi(300.0)
        plt.show()

    def plot_fig_2abcd(interpreter1, interpreter2, xlim):
        legend = Plotter.get_people_fed_legend(interpreter1, True)
        fig = plt.figure()
        pal = [
            "#1e7ecd",
            "#71797E",
            "#e75480",
            "#76d7ea",
            "#056608",
            "#f3f4e3",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        for i, label in enumerate(("a", "b", "c", "d")):
            if label == "a":
                interpreter = interpreter1
            if label == "b":
                interpreter = interpreter1
            if label == "c":
                interpreter = interpreter2
            if label == "d":
                interpreter = interpreter2
            ax = fig.add_subplot(2, 2, i + 1)
            ax.set_xlim([0.5, xlim])
            if label == "a":
                plt.title("Food availability")
            if label == "b":
                plt.title("Available food macronutrition")
            if label == "c":
                plt.title("Diet composition")
            if label == "d":
                plt.title("Diet macronutrition")
            if label == "a" or label == "c":
                ykcals = []
                ykcals.append(interpreter.fish_kcals_equivalent.kcals)
                ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
                ykcals.append(interpreter.scp_kcals_equivalent.kcals)
                ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
                ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
                ykcals.append(
                    (
                        interpreter.grazing_milk_kcals_equivalent.kcals
                        + interpreter.grain_fed_milk_kcals_equivalent.kcals
                    )
                )
                ykcals.append(
                    (
                        interpreter.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                        + interpreter.grain_fed_meat_kcals_equivalent.kcals
                    )
                )
                ykcals.append(
                    interpreter.immediate_outdoor_crops_kcals_equivalent.kcals
                )
                ykcals.append(
                    interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals
                )
                ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )
                ax.stackplot(
                    interpreter.time_months_middle,
                    np.array(ykcals),
                    labels=legend,
                    colors=pal,
                )

                # get the sum of all the ydata up to xlim month,
                # then find max month
                maxy = max(sum([x[0:xlim] for x in ykcals]))
                ax.set_ylim([0, maxy])

                plt.ylabel("Kcals / capita / day")
            if label == "b" or label == "d":
                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )
                plt.xlabel("Months since May nuclear winter onset")

                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.kcals_fed,
                    color="blue",
                    linestyle="solid",
                )

                if interpreter.include_fat:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.fat_fed,
                        color="green",
                        linestyle="dashed",
                    )

                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.protein_fed,
                        color="red",
                        linestyle="dotted",
                    )

                ax.set_ylabel("Percent of minimum recommendation")
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            if label == "c":
                # ax.legend(loc='center left', frameon=False,bbox_to_anchor=(0, -0.2), shadow=False,)
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                plt.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.5),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels),
                )

            if label == "d":
                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=["Calories", "Fat", "Protein"],
                )
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            plt.xlabel("Months since May nuclear winter onset")

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig(Path(repo_root) / "results" / "fig_2abcd.png")
        print("saved figure 2abcd")
        plt.show()

    def plot_fig_3abcde_updated(results, xlim):
        """
        Plots a figure with 5 subplots, each containing a map and text. The maps show the
        distribution of people in a given scenario, and the text shows the percentage of
        people fed in that scenario.

        Args:
            results (dict): A dictionary containing the results of the simulation for each
            scenario.
            xlim (tuple): A tuple containing the minimum and maximum x-axis values for the
            plots.

        Returns:
            None

        Example:
            >>>
            >>> plot_fig_3abcde_updated(results, xlim)

        """
        # Create a list of lists containing the percentage of people fed, the interpreter
        # object, and the scenario name for each scenario in the results dictionary.
        lists_of_lists = []
        for scenario_name, interpreter in results.items():
            print(scenario_name)
            print(interpreter.percent_people_fed)
            lists_of_lists.append(
                [interpreter.percent_people_fed, interpreter, scenario_name]
            )

        # Create a figure with 5 subplots arranged in a 5x3 grid.
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(
            5,
            3,
            wspace=0.4,
            hspace=0.5,
            width_ratios=[1, 2, 2],
            height_ratios=[0.125, 2, 2, 2, 3],
            left=0.02,
            right=0.98,
            top=0.98,
            bottom=0.02,
        )

        # Add two empty subplots to the top row of the grid.
        ax = fig.add_subplot(gs[0, 1])
        ax.axis("off")
        ax = fig.add_subplot(gs[0, 2])
        ax.axis("off")

        # Loop through the first three scenarios in the list of lists and create a subplot
        # for each one.
        for i in range(3):
            [
                percent_people_fed,
                interpreter,
                scenario_name,
            ] = lists_of_lists[i]
            row = i + 1
            if row == 1:
                max_y_percent = 300
            else:
                max_y_percent = -1
            gs, fig = Plotter.helper_for_plotting_fig_3abcde(
                interpreter, xlim, gs, row, fig, max_y_percent
            )
            ax = fig.add_subplot(gs[row, 0])
            percent_fed = str(int(percent_people_fed))
            labels = {1: "a", 2: "b", 3: "c"}

            # Add a label to the top left corner of the subplot indicating which scenario
            # it represents.
            ax.text(
                0.5,
                1.1,
                labels[row],
                transform=ax.transAxes,
                fontsize=11,
                fontweight="bold",
                va="top",
                ha="right",
            )

            # Add a text box to the center of the subplot containing the scenario name and
            # the percentage of people fed.
            ax.text(
                0.5,
                0.5,
                scenario_name + "\n\nNeeds met: " + percent_fed + "%",
                fontweight="bold",
                bbox={
                    "facecolor": "white",
                    "alpha": 1,
                    "edgecolor": "none",
                    "pad": 1,
                },
                fontsize=10,
                ha="center",
                va="center",
            )

            ax.axis("off")

        # Save the figure as a PNG file and display it.
        plt.savefig(
            Path(repo_root) / "results" / "fig_3abc.png",
            dpi=300,
            facecolor=fig.get_facecolor(),
            transparent=False,
            edgecolor="none",
        )
        plt.show()

    def plot_fig_3ab(monte_carlo_data, food_names, removed, added):
        # fig = plt.figure()
        fig = plt.figure(figsize=(10, 10))
        gs = gridspec.GridSpec(4, 2, wspace=0.3)
        print("95% lower")
        print(np.percentile(np.array(monte_carlo_data), 2.5))
        print("95% upper")
        print(np.percentile(np.array(monte_carlo_data), 97.5))
        for i, label in enumerate(("a", "b")):
            if label == "a":
                ax3 = fig.add_subplot(gs[0:3, 0])
                ax3.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax3.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )
                ax3.spines["top"].set_visible(False)
                ax3.spines["right"].set_visible(False)
                ax4 = fig.add_subplot(gs[3, 0])
                # ax4.axis("off")
                ax4.spines["top"].set_visible(False)
                ax4.spines["bottom"].set_visible(False)
                ax4.spines["right"].set_visible(False)
                ax4.spines["left"].set_visible(False)

            if label == "b":
                # ax_box = fig.add_subplot(gs[0, 1])
                # ax_box.text(-0.06, 1.35, label, transform=ax_box.transAxes,
                ax_hist = fig.add_subplot(gs[0:3, 1])
                ax_hist.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax_hist.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )
                # ax_box.axis("off")

            if label == "a":
                dict = {}
                dict["category"] = []
                dict["food"] = []
                dict["calories"] = []
                for i in range(0, len(food_names)):
                    f = food_names[i]
                    food_removed = removed[f]
                    dict["category"] = np.append(
                        dict["category"],
                        ["loss of calories if removed"] * len(food_removed),
                    )
                    dict["food"] = np.append(dict["food"], [f] * len(food_removed))
                    dict["calories"] = np.append(dict["calories"], removed[f])
                    food_added = added[f]
                    dict["category"] = np.append(
                        dict["category"],
                        ["additional calories if included"] * len(food_added),
                    )
                    dict["food"] = np.append(dict["food"], [f] * len(food_added))
                    dict["calories"] = np.append(dict["calories"], added[f])
                df = pd.DataFrame.from_dict(dict)
                sns.boxplot(
                    data=df,
                    x="calories",
                    y="food",
                    hue="category",
                    ax=ax3,
                    showfliers=False,
                    palette=sns.color_palette(["#ff0000", "#00ff00"]),
                )
                ax3.get_legend().remove()
                ax3.set(title="Comparative evaluation")
                plt.legend(
                    bbox_to_anchor=(0.0, -0.1),
                )
                ax3.set(xlabel="change in caloric availability (Kcals / person / day)")
                plt.ylabel("")
                handles, labels = ax3.get_legend_handles_labels()
                ax4.legend(handles, labels, frameon=False, bbox_to_anchor=(0.8, 0.8))
                ax4.axis("off")
            if label == "b":
                sns.histplot(data=monte_carlo_data, ax=ax_hist)
                ax_hist.set(xlabel="mean caloric availability (Kcals / person / day)")
                ax_hist.set(title="Monte Carlo outcomes")

        plt.tight_layout()
        plt.savefig(Path(repo_root) / "results" / "fig_3ab.png")
        print("saved figure 3ab")
        plt.show()

    def plot_fig_s2abcd(interpreter1, interpreter2, xlim1, xlim2):
        """
        Plots a figure with four subplots, each showing different food availability and macronutrition scenarios.
        Args:
            interpreter1 (Interpreter): an instance of the Interpreter class representing the first scenario
            interpreter2 (Interpreter): an instance of the Interpreter class representing the second scenario
            xlim1 (int): the limit for the x-axis for the first and second subplots
            xlim2 (int): the limit for the x-axis for the third and fourth subplots
        Returns:
            None
        """
        # Get the legend for the plot
        legend = Plotter.get_people_fed_legend(interpreter1, True)

        # Create a new figure
        fig = plt.figure()

        # Define a color palette for the plot
        pal = [
            "#1e7ecd",
            "#71797E",
            "#e75480",
            "#76d7ea",
            "#056608",
            "#f3f4e3",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        # Iterate over the four subplots
        for i, label in enumerate(("a", "b", "c", "d")):
            # Set the interpreter based on the label
            if label == "a":
                interpreter = interpreter1
            if label == "b":
                interpreter = interpreter1
            if label == "c":
                interpreter = interpreter2
            if label == "d":
                interpreter = interpreter2

            # Add a new subplot to the figure
            ax = fig.add_subplot(2, 2, i + 1)

            # Set the title and x-axis limit based on the label
            if label == "a":
                xlim = xlim1
                plt.title("Resilient food availability")
            if label == "b":
                xlim = xlim1
                plt.title("Resilient food macronutrition")
            if label == "c":
                xlim = xlim2
                plt.title("No resilient food availability")
            if label == "d":
                xlim = xlim2
                plt.title("No resilient food macronutrition")

            # Set the x-axis limit for the subplot
            ax.set_xlim([0.5, xlim])

            # Plot the stackplot for subplots a and c
            if label == "a" or label == "c":
                # Get the kcals for each food source
                ykcals = []
                ykcals.append(interpreter.fish_kcals_equivalent.kcals)
                ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
                ykcals.append(interpreter.scp_kcals_equivalent.kcals)
                ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
                ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
                ykcals.append(
                    (
                        interpreter.grazing_milk_kcals_equivalent.kcals
                        + interpreter.grain_fed_milk_kcals_equivalent.kcals
                    )
                )
                ykcals.append(
                    (
                        interpreter.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                        + interpreter.grain_fed_meat_kcals_equivalent.kcals
                    )
                )
                ykcals.append(
                    interpreter.immediate_outdoor_crops_kcals_equivalent.kcals
                )
                ykcals.append(
                    interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals
                )
                ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

                # Add the label to the subplot
                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )

                # Plot the stackplot
                ax.stackplot(
                    interpreter.time_months_middle,
                    np.array(ykcals),
                    labels=legend,
                    colors=pal,
                )

                plt.ylabel("Kcals / capita / day")

            # Plot the line plot for subplots b and d
            if label == "b" or label == "d":
                # Add the label to the subplot
                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )

                # Set the x-axis label
                plt.xlabel("Months since May nuclear winter onset")

                # Plot the line plot for kcals fed
                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.kcals_fed,
                    color="blue",
                    linestyle="solid",
                )

                # Plot the line plot for fat fed if include_fat is True
                if interpreter.include_fat:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.fat_fed,
                        color="green",
                        linestyle="dashed",
                    )

                # Plot the line plot for protein fed if include_protein is True
                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.protein_fed,
                        color="red",
                        linestyle="dotted",
                    )

                # Set the y-axis label and limit
                ax.set_ylabel("Percent of minimum recommendation")
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            # Add the legend to subplot c
            if label == "c":
                # Get the handles
                handles, labels = ax.get_legend_handles_labels()

                # Reverse the handles and labels
                plt.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.5),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels),
                )

            # Add the legend to subplot d
            if label == "d":
                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=["Calories", "Fat", "Protein"],
                )
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            # Set the y-axis limit for subplots a and c
            if label == "a":
                maxy = max(sum([x[0:xlim1] for x in ykcals]))
                ax.set_ylim([0, maxy])
            if label == "c":
                maxy = max(sum([x[0:xlim2] for x in ykcals]))
                ax.set_ylim([0, maxy])

            # Set the x-axis label for subplots a and c
            plt.xlabel("Months since May ASRS")

        # Set the figure size and layout
        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()

        # Save the figure and display it
        plt.savefig(Path(repo_root) / "results" / "fig_s2abcd.png")
        print("saved figure s2abcd")
        plt.show()

    @classmethod
    def plot_fig_s1abcd(crs, interpreter1, interpreter2, xlim, showplot=False):
        """
        Plots four subplots of food availability and macronutrition before and after ASRS.
        Args:
            crs (object): CRS object
            interpreter1 (object): Interpreter object for before ASRS
            interpreter2 (object): Interpreter object for after ASRS
            xlim (int): The maximum limit for the x-axis
            showplot (bool): Whether to show the plot or not. Default is False.
        Returns:
            None
        """
        # Get the legend for the stackplot
        legend = Plotter.get_people_fed_legend(interpreter1, False)
        # Create a new figure
        fig = plt.figure()
        # Define a color palette
        pal = [
            "#1e7ecd",
            "#71797E",
            "#e75480",
            "#76d7ea",
            "#056608",
            "#f3f4e3",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        # Iterate over the four subplots
        for i, label in enumerate(("a", "b", "c", "d")):
            # Set the interpreter based on the label
            if label == "a":
                interpreter = interpreter1
            if label == "b":
                interpreter = interpreter1
            if label == "c":
                interpreter = interpreter2
            if label == "d":
                interpreter = interpreter2
            # Add a new subplot to the figure
            ax = fig.add_subplot(2, 2, i + 1)
            # Set the x-axis limit
            ax.set_xlim([0.5, xlim])
            # Set the title based on the label
            if label == "a":
                plt.title("Food availability before ASRS")
            if label == "b":
                plt.title("Available food macronutrition")
            if label == "c":
                plt.title("Diet composition")
            if label == "d":
                plt.title("Diet macronutrition")
            # Set the y-axis limit and label for subplots a and c
            if label == "a" or label == "c":
                # Get the kcals for each food source
                ykcals = []
                ykcals.append(interpreter.fish_kcals_equivalent.kcals)
                ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
                ykcals.append(interpreter.scp_kcals_equivalent.kcals)
                ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
                ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
                ykcals.append(
                    (
                        interpreter.grazing_milk_kcals_equivalent.kcals
                        + interpreter.grain_fed_milk_kcals_equivalent.kcals
                    )
                )
                ykcals.append(
                    (
                        interpreter.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                        + interpreter.grain_fed_meat_kcals_equivalent.kcals
                    )
                )
                ykcals.append(
                    interpreter.immediate_outdoor_crops_kcals_equivalent.kcals
                )
                ykcals.append(
                    interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals
                )
                ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)
                # Add the label to the top left corner of the subplot
                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )
                # Create a stackplot of the kcals for each food source
                ax.stackplot(
                    interpreter.time_months_middle,
                    np.array(ykcals),
                    labels=legend,
                    colors=pal,
                )
                # Set the y-axis label
                plt.ylabel("Kcals / capita / day")
            # Set the y-axis limit and label for subplots b and d
            if label == "b" or label == "d":
                # Add the label to the top left corner of the subplot
                ax.text(
                    -0.06,
                    1.1,
                    label,
                    transform=ax.transAxes,
                    fontsize=11,
                    fontweight="bold",
                    va="top",
                    ha="right",
                )
                # Set the x-axis label
                plt.xlabel("Months since May nuclear winter onset")
                # Plot the kcals fed
                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.kcals_fed,
                    color="blue",
                    linestyle="solid",
                )
                # Plot the fat fed if included
                if interpreter.include_fat:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.fat_fed,
                        color="green",
                        linestyle="dashed",
                    )
                # Plot the protein fed if included
                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.protein_fed,
                        color="red",
                        linestyle="dotted",
                    )
                # Set the y-axis label
                ax.set_ylabel("Percent of minimum recommendation")
                # Set the y-axis limit
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))
            # Set the legend for subplot c
            if label == "c":
                # Get the handles and labels for the legend
                handles, labels = ax.get_legend_handles_labels()
                # Reverse the order of the handles and labels
                plt.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.4),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels),
                )
            # Set the legend for subplot d
            if label == "d":
                # Set the legend for the subplot
                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=["Calories", "Fat", "Protein"],
                )
                # Set the y-axis limit
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))
            # Set the x-axis label for all subplots
            plt.xlabel("Months since May")
        # Set the figure height and width
        fig.set_figheight(8)
        fig.set_figwidth(10)
        # Set the padding between subplots
        plt.tight_layout(w_pad=1, h_pad=1)
        # Save or show the plot
        saveloc = Path(repo_root) / "results" / "fig_s1abcd.png"
        plt.savefig(
            saveloc,
            dpi=300,
        )
        print("saved figure s1abcd")
        if showplot:
            plt.show()

    def getylim_nutrients(interpreter, xlim):
        """
        Calculates the minimum and maximum values for the y-axis of a plot of nutrient data.

        Args:
            interpreter (Interpreter): An instance of the Interpreter class containing nutrient data.
            xlim (int): The maximum x-axis value for the plot.

        Returns:
            list: A list containing the minimum and maximum values for the y-axis of the plot.

        Example:
            >>> interpreter = Interpreter()
            >>> interpreter.include_fat = True
            >>> interpreter.include_protein = True
            >>> interpreter.kcals_fed = [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]
            >>> interpreter.fat_fed = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
            >>> interpreter.protein_fed = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
            >>> getylim_nutrients(interpreter, 5)
            [80, 320]
        """
        kcals = interpreter.kcals_fed

        if interpreter.include_fat:
            fat = interpreter.fat_fed
        else:
            fat = interpreter.kcals_fed

        if interpreter.include_protein:
            protein = interpreter.protein_fed
        else:
            protein = interpreter.kcals_fed

        # Calculate the minimum and maximum values for the y-axis of the plot
        min_plot = (
            min([min(fat[0:xlim]), min(protein[0:xlim]), min(kcals[0:xlim])]) - 20
        )

        max_plot = (
            max([max(fat[0:xlim]), max(protein[0:xlim]), max(kcals[0:xlim])]) + 20
        )

        return [min_plot, max_plot]

    def plot_histogram(ax, data, N, xlabel, ylabel, title):
        """
        Plots a histogram of the given data on the given axis with the given labels and title.

        Args:
            ax (matplotlib.axes.Axes): The axis to plot the histogram on.
            data (list): The data to plot.
            N (int): The number of data points.
            xlabel (str): The label for the x-axis.
            ylabel (str): The label for the y-axis.
            title (str): The title for the plot.

        Returns:
            None

        Example:
            >>> fig, ax = plt.subplots()
            >>> data = [1, 2, 3, 4, 5]
            >>> N = 5
            >>> xlabel = "X Label"
            >>> ylabel = "Y Label"
            >>> title = "Title"
            >>> plot_histogram(ax, data, N, xlabel, ylabel, title)
        """
        num_bins = int(N / 10)  # Calculate the number of bins for the histogram
        ax.hist(data, bins=num_bins, facecolor="blue", alpha=0.5)  # Plot the histogram
        ax.set_xlabel(xlabel)  # Set the x-axis label
        ax.set_ylabel(ylabel)  # Set the y-axis label
        ax.set_title(title)  # Set the plot title
        # ax.set_ylabel()

    def plot_histogram_with_boxplot(data, xlabel, title):
        """
        This function plots a histogram with a boxplot on top of it using seaborn library.
        It also prints the 95% lower and upper bounds of the data.

        Args:
            data (list): A list of numerical data to be plotted.
            xlabel (str): The label for the x-axis of the histogram.
            title (str): The title of the plot.

        Returns:
            None

        Example:
            >>> data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            >>> xlabel = "Values"
            >>> title = "Histogram with Boxplot"
            >>> plot_histogram_with_boxplot(data, xlabel, title)
        """

        # set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
        sns.set(style="darkgrid")

        # creating a figure composed of two matplotlib.Axes objects (ax_box and ax_hist)
        f, (ax_box, ax_hist) = plt.subplots(
            2, sharex=True, gridspec_kw={"height_ratios": (0.15, 0.85)}
        )

        # assigning a graph to each ax
        sns.boxplot(data, ax=ax_box, showfliers=True)
        sns.histplot(data=data, ax=ax_hist)

        # Remove x axis name for the boxplot
        ax_hist.set(xlabel=xlabel)
        ax_box.set(title=title)
        plt.show()

        # Print the 95% lower and upper bounds of the data
        print("95% lower")
        print(np.percentile(np.array(data), 2.5))
        print("95% upper")
        print(np.percentile(np.array(data), 97.5))

    def get_people_fed_legend(interpreter, is_nuclear_winter):
        """
        Returns a list of strings representing the legend for the plot of the amount of people fed
        Args:
            interpreter (Interpreter): an instance of the Interpreter class
            is_nuclear_winter (bool): a boolean indicating whether the simulation includes a nuclear winter
        Returns:
            list: a list of strings representing the legend for the plot of the amount of people fed
        """
        # Set the labels for the stored food consumed before and after the simulation/nuclear winter
        if not is_nuclear_winter:
            stored_food_label = (
                "Crops consumed that month that were\nstored before simulation"
            )
            OG_stored_label = (
                "Crops consumed that month that were\nstored after simulation start"
            )
        else:
            stored_food_label = "Crops consumed that month that were\nstored before nuclear winter onset"
            OG_stored_label = (
                "Crops consumed that month that were\nstored after nuclear winter onset"
            )

        # Create a list of strings representing the legend for the plot of the amount of people fed
        legend = []

        # Add the legend for marine fish if ADD_FISH is True, otherwise add an empty string
        if interpreter.constants["ADD_FISH"]:
            legend = legend + ["Marine Fish"]
        else:
            legend = legend + [""]

        # Add the legend for cellulose sugar if ADD_CELLULOSIC_SUGAR is True, otherwise add an empty string
        if interpreter.constants["ADD_CELLULOSIC_SUGAR"]:
            legend = legend + ["Cellulosic Sugar"]
        else:
            legend = legend + [""]

        # Add the legend for methane SCP if ADD_METHANE_SCP is True, otherwise add an empty string
        if interpreter.constants["ADD_METHANE_SCP"]:
            legend = legend + ["Methane SCP"]
        else:
            legend = legend + [""]

        # Add the legend for greenhouses if ADD_GREENHOUSES is True, otherwise add an empty string
        if interpreter.constants["ADD_GREENHOUSES"]:
            legend = legend + ["Greenhouses"]
        else:
            legend = legend + [""]

        # Add the legend for seaweed if ADD_SEAWEED is True, otherwise add an empty string
        if interpreter.constants["ADD_SEAWEED"]:
            legend = legend + ["Seaweed"]
        else:
            legend = legend + [""]

        # Add the legend for dairy milk if ADD_MILK is True, otherwise add an empty string
        if interpreter.constants["ADD_MILK"]:
            legend = legend + ["Dairy Milk"]
        else:
            legend = legend + [""]

        # Add the legend for meat if ADD_CULLED_MEAT or ADD_MAINTAINED_MEAT is True, otherwise add an empty string
        if (
            interpreter.constants["ADD_CULLED_MEAT"]
            or interpreter.constants["ADD_MAINTAINED_MEAT"]
        ):
            legend = legend + ["Meat"]
        else:
            legend = legend + [""]

        # Add the legend for outdoor crops consumed immediately if
        # ADD_OUTDOOR_GROWING is True, otherwise add an empty string
        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + ["Outdoor Crops consumed immediately"]
        else:
            legend = legend + [""]

        # Add the legend for crops consumed after simulation/nuclear winter onset
        # if ADD_OUTDOOR_GROWING is True, otherwise add an empty string
        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + [OG_stored_label]
        else:
            legend = legend + [""]

        # Add the legend for stored food consumed before simulation/nuclear winter
        # onset if ADD_STORED_FOOD is True, otherwise add an empty string
        if interpreter.constants["ADD_STORED_FOOD"]:
            legend = legend + [stored_food_label]
        else:
            legend = legend + [""]

        return legend

    def get_feed_biofuels_legend(interpreter):
        """
        Returns a list of strings representing the legend for the feed and biofuels in the simulation.

        Args:
            interpreter (Interpreter): An instance of the Interpreter class.

        Returns:
            list: A list of strings representing the legend for the feed and biofuels in the simulation.

        Example:
            >>> interpreter = Interpreter()
            >>> get_feed_biofuels_legend(interpreter)
            ['Cellulosic Sugar Feed', '', 'Seaweed Feed', 'Outdoor Crops consumed Feed', 'Stored food, either from before or after catastrophe Feed', 'Cellulosic Sugar Feed', 'Methane SCP Biofuels', 'Seaweed Biofuels', 'Outdoor Crops consumed Biofuels', 'Stored food, either from before or after catastrophe Biofuels']
        """
        # Define the label for stored food
        stored_food_label = "Stored food, either from before or after catastrophe"

        # Initialize the legend list
        legend = []

        # Check if cellulosic sugar feed is added
        if interpreter.constants["ADD_CELLULOSIC_SUGAR"]:
            legend = legend + ["Cellulosic Sugar Feed"]
        else:
            legend = legend + [""]

        # Check if methane SCP feed is added
        if interpreter.constants["ADD_METHANE_SCP"]:
            legend = legend + ["Methane SCP Feed"]
        else:
            legend = legend + [""]

        # Check if seaweed feed is added
        if interpreter.constants["ADD_SEAWEED"]:
            legend = legend + ["Seaweed Feed"]
        else:
            legend = legend + [""]

        # Check if outdoor growing is added
        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + ["Outdoor Crops consumed Feed"]
        else:
            legend = legend + [""]

        # Check if stored food is added
        if interpreter.constants["ADD_STORED_FOOD"]:
            legend = legend + [stored_food_label + " Feed"]
        else:
            legend = legend + [""]

        # Check if cellulosic sugar biofuels is added
        if interpreter.constants["ADD_CELLULOSIC_SUGAR"]:
            legend = legend + ["Cellulosic Sugar Feed"]
        else:
            legend = legend + [""]

        # Check if methane SCP biofuels is added
        if interpreter.constants["ADD_METHANE_SCP"]:
            legend = legend + ["Methane SCP Biofuels"]
        else:
            legend = legend + [""]

        # Check if seaweed biofuels is added
        if interpreter.constants["ADD_SEAWEED"]:
            legend = legend + ["Seaweed Biofuels"]
        else:
            legend = legend + [""]

        # Check if outdoor growing biofuels is added
        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + ["Outdoor Crops consumed Biofuels"]
        else:
            legend = legend + [""]

        # Check if stored food biofuels is added
        if interpreter.constants["ADD_STORED_FOOD"]:
            legend = legend + [stored_food_label + " Biofuels"]
        else:
            legend = legend + [""]

        # Return the legend list
        return legend

    def plot_monthly_reductions_seasonally(ratios):
        """
        Plots the fraction of crop production per month, including seasonality.

        Args:
            ratios (list): A list of ratios to baseline production.

        Returns:
            None

        Example:
            >>> ratios = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.1, 1.0, 0.9, 0.8]
            >>> plot_monthly_reductions_seasonally(ratios)
        """
        # Create a list of month numbers
        month_nums = np.linspace(0, len(ratios), len(ratios))

        # Plot the ratios as a scatter plot
        plt.scatter(month_nums, ratios)

        # Plot the ratios as a line plot
        plt.plot(month_nums, ratios)

        # Set the x-axis label
        plt.xlabel("month")

        # Set the y-axis label
        plt.ylabel("ratios to baseline production")

        # Set the plot title
        plt.title("fraction of crop production per month, including seasonality")

        # Show the plot
        plt.show()

    def plot_monthly_reductions_no_seasonality(all_months_reductions):
        """
        Plot the reduction each month, showing the seasonal variability.

        Args:
            all_months_reductions (list): A list of floats representing the reduction in crop production for each month.

        Returns:
            None

        Example:
            >>> all_months_reductions = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.5]
            >>> plot_monthly_reductions_no_seasonality(all_months_reductions)
        """
        # Create an array of month numbers
        month_nums = np.linspace(
            0, len(all_months_reductions), len(all_months_reductions)
        )

        # Plot the reduction for each month
        plt.scatter(month_nums, all_months_reductions)

        # Set the title, x-axis label, and y-axis label
        plt.title("fraction of crop production per month, not including seasonality")
        plt.xlabel("month")
        plt.ylabel("ratio to baseline production")

        # Show the plot
        plt.show()

    def plot_food(food, title):
        """
        Plot the food generically with the 3 macronutrients.

        Args:
            food (Food): An instance of the Food class containing the macronutrient data to be plotted.
            title (str): The title of the plot.

        Returns:
            pathlib.Path: The path to the saved plot.

        Example:
            >>> food = Food(kcals=[100, 200, 300], kcals_units="kcal each month", fat=[10, 20, 30], fat_units="g each month", protein=[5, 10, 15], protein_units="g each month")
            >>> plot_food(food, "Monthly Macronutrient Intake")
        """

        # Ensure that food is a list
        food.make_sure_is_a_list()

        # Extract the macronutrient data from the Food instance
        vals1 = food.kcals
        title1 = food.kcals_units
        vals2 = food.fat
        title2 = food.fat_units
        vals3 = food.protein
        title3 = food.protein_units

        # Placing the plots in the plane
        fig, ax = plt.subplots(2, 2)
        plt.rc("font", size=10)  # controls default text size
        plot1 = plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan=2)
        plot2 = plt.subplot2grid((2, 2), (0, 1))
        plot3 = plt.subplot2grid((2, 2), (1, 1))

        # Using Numpy to create an array x
        x = np.arange(len(vals1))

        # Plot for vals1
        plot1.plot(x, vals1)
        plot1.set_ylabel(title1.split(" each month")[0], fontsize=6)
        plot1.set_xlabel("month", fontsize=6)
        plot1.set_title("kcals: " + title1, fontsize=6)

        # Plot for  vals2
        plot2.plot(x, vals2)
        plot2.set_ylabel(title2.split(" each month")[0], fontsize=6)
        plot2.set_xlabel("month", fontsize=6)
        plot2.set_title("fat: " + title2, fontsize=6)

        # Plot for vals3
        plot3.plot(x, vals3)
        plot3.set_ylabel(title3.split(" each month")[0], fontsize=6)
        plot3.set_xlabel("month", fontsize=6)
        plot3.set_title("protein: " + title3, fontsize=6)

        # Packing all the plots and displaying them
        plt.tight_layout()
        fig.suptitle(title)

        # Save the plot to a file
        saveloc = Path(repo_root) / "results" / "large_reports" / (title + ".png")
        plt.savefig(saveloc, dpi=300)

        # Show the plot if SHOWPLOT is True
        SHOWPLOT = True
        if SHOWPLOT:
            plt.show()
        # else:
        # plt.close()

        # Return the path to the saved plot
        return saveloc

    def plot_food_alternative(food, title):
        """
        Plot the food generically with the 3 macronutrients (alternative layout).
        Args:
            food (Food): An instance of the Food class containing the macronutrient data to be plotted.
            title (str): The title of the plot.
        Returns:
            pathlib.Path: The path to the saved plot.
        """
        # Ensure that food is a list
        food.make_sure_is_a_list()

        # Extract the macronutrient data from the food object
        vals1 = food.kcals
        title1 = food.kcals_units
        vals2 = food.fat
        title2 = food.fat_units
        vals3 = food.protein
        title3 = food.protein_units

        # Placing the plots in the plane
        fig, ax = plt.subplots(3, 1)
        plt.rc("font", size=10)  # controls default text size
        plot1 = plt.subplot2grid((3, 1), (0, 0))
        plot2 = plt.subplot2grid((3, 1), (1, 0))
        plot3 = plt.subplot2grid((3, 1), (2, 0))

        # Using Numpy to create an array x
        x = np.arange(len(vals1))

        # Plot for vals1
        plot1.plot(x, vals1)
        plot1.set_ylabel(title1.split(" each month")[0], fontsize=6)
        plot1.set_xlabel("month", fontsize=6)
        plot1.set_title("kcals: " + title1, fontsize=6)

        # Plot for  vals2
        plot2.plot(x, vals2)
        plot2.set_ylabel(title2.split(" each month")[0], fontsize=6)
        plot2.set_xlabel("month", fontsize=6)
        plot2.set_title("fat: " + title2, fontsize=6)

        # Plot for vals3
        plot3.plot(x, vals3)
        plot3.set_ylabel(title3.split(" each month")[0], fontsize=6)
        plot3.set_xlabel("month", fontsize=6)
        plot3.set_title("protein: " + title3, fontsize=6)

        # Packing all the plots and displaying them
        plt.tight_layout()
        fig.suptitle(title)

        # Define the location to save the plot
        saveloc = Path(repo_root) / "results" / "large_reports" / "" + title + ".png"

        # Save the plot
        plt.savefig(
            saveloc,
            dpi=300,
        )

        # Display the plot if SHOWPLOT is True
        SHOWPLOT = True
        if SHOWPLOT:
            plt.show()
        # else:
        # plt.close()

        # Return the path to the saved plot
        return saveloc

    @classmethod
    def plot_map_of_countries_fed(
        crs, world, ratio_fed, description, plot_map, create_slide
    ):
        """
        Plots a map of countries fed with a given ratio of minimum macronutritional needs with no trade.
        Saves the plot as a png file and displays it if plot_map is True.
        If create_slide is True, inserts a slide with the plot in a presentation.

        Args:
            crs (object): an object with a method to insert a slide in a presentation
            world (GeoDataFrame): a GeoDataFrame containing the world map
            ratio_fed (float): the ratio of minimum macronutritional needs with no trade
            description (str): the description of the slide to be inserted
            plot_map (bool): whether to display the plot or not
            create_slide (bool): whether to insert a slide or not

        Returns:
            None

        Example:
            >>>
            >>> plot_map_of_countries_fed(crs, world, 0.5, "Slide description", True, True)

        """
        # If neither plot_map nor create_slide is True, there is no point in doing anything
        if (not plot_map) and (not create_slide):
            return

        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Plot the world map boundaries
        world.boundary.plot(ax=ax, color="Black", linewidth=0.1)

        # Plot the world map with the needs_ratio column as the color map
        world.plot(
            ax=ax,
            column="needs_ratio",
            legend=True,
            cmap="viridis",
            legend_kwds={"label": "Fraction Fed", "orientation": "horizontal"},
        )

        # Create a string for the title of the plot
        save_title_string = (
            "Fraction of minimum macronutritional needs with no trade, ratio fed: "
            + str(ratio_fed)
        )

        # Save the plot as a png file
        path_string = str(
            Path(repo_root) / "results" / "large_reports" / "map_ratio_fed_"
        )
        saveloc = path_string + ratio_fed + ".png"
        fig.savefig(
            saveloc,
            dpi=300,
        )
        plt.tight_layout()

        # Display the plot if plot_map is True
        if plot_map:
            plt.show()

        # Insert a slide with the plot in a presentation if create_slide is True
        if create_slide:
            crs.mp.insert_slide(
                title_below=save_title_string,
                description=description,
                figure_save_loc=saveloc,
            )

    @classmethod
    def start_pptx(crs, title):
        """
        Initializes a PowerPoint presentation with a title slide.

        Args:
            crs (Course): An instance of the Course class.
            title (str): The title of the presentation.

        Returns:
            None.

        Example:
            >>> crs = Course()
            >>> start_pptx(crs, "My Presentation")
        """
        # Create an instance of the MakePowerpoint class
        mp = MakePowerpoint()

        # Create a title slide with the given title
        mp.create_title_slide(title)

        # Set the mp attribute of the Course instance to the created MakePowerpoint instance
        crs.mp = mp

    @classmethod
    def end_pptx(crs, saveloc):
        """
        Saves a PowerPoint file and creates a directory for it if it doesn't exist.
        Args:
            crs (class): an instance of the Plotter class
            saveloc (str): the path to save the PowerPoint file to
        Returns:
            None
        """
        # Check if the directory for large reports exists, if not, create it
        if not os.path.exists(Path(repo_root) / "results" / "large_reports"):
            os.mkdir(Path(repo_root) / "results" / "large_reports")
        # Save the PowerPoint file to the specified location
        crs.mp.save_ppt(saveloc)
