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
import re
import git

plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"

repo_root = git.Repo(".", search_parent_directories=True).working_dir

# in some linux win manager setups matplotlib plotting doesn't seem to play nice
# matplotlib.use('Svg')
# matplotlib.use('QtAgg')


font = {"family": "normal", "weight": "bold", "size": 7}

matplotlib.rc("font", **font)


class Plotter:
    def __init__(self):
        pass

    @classmethod
    def plot_to_humans_stackplot(
        crs,
        interpreter,
        xlim,
        newtitle="",
        plot_figure=True,
        add_slide_with_fig=True,
        description="",
        split_legend=True,
    ):
        if (not plot_figure) and (not add_slide_with_fig):
            return

        ADD_THE_NUTRITION_PLOT = interpreter.include_protein or interpreter.include_fat

        is_nuclear_winter = "baseline" not in newtitle.lower()

        legend = Plotter.get_people_fed_legend(interpreter, is_nuclear_winter)
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
        for i, label in enumerate(("a", "b")):
            if ADD_THE_NUTRITION_PLOT:
                ax = fig.add_subplot(1, 2, i + 1)
            else:
                if label == "b":
                    continue
                ax = fig.add_subplot(1, 1, 1)
            ykcals = []
            ykcals.append(interpreter.fish_kcals_equivalent.kcals)
            ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
            ykcals.append(interpreter.scp_kcals_equivalent.kcals)
            ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
            ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
            ykcals.append(interpreter.milk_kcals_equivalent.kcals)
            ykcals.append(interpreter.meat_kcals_equivalent.kcals)
            ykcals.append(interpreter.immediate_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

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
                ax.stackplot(
                    interpreter.time_months_middle,
                    np.array(ykcals),
                    labels=legend,
                    colors=pal,
                )
                if xlim == "earliest_month_zero":
                    xlim = interpreter.get_month_after_which_is_all_zero(
                        ykcals, interpreter.constants["NMONTHS"]
                    )

                ax.set_xlim([0.25, xlim])

                # get the sum of all the ydata up to xlim month,
                # then find max month
                # maxy = max(sum([x[0:xlim] for x in ykcals]))
                maxy = max([sum(x[0:xlim]) for x in ykcals])
                maxy = 0
                for i in range(xlim):
                    maxy = max(maxy, sum([x[i] for x in ykcals]))

                maxy += maxy / 20
                ax.set_ylim([0, maxy])
                # ax.set_ylim([0, maxy])

                plt.ylabel("Kcals / person / day", fontsize=11)
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
                if xlim == "earliest_month_zero":
                    xlim = interpreter.get_month_after_which_is_all_zero(
                        [interpreter.feed_and_biofuels.nonhuman_consumption],
                        interpreter.constants["NMONTHS"],
                    )
                ax.set_xlim([0.25, xlim])

                plt.xlabel("Months since May nuclear winter onset", fontsize=11)

                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.nonhuman_consumption.in_units_percent_fed().kcals,
                    color="blue",
                    linestyle="solid",
                )

                if interpreter.include_fat:
                    # 1 gram of fat is 9 kcals.
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.nonhuman_consumption.in_units_percent_fed().fat,
                        color="green",
                        linestyle="dashed",
                    )
                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.nonhuman_consumption.in_units_percent_fed().protein,
                        color="red",
                        linestyle="dotted",
                    )

                ax.set_ylabel("Percent of minimum recommendation")
                # ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            if label == "a":
                if ADD_THE_NUTRITION_PLOT:
                    legend_loc = (-0.15, -0.4)
                    print(
                        "the legend will not split when you add nutrition, you can change this easily"
                        "in plotter.py if you want"
                    )
                else:
                    if not split_legend:
                        legend_loc = (0, -0.2)

                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                if split_legend and not ADD_THE_NUTRITION_PLOT:
                    # Use ncol to specify the number of columns in the legend
                    ax.legend(
                        reversed(handles),
                        reversed(labels),
                        loc="lower center",
                        ncol=2,
                        bbox_to_anchor=(
                            0,
                            -0.25,
                            0.75,
                            0.75,
                        ),  # x0, y0, width, height (the y0 should be small negative)
                        mode="expand",  # Ensure the legend uses the full width set by bbox_to_anchor
                        borderaxespad=0.4,
                        frameon=False,
                        prop={"size": 8},
                        columnspacing=0.25,  # Adjust the space between columns as needed
                        handletextpad=0.5,  # Adjust the pad between the legend handle and text as needed
                    )

                    # Adjust the width of the legend - may need to adjust subplot params or legend size
                    fig.subplots_adjust(
                        bottom=0.2
                    )  # Adjust the bottom parameter to make room for the legend

                else:
                    plt.legend(
                        loc="center left",
                        frameon=False,
                        bbox_to_anchor=legend_loc,
                        shadow=False,
                        handles=reversed(handles),
                        labels=reversed(labels),
                    )

            if label == "b":
                labels = ["Calories"]
                if interpreter.include_fat:
                    labels += ("Fat",)
                if interpreter.include_protein:
                    labels += ("Protein",)

                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=labels,
                )

            if label == "a":
                if ADD_THE_NUTRITION_PLOT:
                    plt.title("Food availability", fontsize=11)
                else:
                    plt.title("Food availability, " + newtitle, fontsize=11)

            if label == "b":
                plt.title("Available food macronutrition", fontsize=11)

            plt.xlabel("Months since start of simulation", fontsize=11)

        # plt.rcParams["figure.figsize"] = [12.50, 10]

        fig.set_figheight(8)
        fig.set_figwidth(8)
        # plt.tight_layout()
        if ADD_THE_NUTRITION_PLOT:
            fig.suptitle(newtitle)

        path_string = str(Path(repo_root) / "results" / "large_reports" / "no_trade")
        newtitle_for_save = re.sub(r'[\\/*?:"<>|\n]', "_", newtitle)

        saveloc = path_string + newtitle_for_save + ".png"
        feed_saveloc = path_string + newtitle_for_save + "_feed.png"

        slaughter_saveloc = path_string + newtitle_for_save + "_slaughter.png"
        plt.savefig(
            # Replace problematic characters with an underscore or remove them
            saveloc,
            dpi=300,
        )
        if add_slide_with_fig:
            if os.path.isfile(feed_saveloc):
                crs.mp.insert_slide(
                    title_below="Feed and Biofuels "
                    + newtitle
                    + ": Percent fed:"
                    + str(round(interpreter.percent_people_fed, 1))
                    + "%",
                    description=description,
                    figure_save_loc=feed_saveloc,
                )

            if os.path.isfile(slaughter_saveloc):
                crs.mp.insert_slide(
                    title_below="Animal Slaughter "
                    + newtitle
                    + ": Percent fed:"
                    + str(round(interpreter.percent_people_fed, 1))
                    + "%",
                    description=description,
                    figure_save_loc=slaughter_saveloc,
                )

            crs.mp.insert_slide(
                title_below=newtitle
                + ": Percent fed:"
                + str(round(interpreter.percent_people_fed, 1))
                + "%",
                description=description,
                figure_save_loc=saveloc,
            )

        if plot_figure:
            plt.show()
        # else:
        plt.close()

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
        if (not plot_figure) and (not add_slide_with_fig):
            return

        ADD_THE_NUTRITION_PLOT = interpreter.include_protein or interpreter.include_fat

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
                if xlim == "earliest_month_zero":
                    xlim = interpreter.get_month_after_which_is_all_zero(
                        ykcals, interpreter.constants["NMONTHS"]
                    )
                ax.set_xlim([0.25, xlim])

                # get the sum of all the ydata up to xlim month,
                # then find max month
                # maxy = max(sum([x[0:xlim] for x in ykcals]))
                # maxy = max([sum(x[0:xlim]) for x in ykcals])
                maxy = max([sum(x[0:xlim]) for x in ykcals])

                maxy = 0
                for i in range(xlim):
                    maxy = max(maxy, sum([x[i] for x in ykcals]))

                maxy += maxy / 20
                ax.set_ylim([0, maxy])
                # ax.set_ylim([0, maxy])

                plt.ylabel("Kcals / person / day")
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
                    interpreter.feed_and_biofuels.nonhuman_consumption.in_units_percent_fed().kcals,
                    color="blue",
                    linestyle="solid",
                )

                if interpreter.include_fat:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.feed_and_biofuels.nonhuman_consumption.in_units_percent_fed().fat,
                        color="green",
                        linestyle="dashed",
                    )

                if interpreter.include_protein:
                    ax.plot(
                        interpreter.time_months_middle,
                        interpreter.feed_and_biofuels.nonhuman_consumption.in_units_percent_fed().protein,
                        color="red",
                        linestyle="dotted",
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
                labels = ["Calories"]
                if interpreter.include_fat:
                    labels += ("Fat",)
                if interpreter.include_protein:
                    labels += ("Protein",)

                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=labels,
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

        saveloc = path_string + re.sub(r'[\\/*?:"<>|\n]', "_", newtitle) + "_feed.png"
        plt.savefig(
            # Replace problematic characters with an underscore or remove them
            saveloc,
            dpi=300,
        )
        if plot_figure:
            plt.show()
        plt.close()

    @classmethod
    def plot_slaughter(
        crs,
        interpreter,
        xlim,
        newtitle="",
        plot_figure=True,
        add_slide_with_fig=True,
        description="",
    ):
        if (not plot_figure) and (not add_slide_with_fig):
            return

        fig = plt.figure()

        # Define a list of hatch patterns
        hatches = ["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]

        # Define a list of line styles
        line_styles = ["-", "--", "-.", ":"]

        # Define a list of marker styles
        markers = ["o", "s", "D", "^", "v", "<", ">", "p", "*", "+", "x"]

        for i, label in enumerate(("a", "b")):
            ax = fig.add_subplot(1, 2, i + 1)

            if label == "a":
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
                plt.ylabel("Kcals / person / day")
            if label == "b":
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

            if label == "a":
                # Plot for Meat production
                meat_list = []
                meat_labels = []
                for (
                    animal_label,
                    animal_meat,
                ) in interpreter.meat_dictionary.items():
                    meat_labels.append(animal_label)
                    meat_list.append(animal_meat)

                if xlim == "earliest_month_zero":
                    xlim = interpreter.get_month_after_which_is_all_zero(
                        meat_list, interpreter.constants["NMONTHS"]
                    )
                ax.set_xlim([0.25, xlim])
                # Use the hatches when calling stackplot
                stacks = ax.stackplot(
                    interpreter.time_months_middle,
                    meat_list,
                    labels=meat_labels,
                )
                # Apply hatches to each stack
                for stack, hatch in zip(stacks, hatches):
                    stack.set_hatch(hatch)
                ax.set_title("Meat Production and Animal populations over Simulation")
                ax.set_ylabel("Kcals per person per day of meat slaughtered each month")
                # Add legend and any other necessary plot formatting
                plt.title("Meat slaughtered over time")
                # Add a legend underneath this subplot
                ax.legend(
                    loc="upper center", bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=2
                )
            if label == "b":
                labels = []  # to collect labels for the legend
                line_objects = []

                if xlim == "earliest_month_zero":
                    xlim = interpreter.get_month_after_which_is_all_zero(
                        interpreter.animal_population_dictionary,
                        interpreter.constants["NMONTHS"],
                    )
                ax.set_xlim([0.25, xlim])

                for index, (
                    animal_label,
                    animal_population,
                ) in enumerate(interpreter.animal_population_dictionary.items()):
                    population_ratio = animal_population / animal_population[0]
                    ax.plot(interpreter.time_months_middle, population_ratio)
                    labels.append(animal_label)
                    line_style = line_styles[index % len(line_styles)]
                    marker = markers[index % len(markers)]
                    # Set the markevery parameter to a higher value to spread out the markers
                    markevery = 2  # Adjust this value as needed

                    (line,) = ax.plot(
                        interpreter.time_months_middle,
                        animal_population / animal_population[0],
                        line_style,
                        marker=marker,
                        markevery=markevery,
                        label=animal_label,
                    )
                    # (line,) = ax.plot(
                    #     interpreter.time_months_middle,
                    #     animal_population / animal_population[0],
                    #     line_style,
                    #     marker=marker,
                    #     label=animal_label,
                    # )
                    labels.append(animal_label)
                    line_objects.append(line)
                # Add a legend with custom handles
                ax.legend(
                    handles=line_objects,
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.15),
                    shadow=True,
                    ncol=2,
                )
                # ax.legend(labels, loc="lower left")

                ax.set_title("Change in Animal Populations")
                # Add legend with labels for each animal type
                # ax.legend(
                #     loc="upper center", bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=2
                # )
                plt.title("Population relative to beginning population")

            plt.xlabel("Months since May simulation onset")

        fig.set_figheight(8)
        fig.set_figwidth(8)
        plt.tight_layout()
        fig.suptitle(newtitle)
        path_string = str(Path(repo_root) / "results" / "large_reports" / "no_trade")

        saveloc = (
            path_string + re.sub(r'[\\/*?:"<>|\n]', "_", newtitle) + "_slaughter.png"
        )
        plt.savefig(
            # Replace problematic characters with an underscore or remove them
            saveloc,
            dpi=300,
        )
        if plot_figure:
            plt.show()
        plt.close()

    @classmethod
    def plot_fig_1ab_updated(
        crs,
        worlds,
        ratios,
        xlim,
    ):
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
        # plt.show()
        # axes = axes.ravel()
        figure_a_text_indices = [0, 4, 8, 12, 16]
        figure_a_indices = [1, 5, 9, 13, 17]
        figure_b_text_indices = [2, 6, 10, 14, 18]
        figure_b_indices = [3, 7, 11, 15, 19]
        for i in range(22):
            if i == 21:
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
                # text for figure b
                row_index = i // 4
                scenario_label = scenario_labels[row_index]
                ax = fig.add_subplot(gs[row_index, 0])

            if i in figure_a_indices:
                # figure a
                row_index = (i - 1) // 4
                scenario_label = scenario_labels[row_index]
                ax = fig.add_subplot(gs[row_index, 1])
            elif i in figure_b_text_indices:
                # text for figure b
                row_index = (i - 2) // 4
                scenario_label = scenario_labels[row_index + 5]
                ax = fig.add_subplot(gs[row_index, 2])
            elif i in figure_b_indices:
                # figure b
                row_index = (i - 3) // 4
                scenario_label = scenario_labels[row_index + 5]
                ax = fig.add_subplot(gs[row_index, 3])

            ratio = ratios[scenario_label]
            world = worlds[scenario_label]

            ax.axis("off")

            if i in figure_a_text_indices or i in figure_b_text_indices:
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
                world = world.to_crs(
                    "+proj=wintri"
                )  # Change projection to Winkel Tripel
                world.plot(
                    ax=ax,
                    column="needs_ratio",
                    cmap="viridis",
                )

                world.boundary.plot(ax=ax, color="Black", linewidth=0.1)
                ax.axes.get_xaxis().set_ticks([])
                ax.axes.get_yaxis().set_ticks([])

        plt.savefig(
            Path(repo_root) / "results" / "fig_1ab.png",
            dpi=300,
            facecolor=fig.get_facecolor(),
            transparent=False,
            edgecolor="none",
        )

        plt.tight_layout()
        plt.show()

    def helper_for_plotting_fig_3abcde(
        interpreter,
        xlim,
        gs,
        row,
        fig,
        max_y_percent,
        ADD_SECOND_COLUMN,
        split_legend=True,
    ):
        if split_legend:
            legend_column1, legend_column2 = Plotter.get_people_fed_legend(
                interpreter, True, split_legend
            )
            legend = legend_column1 + legend_column2
        else:
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
        for i, label in enumerate(("a", "b")):
            ykcals = []
            ykcals.append(interpreter.fish_kcals_equivalent.kcals)
            ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
            ykcals.append(interpreter.scp_kcals_equivalent.kcals)
            ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
            ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
            ykcals.append(interpreter.milk_kcals_equivalent.kcals)
            ykcals.append(interpreter.meat_kcals_equivalent.kcals)
            ykcals.append(interpreter.immediate_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals)
            ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

            if label == "a":
                ax = fig.add_subplot(gs[row, 1])
                if row == 4:
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
                if row == 4:
                    plt.xlabel("Months since May nuclear winter onset", fontsize=9)

                # get the sum of all the ydata up to xlim month,
                # then find max month
                # maxy = max(sum([x[0:xlim] for x in ykcals]))
                # maxy = max([sum(x[0:xlim]) for x in ykcals])
                maxy = 0
                for i in range(xlim):
                    if max_y_percent != -1:
                        maxy = max_y_percent / 100 * 2100
                    else:
                        maxy = max(maxy, sum([x[i] for x in ykcals]))

                ax.set_ylim([0, maxy])
                # ax.set_ylim([0, maxy])

                plt.ylabel("Kcals / person / day", fontsize=9)
            if label == "b" and ADD_SECOND_COLUMN:
                ax = fig.add_subplot(gs[row, 2])

                ax.plot(
                    interpreter.time_months_middle,
                    interpreter.kcals_fed,
                    color="blue",
                    linestyle="solid",
                )

                if interpreter.include_fat:
                    # 1 gram of fat is 9 kcals.
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
                if max_y_percent != -1:
                    ax.set_ylim([0, max_y_percent])
                ax.set_ylabel("% min recommended", fontsize=9)
                # ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))
            ax.set_xlim([0.5, xlim])

            if label == "a":
                if row == 1:
                    plt.title("Needs Met, Caloric\n", fontsize=10, fontweight="bold")
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                if row == 4:
                    if split_legend:
                        # # Flatten the columns into a single list while maintaining the two-column structure
                        # legend = legend_column1 + legend_column2

                        # Use ncol to specify the number of columns in the legend
                        ax.legend(
                            reversed(handles),
                            reversed(labels),
                            loc="lower center",
                            ncol=2,
                            bbox_to_anchor=(0.01, -1.7, 0.9, 1),
                            borderaxespad=0.0,
                            frameon=False,
                            prop={"size": 9},  # Adjust the font size as needed
                            # columnspacing=0.01,  # Adjust space between columns
                            handletextpad=0.25,  # Adjust the pad between the legend handle and text
                            mode="expand",  # Make the legend expand to fill the space allocated by bbox_to_anchor
                        )

                        # Adjust the width of the legend - may need to adjust subplot params or legend size
                        fig.subplots_adjust(
                            bottom=0.2
                        )  # Adjust the bottom parameter to make room for the legend

                    else:
                        plt.legend(
                            loc="center left",
                            frameon=False,
                            bbox_to_anchor=(0, -1.1),
                            shadow=False,
                            handles=reversed(handles),
                            labels=reversed(labels),
                        )

            if label == "b" and ADD_SECOND_COLUMN:
                if row == 4:
                    labels = ["Calories"]
                    if interpreter.include_fat:
                        labels += ("Fat",)
                    if interpreter.include_protein:
                        labels += ("Protein",)

                    ax.legend(
                        loc="center left",
                        frameon=False,
                        bbox_to_anchor=(-0.05, -0.3),
                        shadow=False,
                        labels=labels,
                    )
                if row == 1:
                    plt.title(
                        "Needs Met, All Macronutrients\n",
                        fontsize=10,
                        fontweight="bold",
                    )

            if row == 4:
                plt.xlabel("Months since May nuclear winter onset", fontsize=9)

        # plt.rcParams["figure.figsize"] = [12.50, 10]

        # fig.set_figheight(8)
        # fig.set_figwidth(8)
        # plt.tight_layout()

        return gs, fig

    def helper_for_plotting_fig_2abcde(
        ax,
        interpreter,
        xlim,
        title,
        add_ylabel=True,
        add_xlabel=True,
        ylim_constraint=100000,
        split_legend=True,
    ):
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
        ykcals = []
        ykcals.append(interpreter.fish_kcals_equivalent.kcals)
        ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
        ykcals.append(interpreter.scp_kcals_equivalent.kcals)
        ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
        ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
        ykcals.append(interpreter.milk_kcals_equivalent.kcals)
        ykcals.append(interpreter.meat_kcals_equivalent.kcals)
        ykcals.append(interpreter.immediate_outdoor_crops_kcals_equivalent.kcals)
        ykcals.append(interpreter.new_stored_outdoor_crops_kcals_equivalent.kcals)
        ykcals.append(interpreter.stored_food_kcals_equivalent.kcals)

        # ax.text(
        #     -0.06,
        #     1.1,
        #     "some label goes here",
        #     transform=ax.transAxes,
        #     fontsize=11,
        #     fontweight="bold",
        #     va="top",
        #     ha="right",
        # )
        ax.stackplot(
            interpreter.time_months_middle,
            np.array(ykcals),
            # labels=legend,
            colors=pal,
        )
        # get the sum of all the ydata up to xlim month,
        # then find max month
        # maxy = max(sum([x[0:xlim] for x in ykcals]))
        # maxy = max([sum(x[0:xlim]) for x in ykcals])
        maxy = 0
        for i in range(xlim):
            maxy = max(maxy, sum([x[i] for x in ykcals]))

        # maxy += maxy / 20
        ax.set_ylim([0, min(maxy, ylim_constraint)])
        ax.set_xlim([0, xlim])
        if add_ylabel:
            plt.ylabel("Kcals / person / day", fontsize=9)
        if add_xlabel:
            plt.xlabel("Months since May nuclear winter onset", fontsize=9)

        # get the handles
        handles, labels = ax.get_legend_handles_labels()
        # plt.legend(
        #     loc="center left",
        #     frameon=False,
        #     bbox_to_anchor=(-0.15, -0.4),
        #     shadow=False,
        #     handles=reversed(handles),
        #     labels=reversed(labels),
        # )

        plt.title(
            title,
            fontweight="bold",
            fontsize=9,
        )

        # plt.xlabel("Months since May nuclear winter onset")

        # plt.rcParams["figure.figsize"] = [12.50, 10]

        # fig.set_figheight(8)
        # fig.set_figwidth(8)
        # plt.tight_layout()
        # plt.show()
        return ax, legend, pal

    @classmethod
    def plot_fig_2abcde_updated(crs, lists_of_lists, xlim, split_legend=True):
        # put maps and texts together: 5X4
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

        # plt.show()
        # axes = axes.ravel()
        figure_a_indices = [0, 1, 2, 3, 4]
        figure_b_indices = [5, 6, 7, 8, 9]
        ax = []
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

        for i in range(10):
            people_fed = int(lists_of_lists[i][0])
            country_name = lists_of_lists[i][1]
            interpreter = lists_of_lists[i][2]
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
            elif i in figure_b_indices:
                add_ylabel = False
                # figure b
                row_index = i - 5
                ax.axis("off")
                ax = fig.add_subplot(gs[row_index + 1, 2])
                # xticks = ax.get_xticks()
                # ax.set_xticklabels(xticks, rotation=0, fontsize=9)
                # ax.xaxis.set_major_formatter(lambda x, pos: str(round(x / 12, 0)))

            if i in figure_a_indices or i in figure_b_indices:
                if row_index == 4:
                    add_xlabel = True
                else:
                    add_xlabel = False

                CONSTRAIN_UP_TO_PERCENT_FED = True
                if CONSTRAIN_UP_TO_PERCENT_FED:
                    # constrain to only show up to the level of people fed in the scenario
                    ylim_constraint = (
                        people_fed
                        / 100
                        * interpreter.constants["inputs"]["NUTRITION"]["KCALS_DAILY"]
                    )
                else:
                    ylim_constraint = 10000

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

        if split_legend:
            leg = ax.legend(
                handles=legend_elements,
                loc="center",
                ncol=2,
                bbox_to_anchor=(0.125, -0.01, 0.85, 1),
                borderaxespad=0.0,
                frameon=False,
                prop={"size": 9},  # Adjust the font size as needed
                # columnspacing=2.0,  # Adjust space between columns
                handletextpad=1,  # Adjust the pad between the legend handle and text
                mode="expand",
                framealpha=0,
            )

            # Adjust the width of the legend - may need to adjust subplot params or legend size
            fig.subplots_adjust(
                bottom=0.2
            )  # Adjust the bottom parameter to make room for the legend

        else:
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

        # plt.show()
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

    def plot_fig_3abcde_updated(results, xlim, ADD_SECOND_COLUMN=False):
        lists_of_lists = []
        for scenario_name, interpreter in results.items():
            print(scenario_name)
            print(interpreter.percent_people_fed)
            lists_of_lists.append(
                [interpreter.percent_people_fed, interpreter, scenario_name]
            )

        # put maps and texts together: 5X4
        fig = plt.figure(figsize=(10, 8))

        gs = gridspec.GridSpec(
            6,
            3 if ADD_SECOND_COLUMN else 2,
            wspace=0.4,
            hspace=0.5,
            width_ratios=[1, 2, 2] if ADD_SECOND_COLUMN else [1, 4],
            height_ratios=[0.125, 2, 2, 2, 2, 3],
            left=0.02,
            right=0.98,
            top=0.98,
            bottom=0.02,
        )

        ax = fig.add_subplot(gs[0, 1])
        ax.axis("off")
        if ADD_SECOND_COLUMN:
            ax = fig.add_subplot(gs[0, 2])
            ax.axis("off")

        for i in range(4):
            [
                percent_people_fed,
                interpreter,
                scenario_name,
            ] = lists_of_lists[i]
            row = i + 1
            max_y_percent = -1
            gs, fig = Plotter.helper_for_plotting_fig_3abcde(
                interpreter, xlim, gs, row, fig, max_y_percent, ADD_SECOND_COLUMN
            )
            ax = fig.add_subplot(gs[row, 0])
            percent_fed = str(int(percent_people_fed))
            labels = {1: "a", 2: "b", 3: "c", 4: "d"}
            ax.text(
                0.5,
                1.2,
                labels[row],
                transform=ax.transAxes,
                fontsize=11,
                fontweight="bold",
                va="top",
                ha="right",
            )

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
        if not interpreter1.include_fat and not interpreter1.include_protein:
            ONLY_SHOW_A_AND_B = True
        else:
            ONLY_SHOW_A_AND_B = False
        for i, label in enumerate(("a", "b", "c", "d")):
            to_show_label = label
            if ONLY_SHOW_A_AND_B and label != "a":
                # skip labels "b" and "d". We only  want  "c"  (but  we'll  display  as  "b")
                if label == "b" or label == "d":
                    continue
                i == 1
                to_show_label = "b"
            if label == "a":
                interpreter = interpreter1
            if label == "b":
                interpreter = interpreter2
            if label == "c":
                interpreter = interpreter2
            if label == "d":
                interpreter = interpreter2
            if ONLY_SHOW_A_AND_B:
                ax = fig.add_subplot(2, 1, i + 1)
            else:
                ax = fig.add_subplot(2, 2, i + 1)
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

            ax.set_xlim([0.5, xlim])

            if label == "a" or label == "c":
                ykcals = []
                ykcals.append(interpreter.fish_kcals_equivalent.kcals)
                ykcals.append(interpreter.cell_sugar_kcals_equivalent.kcals)
                ykcals.append(interpreter.scp_kcals_equivalent.kcals)

                ykcals.append(interpreter.greenhouse_kcals_equivalent.kcals)
                ykcals.append(interpreter.seaweed_kcals_equivalent.kcals)
                ykcals.append(interpreter.milk_kcals_equivalent.kcals)
                ykcals.append(interpreter.meat_kcals_equivalent.kcals)
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
                    to_show_label,
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

                plt.ylabel("Kcals / person / day")
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
                labels = ["Calories"]
                if interpreter.include_fat:
                    labels += ("Fat",)
                if interpreter.include_protein:
                    labels += ("Protein",)

                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=labels,
                )
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            if label == "a":
                maxy = max(sum([x[0:xlim1] for x in ykcals]))
                ax.set_ylim([0, maxy])
            if label == "c":
                maxy = max(sum([x[0:xlim2] for x in ykcals]))
                ax.set_ylim([0, maxy])

            plt.xlabel("Months since May ASRS")

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig(Path(repo_root) / "results" / "fig_s2abcd.png")
        print("saved figure s2abcd")
        plt.show()

    @classmethod
    def plot_fig_s1abcd(
        crs, interpreter1, interpreter2, xlim, showplot=False, split_legend=False
    ):
        legend_column1, legend_column2 = Plotter.get_people_fed_legend(
            interpreter1, False, split_legend
        )
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
                plt.title("Food availability before ASRS")
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
                ykcals.append(interpreter.milk_kcals_equivalent.kcals)
                ykcals.append(interpreter.meat_kcals_equivalent.kcals)
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
                if split_legend:
                    ax.stackplot(
                        interpreter.time_months_middle,
                        np.array(ykcals),
                        labels=legend_column1 + legend_column2,
                        colors=pal,
                    )
                else:
                    ax.stackplot(
                        interpreter.time_months_middle,
                        np.array(ykcals),
                        labels=legend_column1,
                        colors=pal,
                    )
                # get the sum of all the ydata up to xlim month,
                # then find max month
                # maxy = max(sum([x[0:xlim] for x in ykcals]))
                # ax.set_ylim([0, maxy])

                plt.ylabel("Kcals / person / day")
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
                    if split_legend:
                        # Split the legend into two columns
                        ax.legend(
                            loc="center left",
                            frameon=False,
                            bbox_to_anchor=(0, -0.2),
                            shadow=False,
                            ncol=2,
                        )
                    else:
                        # Get the handles and labels
                        handles, labels = ax.get_legend_handles_labels()
                        plt.legend(
                            loc="center left",
                            frameon=False,
                            bbox_to_anchor=(-0.15, -0.4),
                            shadow=False,
                            handles=reversed(handles),
                            labels=reversed(labels),
                        )
                plt.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.4),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels),
                )

            if label == "d":
                labels = ["Calories"]
                if interpreter.include_fat:
                    labels += ("Fat",)
                if interpreter.include_protein:
                    labels += ("Protein",)

                ax.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=labels,
                )
                ax.set_ylim(Plotter.getylim_nutrients(interpreter, xlim))

            plt.xlabel("Months since May")

        fig.set_figheight(8)
        fig.set_figwidth(10)
        plt.tight_layout(w_pad=1, h_pad=1)
        # if not showplot:
        print("saving")
        saveloc = Path(repo_root) / "results" / "fig_s1abcd.png"
        print(saveloc)
        plt.savefig(
            # Replace problematic characters with an underscore or remove them
            saveloc,
            dpi=300,
        )
        # plt.close()
        print("saved figure s1abcd")
        # else:
        plt.show()

    def getylim_nutrients(interpreter, xlim):
        kcals = interpreter.kcals_fed

        if interpreter.include_fat:
            fat = interpreter.fat_fed
        else:
            fat = interpreter.kcals_fed

        if interpreter.include_protein:
            protein = interpreter.protein_fed
        else:
            protein = interpreter.kcals_fed

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

    def plot_histogram_with_boxplot(data, xlabel, title):
        # https://www.python-graph-gallery.com/24-histogram-with-a-boxplot-on-top-seaborn
        # set a grey background (use sns.set_theme() if seaborn
        # version 0.11.0 or above)
        sns.set(style="darkgrid")

        # creating a figure composed of two matplotlib.Axes objects
        # (ax_box and ax_hist)
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
        print("95% lower")
        print(np.percentile(np.array(data), 2.5))
        print("95% upper")
        print(np.percentile(np.array(data), 97.5))

    def get_people_fed_legend(interpreter, is_nuclear_winter, split_legend=False):
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

        legend = []
        if interpreter.constants["ADD_FISH"]:
            legend = legend + ["Marine Fish"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_CELLULOSIC_SUGAR"]:
            legend = legend + ["Cellulosic Sugar"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_METHANE_SCP"]:
            legend = legend + ["Methane SCP"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_GREENHOUSES"]:
            legend = legend + ["Greenhouses"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_SEAWEED"]:
            legend = legend + ["Seaweed"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_MILK"]:
            legend = legend + ["Dairy"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_MEAT"]:
            legend = legend + ["Meat"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + ["Outdoor Crops consumed immediately"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + [OG_stored_label]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_STORED_FOOD"]:
            legend = legend + [stored_food_label]
        else:
            legend = legend + [""]

        if split_legend:
            # Split the legend into two columns
            legend_column1 = legend[: len(legend) // 2]
            legend_column2 = legend[len(legend) // 2 :]
            return legend_column1, legend_column2
        else:
            return legend

    def get_feed_biofuels_legend(interpreter):
        stored_food_label = "Stored food, either from before or after catastrophe"

        legend = []
        if interpreter.constants["ADD_CELLULOSIC_SUGAR"]:
            legend = legend + ["Cellulosic Sugar Feed"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_METHANE_SCP"]:
            legend = legend + ["Methane SCP Feed"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_SEAWEED"]:
            legend = legend + ["Seaweed Feed"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + ["Outdoor Crops consumed Feed"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_STORED_FOOD"]:
            legend = legend + [stored_food_label + " Feed"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_CELLULOSIC_SUGAR"]:
            legend = legend + ["Cellulosic Sugar Feed"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_METHANE_SCP"]:
            legend = legend + ["Methane SCP Biofuels"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_SEAWEED"]:
            legend = legend + ["Seaweed Biofuels"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + ["Outdoor Crops consumed Biofuels"]
        else:
            legend = legend + [""]

        if interpreter.constants["ADD_STORED_FOOD"]:
            legend = legend + [stored_food_label + " Biofuels"]
        else:
            legend = legend + [""]

        return legend

    def plot_monthly_reductions_seasonally(ratios):
        month_nums = np.linspace(0, len(ratios), len(ratios))
        plt.scatter(month_nums, ratios)
        plt.plot(month_nums, ratios)

        plt.xlabel("month")
        plt.ylabel("ratios to baseline production")
        plt.title("fraction of crop production per month, including seasonality")
        # plt.xlim([0, 12 * 5])
        # plt.ylim([0, 1.5])
        plt.show()

    def plot_monthly_reductions_no_seasonality(all_months_reductions):
        """
        Plot the reduction each month, showing the seasonal variability.
        """
        month_nums = np.linspace(
            0, len(all_months_reductions), len(all_months_reductions)
        )
        plt.scatter(month_nums, all_months_reductions)
        plt.title("fraction of crop production per month, not including seasonality")
        plt.xlabel("month")
        plt.ylabel("ratio to baseline production")
        # plt.xlim([0, 12 * 5])
        # plt.ylim([0, max()])
        plt.show()

    def plot_food(food, title):
        """
        Plot the food generically with the 3 macronutrients.
        """
        food.make_sure_is_a_list()

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

        saveloc = (
            Path(repo_root)
            / "results"
            / "large_reports"
            / (re.sub(r'[\\/*?:"<>|\n]', "_", title) + ".png")
        )

        plt.savefig(
            # Replace problematic characters with an underscore or remove them
            saveloc,
            dpi=300,
        )
        SHOWPLOT_FLAG = True
        if SHOWPLOT_FLAG:
            plt.show()
        # else:
        # plt.close()
        return saveloc

    def plot_food_alternative(food, title):
        """
        Plot the food generically with the 3 macronutrients (alternative layout).
        """
        food.make_sure_is_a_list()

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

        saveloc = (
            Path(repo_root)
            / "results"
            / "large_reports"
            / ("" + re.sub(r'[\\/*?:"<>|\n]', "_", title) + ".png")
        )

        plt.savefig(
            # Replace problematic characters with an underscore or remove them
            saveloc,
            dpi=300,
        )

        SHOWPLOT_FLAG = True
        if SHOWPLOT_FLAG:
            plt.show()
        # else:
        # plt.close()
        return saveloc

    @classmethod
    def plot_map_of_countries_fed(
        crs, world, ratio_fed, description, plot_map, create_slide
    ):
        if (not plot_map) and (not create_slide):
            # no point in doing anything
            return
        fig, ax = plt.subplots()
        world.boundary.plot(ax=ax, color="Black", linewidth=0.1)
        world = world.to_crs("+proj=wintri")  # Change projection to Winkel Tripel
        world.plot(
            ax=ax,
            column="needs_ratio",
            legend=True,
            cmap="viridis",
            legend_kwds={"label": "Fraction Fed", "orientation": "horizontal"},
        )
        save_title_string = (
            "Fraction of minimum macronutritional needs with no trade, ratio fed: "
            + str(ratio_fed)
        )

        # pp.title(save_title_string)
        # plt.close()
        path_string = str(
            Path(repo_root) / "results" / "large_reports" / "map_ratio_fed_"
        )
        saveloc = path_string + ratio_fed + ".png"
        fig.savefig(
            saveloc,
            dpi=300,
        )
        plt.tight_layout()

        if plot_map:
            plt.show()
        # else:
        if create_slide:
            crs.mp.insert_slide(
                title_below=save_title_string,
                description=description,
                figure_save_loc=saveloc,
            )
        plt.close()

    @classmethod
    def start_pptx(crs, title):
        mp = MakePowerpoint()
        mp.create_title_slide(title)

        crs.mp = mp

    @classmethod
    def end_pptx(crs, saveloc):
        if not os.path.exists(Path(repo_root) / "results" / "large_reports"):
            os.mkdir(Path(repo_root) / "results" / "large_reports")
        crs.mp.save_ppt(re.sub(r'[*?:"<>|\n]', "_", saveloc))
