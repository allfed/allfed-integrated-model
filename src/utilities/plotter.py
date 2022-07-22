################################ plotter.py ###################################
##                                                                            #
##            A set of utility functions useful for plotting                  #
##                                                                            #
###############################################################################


from scipy.stats import t
import seaborn as sns
from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib.gridspec as gridspec
import os
import sys
import pandas as pd

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# in some linux win manager setups matplotlib plotting doesn't seem to play nice
# matplotlib.use('Svg')
# matplotlib.use('QtAgg')


class Plotter:
    def __init__(self):
        pass

    def plot_fig_1ab(analysis1, xlim):
        legend = Plotter.get_people_fed_legend(analysis1, True)
        fig = plt.figure()
        pal = [
            "#1e7ecd",
            "#71797E",
            "#76d7ea",
            "#056608",
            "#fdfff5",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]
        for i, label in enumerate(("a", "b")):
            if label == "a":
                analysis = analysis1
            if label == "b":
                analysis = analysis1
            ax = fig.add_subplot(1, 2, i + 1)
            ax.set_xlim([0.5, xlim])

            ykcals = []
            ykcals.append(analysis.billions_fed_fish_kcals)
            ykcals.append(
                (
                    np.array(analysis.billions_fed_CS_kcals)
                    + np.array(analysis.billions_fed_SCP_kcals)
                )
            )
            ykcals.append(analysis.billions_fed_GH_kcals)
            ykcals.append(analysis.billions_fed_seaweed_kcals)
            ykcals.append(
                (
                    analysis.billions_fed_milk_kcals
                    + analysis.billions_fed_h_e_milk_kcals
                )
            )
            ykcals.append(
                (
                    analysis.billions_fed_meat_kcals
                    + analysis.billions_fed_h_e_meat_kcals
                )
            )
            ykcals.append(analysis.billions_fed_immediate_OG_kcals)
            ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
            ykcals.append(analysis.billions_fed_SF_kcals)

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
                ax.stackplot(
                    analysis.time_months_middle,
                    np.array(ykcals) / analysis.constants["CONVERSION_TO_KCALS"],
                    labels=legend,
                    colors=pal,
                )
                # get the sum of all the ydata up to xlim month,
                # then find max month
                maxy = max(sum([x[0:xlim] for x in ykcals]))
                ax.set_ylim([0, maxy / analysis.constants["CONVERSION_TO_KCALS"]])

                plt.ylabel("Calories / capita / day")
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
                plt.xlabel("Months since May ASRS onset")

                ax.plot(
                    analysis.time_months_middle,
                    analysis.kcals_fed
                    / analysis.constants["CONVERSION_TO_KCALS"]
                    / analysis.constants["inputs"]["NUTRITION"]["KCALS_DAILY"],
                    color="blue",
                    linestyle="solid",
                )

                ax.plot(
                    analysis.time_months_middle,
                    analysis.protein_fed
                    / analysis.constants["CONVERSION_TO_PROTEIN"]
                    / analysis.constants["inputs"]["NUTRITION"]["PROTEIN_DAILY"],
                    color="red",
                    linestyle="dotted",
                )

                # 1 gram of fat is 9 kcals.
                ax.plot(
                    analysis.time_months_middle,
                    analysis.fat_fed
                    / analysis.constants["CONVERSION_TO_FAT"]
                    / analysis.constants["inputs"]["NUTRITION"]["FAT_DAILY"],
                    color="green",
                    linestyle="dashed",
                )

                ax.set_ylabel("Fraction of minimum recommendation")
                ax.set_ylim(Plotter.getylim_nutrients(analysis, xlim))

            if label == "a":
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                plt.legend(
                    loc="center left",
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.4),
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
                plt.title("Food availability")
            if label == "b":
                plt.title("Available food macronutrition")

            plt.xlabel("Months since May ASRS onset")

        # plt.rcParams["figure.figsize"] = [12.50, 10]

        fig.set_figheight(8)
        fig.set_figwidth(8)
        plt.tight_layout()
        # plt.savefig('../../results/fig_1ab.png')
        print("saved figure 1ab")
        plt.show()

    def plot_fig_2abcd(analysis1, analysis2, xlim):
        legend = Plotter.get_people_fed_legend(analysis1, True)
        fig = plt.figure()
        pal = [
            "#1e7ecd",
            "#71797E",
            "#76d7ea",
            "#056608",
            "#fdfff5",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        for i, label in enumerate(("a", "b", "c", "d")):
            if label == "a":
                analysis = analysis1
            if label == "b":
                analysis = analysis1
            if label == "c":
                analysis = analysis2
            if label == "d":
                analysis = analysis2
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
                ykcals.append(analysis.billions_fed_fish_kcals)
                ykcals.append(
                    (
                        np.array(analysis.billions_fed_CS_kcals)
                        + np.array(analysis.billions_fed_SCP_kcals)
                    )
                )
                ykcals.append(analysis.billions_fed_GH_kcals)
                ykcals.append(analysis.billions_fed_seaweed_kcals)
                ykcals.append(
                    (
                        analysis.billions_fed_milk_kcals
                        + analysis.billions_fed_h_e_milk_kcals
                    )
                )
                ykcals.append(
                    (
                        analysis.billions_fed_meat_kcals
                        + analysis.billions_fed_h_e_meat_kcals
                    )
                )
                ykcals.append(analysis.billions_fed_immediate_OG_kcals)
                ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
                ykcals.append(analysis.billions_fed_SF_kcals)

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
                    analysis.time_months_middle,
                    np.array(ykcals) / analysis.constants["CONVERSION_TO_KCALS"],
                    labels=legend,
                    colors=pal,
                )

                # get the sum of all the ydata up to xlim month,
                # then find max month
                maxy = max(sum([x[0:xlim] for x in ykcals]))
                ax.set_ylim([0, maxy / analysis.constants["CONVERSION_TO_KCALS"]])

                plt.ylabel("Calories / capita / day")
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
                plt.xlabel("Months since May ASRS onset")

                ax.plot(
                    analysis.time_months_middle,
                    analysis.kcals_fed
                    / analysis.constants["CONVERSION_TO_KCALS"]
                    / analysis.constants["inputs"]["NUTRITION"]["KCALS_DAILY"],
                    color="blue",
                    linestyle="solid",
                )

                ax.plot(
                    analysis.time_months_middle,
                    analysis.protein_fed
                    / analysis.constants["CONVERSION_TO_PROTEIN"]
                    / analysis.constants["inputs"]["NUTRITION"]["PROTEIN_DAILY"],
                    color="red",
                    linestyle="dotted",
                )

                ax.plot(
                    analysis.time_months_middle,
                    analysis.fat_fed
                    / analysis.constants["CONVERSION_TO_FAT"]
                    / analysis.constants["inputs"]["NUTRITION"]["FAT_DAILY"],
                    color="green",
                    linestyle="dashed",
                )

                ax.set_ylabel("Fraction of minimum recommendation")
                ax.set_ylim(Plotter.getylim_nutrients(analysis, xlim))

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
                ax.set_ylim(Plotter.getylim_nutrients(analysis, xlim))

            plt.xlabel("Months since May ASRS onset")

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig("../../results/fig_2abcd.png")
        print("saved figure 2abcd")
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
                # sns.boxplot(monte_carlo_data, ax=ax_box, showfliers=False)
                sns.histplot(data=monte_carlo_data, ax=ax_hist)
                ax_hist.set(xlabel="mean caloric availability (Kcals / person / day)")
                ax_hist.set(title="Monte Carlo outcomes")

        plt.tight_layout()
        plt.savefig("../../results/fig_3ab.png")
        print("saved figure 3ab")
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_fig_s1(variables, N):
        # create histogram of variables
        fig, axs = plt.subplots(2, 4, figsize=(10, 7))

        Plotter.plot_histogram(
            axs[0, 0],
            variables["seaweed_production_rate"],
            1000,
            "seaweed growth per day\n (%)",
            "number of scenarios",
            "",
        )
        Plotter.plot_histogram(
            axs[0, 1],
            variables["seaweed_new"],
            1000,
            "seaweed area built \n(1000s km^2/month)",
            "number of scenarios",
            "seaweed new area built monthly",
        )
        Plotter.plot_histogram(
            axs[0, 2],
            variables["max_seaweed"],
            1000,
            "seaweed max calories\n (% of diet)",
            "number of scenarios",
            "Seaweed percent dietary calories",
        )
        # divide by the baseline from Xia et al
        no_relocation_nuclear_winter = 0.89
        Plotter.plot_histogram(
            axs[0, 3],
            (1 - variables["rotation_outcome_kcals"] * no_relocation_nuclear_winter)
            / (1 - no_relocation_nuclear_winter),
            1000,
            "ratio to baseline calories\nrelocation outcome year 3",
            "number of scenarios",
            "",
        )
        Plotter.plot_histogram(
            axs[1, 0],
            variables["greenhouse_gain"],
            1000,
            "greenhouse yield gain \n(%)",
            "number of scenarios",
            "gain (%)",
        )
        Plotter.plot_histogram(
            axs[1, 1],
            variables["greenhouse_area"],
            1000,
            "greenhouse area scale factor",
            "number of scenarios",
            "seaweed new area built monthly",
        )
        Plotter.plot_histogram(
            axs[1, 2],
            variables["industrial_foods"],
            1000,
            "industrial foods scale factor",
            "number of scenarios",
            "",
        )
        Plotter.plot_histogram(
            axs[1, 3],
            variables["industrial_foods_delay"],
            100,
            "delay industrial construction\n (months)",
            "number of scenarios",
            "months delayed starting",
        )
        plt.tight_layout()

        plt.rcParams["figure.figsize"] = [12, 9]
        plt.savefig("../../results/fig_s1.png")
        print("saved figure s1")
        plt.show()

    def plot_fig_s2abcd(analysis1, analysis2, xlim1, xlim2):
        legend = Plotter.get_people_fed_legend(analysis1, True)
        fig = plt.figure()
        pal = [
            "#1e7ecd",
            "#71797E",
            "#76d7ea",
            "#056608",
            "#fdfff5",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        for i, label in enumerate(("a", "b", "c", "d")):
            if label == "a":
                analysis = analysis1
            if label == "b":
                analysis = analysis1
            if label == "c":
                analysis = analysis2
            if label == "d":
                analysis = analysis2
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
                ykcals.append(analysis.billions_fed_fish_kcals)
                ykcals.append(
                    (
                        np.array(analysis.billions_fed_CS_kcals)
                        + np.array(analysis.billions_fed_SCP_kcals)
                    )
                )
                ykcals.append(analysis.billions_fed_GH_kcals)
                ykcals.append(analysis.billions_fed_seaweed_kcals)
                ykcals.append(
                    (
                        analysis.billions_fed_milk_kcals
                        + analysis.billions_fed_h_e_milk_kcals
                    )
                )
                ykcals.append(
                    (
                        analysis.billions_fed_meat_kcals
                        + analysis.billions_fed_h_e_meat_kcals
                    )
                )
                ykcals.append(analysis.billions_fed_immediate_OG_kcals)
                ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
                ykcals.append(analysis.billions_fed_SF_kcals)

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
                    analysis.time_months_middle,
                    np.array(ykcals) / analysis.constants["CONVERSION_TO_KCALS"],
                    labels=legend,
                    colors=pal,
                )

                plt.ylabel("Calories / capita / day")
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
                plt.xlabel("Months since May ASRS onset")

                ax.plot(
                    analysis.time_months_middle,
                    analysis.kcals_fed
                    / analysis.constants["CONVERSION_TO_KCALS"]
                    / analysis.constants["inputs"]["NUTRITION"]["KCALS_DAILY"],
                    color="blue",
                    linestyle="solid",
                )

                ax.plot(
                    analysis.time_months_middle,
                    analysis.protein_fed
                    / analysis.constants["CONVERSION_TO_PROTEIN"]
                    / analysis.constants["inputs"]["NUTRITION"]["PROTEIN_DAILY"],
                    color="red",
                    linestyle="dotted",
                )

                ax.plot(
                    analysis.time_months_middle,
                    analysis.fat_fed
                    / analysis.constants["CONVERSION_TO_FAT"]
                    / analysis.constants["inputs"]["NUTRITION"]["FAT_DAILY"],
                    color="green",
                    linestyle="dashed",
                )

                ax.set_ylabel("Fraction of minimum recommendation")
                ax.set_ylim(Plotter.getylim_nutrients(analysis, xlim))

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
                ax.set_ylim(Plotter.getylim_nutrients(analysis, xlim))

            if label == "a":
                maxy = max(sum([x[0:xlim1] for x in ykcals]))
                ax.set_ylim([0, maxy / analysis.constants["CONVERSION_TO_KCALS"]])
            if label == "c":
                maxy = max(sum([x[0:xlim2] for x in ykcals]))
                ax.set_ylim([0, maxy / analysis.constants["CONVERSION_TO_KCALS"]])

            plt.xlabel("Months since May ASRS")

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig("../../results/fig_s2abcd.png")
        print("saved figure s2abcd")
        plt.show()

    def plot_fig_s1abcd(analysis1, analysis2, xlim):
        legend = Plotter.get_people_fed_legend(analysis1, False)
        fig = plt.figure()
        pal = [
            "#1e7ecd",
            "#71797E",
            "#76d7ea",
            "#056608",
            "#fdfff5",
            "#ff0606",
            "#a5d610",
            "#ffeb7a",
            "#e7d2ad",
        ]

        for i, label in enumerate(("a", "b", "c", "d")):
            if label == "a":
                analysis = analysis1
            if label == "b":
                analysis = analysis1
            if label == "c":
                analysis = analysis2
            if label == "d":
                analysis = analysis2
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
                ykcals.append(analysis.billions_fed_fish_kcals)
                ykcals.append(
                    (
                        np.array(analysis.billions_fed_CS_kcals)
                        + np.array(analysis.billions_fed_SCP_kcals)
                    )
                )
                ykcals.append(analysis.billions_fed_GH_kcals)
                ykcals.append(analysis.billions_fed_seaweed_kcals)
                ykcals.append(
                    (
                        analysis.billions_fed_milk_kcals
                        + analysis.billions_fed_h_e_milk_kcals
                    )
                )
                ykcals.append(
                    (
                        analysis.billions_fed_meat_kcals
                        + analysis.billions_fed_h_e_meat_kcals
                    )
                )
                ykcals.append(analysis.billions_fed_immediate_OG_kcals)
                ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
                ykcals.append(analysis.billions_fed_SF_kcals)

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
                    analysis.time_months_middle,
                    np.array(ykcals) / analysis.constants["CONVERSION_TO_KCALS"],
                    labels=legend,
                    colors=pal,
                )

                # get the sum of all the ydata up to xlim month,
                # then find max month
                maxy = max(sum([x[0:xlim] for x in ykcals]))
                # ax.set_ylim([0, maxy / analysis.constants["CONVERSION_TO_KCALS"]])

                plt.ylabel("Calories / capita / day")
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
                plt.xlabel("Months since May ASRS onset")

                ax.plot(
                    analysis.time_months_middle,
                    analysis.kcals_fed
                    / analysis.constants["CONVERSION_TO_KCALS"]
                    / analysis.constants["inputs"]["NUTRITION"]["KCALS_DAILY"],
                    color="blue",
                    linestyle="solid",
                )

                ax.plot(
                    analysis.time_months_middle,
                    analysis.fat_fed
                    / analysis.constants["CONVERSION_TO_FAT"]
                    / analysis.constants["inputs"]["NUTRITION"]["FAT_DAILY"],
                    color="green",
                    linestyle="dashed",
                )

                ax.plot(
                    analysis.time_months_middle,
                    analysis.protein_fed
                    / analysis.constants["CONVERSION_TO_PROTEIN"]
                    / analysis.constants["inputs"]["NUTRITION"]["PROTEIN_DAILY"],
                    color="red",
                    linestyle="dotted",
                )

                ax.set_ylabel("Fraction of minimum recommendation")

                # ax.set_ylim(Plotter.getylim_nutrients(analysis, xlim))

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
                # ax.set_ylim(Plotter.getylim_nutrients(analysis, xlim))

            plt.xlabel("Months since May")

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        # plt.savefig('../../results/fig_s1abcd.png')
        print("saved figure s1abcd")
        plt.show()

    def getylim_nutrients(analysis, xlim):
        kcals = (
            analysis.kcals_fed
            / analysis.constants["CONVERSION_TO_KCALS"]
            / analysis.constants["inputs"]["NUTRITION"]["KCALS_DAILY"]
        )

        protein = (
            analysis.protein_fed
            / analysis.constants["CONVERSION_TO_PROTEIN"]
            / analysis.constants["inputs"]["NUTRITION"]["PROTEIN_DAILY"]
        )

        fat = (
            analysis.fat_fed
            / analysis.constants["CONVERSION_TO_FAT"]
            / analysis.constants["inputs"]["NUTRITION"]["FAT_DAILY"]
        )

        min_plot = (
            min([min(fat[0:xlim]), min(protein[0:xlim]), min(kcals[0:xlim])]) - 0.2
        )

        max_plot = (
            max([max(fat[0:xlim]), max(protein[0:xlim]), max(kcals[0:xlim])]) + 0.2
        )

        return [min_plot, max_plot]

    def plot_histogram(ax, data, N, xlabel, ylabel, title):
        num_bins = int(N / 10)
        # plt.title("Food Available After Delayed Shutoff and Waste ")
        # ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.hist(data, bins=num_bins, facecolor="blue", alpha=0.5)
        ax.set_xlabel(xlabel)
        # ax.set_title(title)
        # ax.set_ylabel()

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

    def get_people_fed_legend(analysis, is_nuclear_winter):
        if not is_nuclear_winter:
            stored_food_label = (
                "Crops consumed that month that were\nstored before simulation"
            )
            OG_stored_label = (
                "Crops consumed that month that were\nstored after simulation start"
            )
        else:
            stored_food_label = (
                "Crops consumed that month that were\nstored before ASRS onset"
            )
            OG_stored_label = (
                "Crops consumed that month that were\nstored after ASRS onset"
            )

        legend = []
        if analysis.constants["ADD_FISH"]:
            legend = legend + ["Marine Fish"]
        else:
            legend = legend + [""]

        if (
            analysis.constants["ADD_CELLULOSIC_SUGAR"]
            or analysis.constants["ADD_METHANE_SCP"]
        ):
            legend = legend + ["Industrial Foods"]
        else:
            legend = legend + [""]

        if analysis.constants["ADD_GREENHOUSES"]:
            legend = legend + ["Greenhouses"]
        else:
            legend = legend + [""]

        if analysis.constants["ADD_SEAWEED"]:
            legend = legend + ["Seaweed"]
        else:
            legend = legend + [""]

        if analysis.constants["ADD_DAIRY"]:
            legend = legend + ["Dairy Milk"]
        else:
            legend = legend + [""]

        if analysis.constants["ADD_MEAT"]:
            legend = legend + ["Meat"]
        else:
            legend = legend + [""]

        if analysis.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + ["Outdoor Crops consumed immediately"]
        else:
            legend = legend + [""]

        if analysis.constants["ADD_OUTDOOR_GROWING"]:
            legend = legend + [OG_stored_label]
        else:
            legend = legend + [""]

        if analysis.constants["ADD_STORED_FOOD"]:
            legend = legend + [stored_food_label]
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
        plot1 = plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan=2)
        plot2 = plt.subplot2grid((2, 2), (0, 1))
        plot3 = plt.subplot2grid((2, 2), (1, 1))

        # Using Numpy to create an array x
        x = np.arange(len(vals1))

        # Plot for vals1
        plot1.plot(x, vals1)
        plot1.set_ylabel(title1.split(" each month")[0])
        plot1.set_xlabel("month")
        plot1.set_title("kcals: " + title1)

        # Plot for  vals2
        plot2.plot(x, vals2)
        plot2.set_ylabel(title2.split(" each month")[0])
        plot2.set_xlabel("month")
        plot2.set_title("fat: " + title2)

        # Plot for vals3
        plot3.plot(x, vals3)
        plot3.set_ylabel(title3.split(" each month")[0])
        plot3.set_xlabel("month")
        plot3.set_title("protein: " + title3)

        # Packing all the plots and displaying them
        plt.tight_layout()
        fig.suptitle(title)
        plt.show()

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
        plot1 = plt.subplot2grid((3, 1), (0, 0))
        plot2 = plt.subplot2grid((3, 1), (1, 0))
        plot3 = plt.subplot2grid((3, 1), (2, 0))

        # Using Numpy to create an array x
        x = np.arange(len(vals1))

        # Plot for vals1
        plot1.plot(x, vals1)
        plot1.set_ylabel(title1.split(" each month")[0])
        plot1.set_xlabel("month")
        plot1.set_title(title1)

        # Plot for  vals2
        plot2.plot(x, vals2)
        plot2.set_ylabel(title2.split(" each month")[0])
        plot2.set_xlabel("month")
        plot2.set_title(title2)

        # Plot for vals3
        plot3.plot(x, vals3)
        plot3.set_ylabel(title3.split(" each month")[0])
        plot3.set_xlabel("month")
        plot3.set_title(title3)

        # Packing all the plots and displaying them
        plt.tight_layout()
        fig.suptitle(title)
        plt.show()
