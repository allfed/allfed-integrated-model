'''

A set of utility functions useful for plotting 

'''
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
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
# matplotlib.use('Svg')
# matplotlib.use('QtAgg')


class Plotter:
    def __init__(self):
        pass

    def plot_fig_1ab(analysis1, xlim):
        legend = Plotter.get_people_fed_legend(analysis1)
        fig = plt.figure()
        pal = ["#1e7ecd",
               "#71797E",
               "#76d7ea",
               "#056608",
               "#fdfff5",
               "#f9906f",
               "#a5d610",
               "#ffeb7a",
               "#e7d2ad"]
        for i, label in enumerate(('a', 'b')):
            if(label == 'a'):
                analysis = analysis1
            if(label == 'b'):
                analysis = analysis1
            ax = fig.add_subplot(1, 2, i+1)
            ax.set_xlim([0.5, xlim])

            ykcals = []
            ykcals.append(analysis.billions_fed_fish_kcals)
            ykcals.append((np.array(analysis.billions_fed_CS_kcals) +
                           np.array(analysis.billions_fed_SCP_kcals)))
            ykcals.append(analysis.billions_fed_GH_kcals)
            ykcals.append(analysis.billions_fed_seaweed_kcals)
            ykcals.append((analysis.billions_fed_milk_kcals +
                           analysis.billions_fed_h_e_milk_kcals))
            ykcals.append((analysis.billions_fed_meat_kcals +
                           analysis.billions_fed_h_e_meat_kcals))
            ykcals.append(analysis.billions_fed_immediate_OG_kcals)
            ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
            ykcals.append(analysis.billions_fed_SF_kcals)

            if(label == 'a'):
                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                ax.stackplot(analysis.time_months_middle,
                             np.array(ykcals) / analysis.c["CONVERT_TO_KCALS"],
                             labels=legend, colors=pal)
                # get the sum of all the ydata up to xlim month,
                # then find max month
                maxy = max(sum([x[0:xlim] for x in ykcals]))
                ax.set_ylim([0, maxy/ analysis.c["CONVERT_TO_KCALS"]])

                plt.ylabel('Calories / capita / day')
            if(label == 'b'):
                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                plt.xlabel('Months since May ASRS onset')

                ax.plot(analysis.time_months_middle,
                        analysis.kcals_fed / analysis.c["CONVERT_TO_KCALS"]
                        / analysis.c["inputs"]['NUTRITION']['KCALS_DAILY'],
                        marker='o',
                        markersize=6,
                        color='blue',
                        linestyle='solid')

                ax.plot(analysis.time_months_middle,
                        analysis.protein_fed / analysis.c["CONVERT_TO_PROTEIN"]
                        / analysis.c["inputs"]['NUTRITION']['PROTEIN_DAILY'],
                        marker='^',
                        markersize=6,
                        color='red',
                        linestyle='dotted')

                # 1 gram of fat is 9 kcals.
                ax.plot(analysis.time_months_middle,
                        analysis.fat_fed / analysis.c["CONVERT_TO_FAT"]
                        / analysis.c["inputs"]['NUTRITION']['FAT_DAILY'],
                        marker='x',
                        markersize=6,
                        color='green',
                        linestyle='dashed')

                ax.set_ylabel('Fraction of minimum recommendation')
                ax.set_ylim([0.6, 1.7])

            if(label == 'a'):
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                plt.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.4),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels))

            if(label == 'b'):
                ax.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=['Calories',
                            'Fat',
                            'Protein'])

            if(label == 'a'):
                plt.title('Food availability')
            if(label == 'b'):
                plt.title('Available food macronutrition')

            plt.xlabel('Months since May ASRS onset')

        # plt.rcParams["figure.figsize"] = [12.50, 10]

        fig.set_figheight(8)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_fig_2abcd(analysis1, analysis2, xlim):
        legend = Plotter.get_people_fed_legend(analysis1)
        fig = plt.figure()
        pal = ["#1e7ecd",
               "#71797E",
               "#76d7ea",
               "#056608",
               "#fdfff5",
               "#f9906f",
               "#a5d610",
               "#ffeb7a",
               "#e7d2ad"]

        for i, label in enumerate(('a', 'b', 'c', 'd')):
            if(label == 'a'):
                analysis = analysis1
            if(label == 'b'):
                analysis = analysis1
            if(label == 'c'):
                analysis = analysis2
            if(label == 'd'):
                analysis = analysis2
            ax = fig.add_subplot(2, 2, i + 1)
            ax.set_xlim([0.5, xlim])
            if(label == 'a'):
                plt.title('Food availability')
            if(label == 'b'):
                plt.title('Available food macronutrition')
            if(label == 'c'):
                plt.title("Diet composition")
            if(label == 'd'):
                plt.title("Diet macronutrition")
            if(label == 'a' or label == 'c'):

                ykcals = []
                ykcals.append(analysis.billions_fed_fish_kcals)
                ykcals.append((np.array(analysis.billions_fed_CS_kcals) +
                               np.array(analysis.billions_fed_SCP_kcals)))
                ykcals.append(analysis.billions_fed_GH_kcals)
                ykcals.append(analysis.billions_fed_seaweed_kcals)
                ykcals.append((analysis.billions_fed_milk_kcals +
                               analysis.billions_fed_h_e_milk_kcals))
                ykcals.append((analysis.billions_fed_meat_kcals +
                               analysis.billions_fed_h_e_meat_kcals))
                ykcals.append(analysis.billions_fed_immediate_OG_kcals)
                ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
                ykcals.append(analysis.billions_fed_SF_kcals)

                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                ax.stackplot(analysis.time_months_middle,
                             np.array(ykcals)
                             / analysis.c["CONVERT_TO_KCALS"],
                             labels=legend, colors=pal)

                # get the sum of all the ydata up to xlim month,
                # then find max month
                maxy = max(sum([x[0:xlim] for x in ykcals]))
                ax.set_ylim([0, maxy/ analysis.c["CONVERT_TO_KCALS"]])

                plt.ylabel('Calories / capita / day')
            if(label == 'b' or label == 'd'):
                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                plt.xlabel('Months since May ASRS onset')

                ax.plot(analysis.time_months_middle,
                        analysis.kcals_fed / analysis.c["CONVERT_TO_KCALS"]
                        / analysis.c["inputs"]['NUTRITION']['KCALS_DAILY'],
                        marker='o',
                        markersize=6,
                        color='blue',
                        linestyle='solid')

                ax.plot(analysis.time_months_middle,
                        analysis.protein_fed / analysis.c["CONVERT_TO_PROTEIN"]
                        / analysis.c["inputs"]['NUTRITION']['PROTEIN_DAILY'],
                        marker='^',
                        markersize=6,
                        color='red',
                        linestyle='dotted')

                ax.plot(analysis.time_months_middle,
                        analysis.fat_fed / analysis.c["CONVERT_TO_FAT"]
                        / analysis.c["inputs"]['NUTRITION']['FAT_DAILY'],
                        marker='x',
                        markersize=6,
                        color='green',
                        linestyle='dashed')

                ax.set_ylabel('Fraction of minimum recommendation')
                ax.set_ylim([1.3, 2.4])


            if(label == 'c'):
                # ax.legend(loc='center left', frameon=False,bbox_to_anchor=(0, -0.2), shadow=False,)
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                plt.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.5),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels))

            if(label == 'd'):
                ax.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=['Calories',
                            'Fat',
                            'Protein'])
                ax.set_ylim([0.9, 2.1])

            plt.xlabel('Months since May ASRS onset')

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_fig_3ab(monte_carlo_data, food_names, removed, added):
        # fig = plt.figure()
        fig = plt.figure(figsize=(10, 10))
        gs = gridspec.GridSpec(4, 2, wspace=0.3)
        print("95% lower")
        print(np.percentile(np.array(monte_carlo_data), 2.5))
        print("95% upper")
        print(np.percentile(np.array(monte_carlo_data), 97.5))
        for i, label in enumerate(('a', 'b')):
            if(label == 'a'):
                ax3 = fig.add_subplot(gs[0:3, 0])
                ax3.text(-0.06, 1.1, label, transform=ax3.transAxes,
                         fontsize=11, fontweight='bold', va='top', ha='right')
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                ax4 = fig.add_subplot(gs[3, 0])
                # ax4.axis("off")
                ax4.spines['top'].set_visible(False)
                ax4.spines['bottom'].set_visible(False)
                ax4.spines['right'].set_visible(False)
                ax4.spines['left'].set_visible(False)

            if(label == 'b'):
                ax_box = fig.add_subplot(gs[0, 1])
                ax_box.text(-0.06, 1.35, label, transform=ax_box.transAxes,
                            fontsize=11, fontweight='bold', va='top', ha='right')
                ax_hist = fig.add_subplot(gs[1:3, 1])
                ax_box.axis("off")

            if(label == 'a'):
                dict = {}
                dict['category'] = []
                dict['food'] = []
                dict['calories'] = []
                for i in range(0, len(food_names)):
                    f = food_names[i]
                    food_removed = removed[f]
                    dict['category'] = np.append(dict['category'],
                                                 ['loss of calories if removed'] * len(food_removed))
                    dict['food'] = np.append(dict['food'], [f] * len(food_removed))
                    dict['calories'] = np.append(dict['calories'], removed[f])
                    food_added = added[f]
                    dict['category'] = np.append(dict['category'],
                                                 ['additional calories if included'] * len(food_added))
                    dict['food'] = np.append(dict['food'], [f] * len(food_added))
                    dict['calories'] = np.append(dict['calories'], added[f])
                df = pd.DataFrame.from_dict(dict)
                sns.boxplot(data=df, x='calories', y='food',
                            hue='category', ax=ax3, showfliers=False)
                ax3.get_legend().remove()
                ax3.set(title="Comparative evaluation")
                plt.legend(bbox_to_anchor=(.0, -.1), )
                ax3.set(xlabel="change in caloric availability (Kcals / person / day)")
                plt.ylabel('')
                handles, labels = ax3.get_legend_handles_labels()
                ax4.legend(handles, labels, frameon=False, bbox_to_anchor=(.8, .8))
                ax4.axis("off")
            if(label == 'b'):
                sns.boxplot(monte_carlo_data, ax=ax_box, showfliers=False)
                sns.histplot(data=monte_carlo_data, ax=ax_hist)
                ax_hist.set(xlabel="mean caloric availability (Kcals / person / day)")
                ax_box.set(title="Monte Carlo outcomes")

        plt.tight_layout()
        plt.savefig("plot.svg")
        plt.rcParams["figure.figsize"] = [15, 8]
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_fig_s1(variables, N):
        # create histogram of variables
        fig, axs = plt.subplots(2, 4, figsize=(10, 7))

        Plotter.plot_histogram(axs[0, 0],
                               variables['seaweed_production_rate'],
                               1000,
                               "seaweed growth per day\n (%)",
                               "number of scenarios",
                               "")
        Plotter.plot_histogram(axs[0, 1],
                               variables['seaweed_new'],
                               1000,
                               "seaweed area built \n(1000s km^2/month)",
                               "number of scenarios",
                               "seaweed new area built monthly")
        Plotter.plot_histogram(axs[0, 2],
                               variables['max_seaweed'],
                               1000,
                               "seaweed max calories\n (% of diet)",
                               "number of scenarios",
                               "Seaweed percent dietary calories")
        Plotter.plot_histogram(axs[0, 3],
                               variables['rotation_outcome'],
                               100,
                               "rotation outcome\n 0=50% relocated\n1=80% relocated\n2=100% relocated",
                               "number of scenarios",
                               "")
        Plotter.plot_histogram(axs[1, 0],
                               variables['greenhouse_gain'],
                               1000,
                               "greenhouse yield gain \n(%)",
                               "number of scenarios",
                               "gain (%)")
        Plotter.plot_histogram(axs[1, 1],
                               variables['greenhouse_area'],
                               1000,
                               "greenhouse area scale factor",
                               "number of scenarios",
                               "seaweed new area built monthly")
        Plotter.plot_histogram(axs[1, 2],
                               variables['industrial_foods'],
                               1000,
                               "industrial foods scale factor",
                               "number of scenarios",
                               "")
        Plotter.plot_histogram(axs[1, 3],
                               variables['industrial_foods_delay'],
                               100,
                               "delay industrial construction\n (months)",
                               "number of scenarios",
                               "months delayed starting")
        plt.tight_layout()

        plt.rcParams["figure.figsize"] = [12, 9]
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_figure_s3abcd(analysis1,
                       analysis2,
                       xlim1,
                       xlim2):
        legend = Plotter.get_people_fed_legend(analysis1)
        fig = plt.figure()
        pal = ["#1e7ecd",
               "#71797E",
               "#76d7ea",
               "#056608",
               "#fdfff5",
               "#f9906f",
               "#a5d610",
               "#ffeb7a",
               "#e7d2ad"]

        for i, label in enumerate(('a', 'b', 'c', 'd')):
            if(label == 'a'):
                analysis = analysis1
            if(label == 'b'):
                analysis = analysis1
            if(label == 'c'):
                analysis = analysis2
            if(label == 'd'):
                analysis = analysis2
            ax = fig.add_subplot(2, 2, i + 1)
            if(label == 'a'):
                ax.set_xlim([0.5, xlim1])
                plt.title("Resilient food availability")
            if(label == 'b'):
                ax.set_xlim([0.5, xlim1])
                plt.title("Resilient food macronutrition")
            if(label == 'c'):
                ax.set_xlim([0.5, xlim2])
                plt.title('No resilient food availability')
            if(label == 'd'):
                ax.set_xlim([0.5, xlim2])
                plt.title('No resilient food macronutrition')
            if(label == 'a' or label == 'c'):

                ykcals = []
                ykcals.append(analysis.billions_fed_fish_kcals)
                ykcals.append((np.array(analysis.billions_fed_CS_kcals) +
                               np.array(analysis.billions_fed_SCP_kcals)))
                ykcals.append(analysis.billions_fed_GH_kcals)
                ykcals.append(analysis.billions_fed_seaweed_kcals)
                ykcals.append((analysis.billions_fed_milk_kcals +
                               analysis.billions_fed_h_e_milk_kcals))
                ykcals.append((analysis.billions_fed_meat_kcals +
                               analysis.billions_fed_h_e_meat_kcals))
                ykcals.append(analysis.billions_fed_immediate_OG_kcals)
                ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
                ykcals.append(analysis.billions_fed_SF_kcals)

                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                ax.stackplot(analysis.time_months_middle,
                             np.array(ykcals)
                             / analysis.c["CONVERT_TO_KCALS"],
                             labels=legend, colors=pal)

                plt.ylabel('Calories / capita / day')
            if(label == 'b' or label == 'd'):
                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                plt.xlabel('Months since May ASRS onset')

                ax.plot(analysis.time_months_middle,
                        analysis.kcals_fed / analysis.c["CONVERT_TO_KCALS"]
                        / analysis.c["inputs"]['NUTRITION']['KCALS_DAILY'],
                        marker='o',
                        markersize=6,
                        color='blue',
                        linestyle='solid')

                ax.plot(analysis.time_months_middle,
                        analysis.protein_fed / analysis.c["CONVERT_TO_PROTEIN"]
                        / analysis.c["inputs"]['NUTRITION']['PROTEIN_DAILY'],
                        marker='^',
                        markersize=6,
                        color='red',
                        linestyle='dotted')

                ax.plot(analysis.time_months_middle,
                        analysis.fat_fed / analysis.c["CONVERT_TO_FAT"]
                        / analysis.c["inputs"]['NUTRITION']['FAT_DAILY'],
                        marker='x',
                        markersize=6,
                        color='green',
                        linestyle='dashed')

                ax.set_ylabel('Fraction of minimum recommendation')
                ax.set_ylim([1.6, 2.9])


            if(label == 'c'):
                # ax.legend(loc='center left', frameon=False,bbox_to_anchor=(0, -0.2), shadow=False,)
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                plt.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.5),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels))

            if(label == 'd'):
                ax.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=['Calories',
                            'Fat',
                            'Protein'])
                ax.set_ylim([0.8, 1.3])

            if(label == 'a'):
                maxy = max(sum([x[0:xlim1] for x in ykcals]))
                ax.set_ylim([0, maxy / analysis.c["CONVERT_TO_KCALS"]])
            if(label == 'c'):
                maxy = max(sum([x[0:xlim2] for x in ykcals]))
                ax.set_ylim([0, maxy / analysis.c["CONVERT_TO_KCALS"]])


            plt.xlabel('Months since May ASRS')

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_fig_s4abcd(analysis1,
                        analysis2,
                        xlim):
        legend = Plotter.get_people_fed_legend(analysis1)
        fig = plt.figure()
        pal = ["#1e7ecd",
               "#71797E",
               "#76d7ea",
               "#056608",
               "#fdfff5",
               "#f9906f",
               "#a5d610",
               "#ffeb7a",
               "#e7d2ad"]

        for i, label in enumerate(('a', 'b', 'c', 'd')):
            if(label == 'a'):
                analysis = analysis1
            if(label == 'b'):
                analysis = analysis1
            if(label == 'c'):
                analysis = analysis2
            if(label == 'd'):
                analysis = analysis2
            ax = fig.add_subplot(2, 2, i + 1)
            ax.set_xlim([0.5, xlim])
            if(label == 'a'):
                plt.title('Food availability before ASRS')
            if(label == 'b'):
                plt.title('Available food macronutrition')
            if(label == 'c'):
                plt.title("Diet composition")
            if(label == 'd'):
                plt.title("Diet macronutrition")
            if(label == 'a' or label == 'c'):

                ykcals = []
                ykcals.append(analysis.billions_fed_fish_kcals)
                ykcals.append((np.array(analysis.billions_fed_CS_kcals) +
                               np.array(analysis.billions_fed_SCP_kcals)))
                ykcals.append(analysis.billions_fed_GH_kcals)
                ykcals.append(analysis.billions_fed_seaweed_kcals)
                ykcals.append((analysis.billions_fed_milk_kcals +
                               analysis.billions_fed_h_e_milk_kcals))
                ykcals.append((analysis.billions_fed_meat_kcals +
                               analysis.billions_fed_h_e_meat_kcals))
                ykcals.append(analysis.billions_fed_immediate_OG_kcals)
                ykcals.append(analysis.billions_fed_new_stored_OG_kcals)
                ykcals.append(analysis.billions_fed_SF_kcals)

                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                ax.stackplot(analysis.time_months_middle,
                             np.array(ykcals)
                             / analysis.c["CONVERT_TO_KCALS"],
                             labels=legend, colors=pal)

                # get the sum of all the ydata up to xlim month,
                # then find max month
                maxy = max(sum([x[0:xlim] for x in ykcals]))
                ax.set_ylim([0, maxy/ analysis.c["CONVERT_TO_KCALS"]])

                plt.ylabel('Calories / capita / day')
            if(label == 'b' or label == 'd'):
                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                plt.xlabel('Months since May ASRS onset')

                ax.plot(analysis.time_months_middle,
                        analysis.kcals_fed / analysis.c["CONVERT_TO_KCALS"]
                        / analysis.c["inputs"]['NUTRITION']['KCALS_DAILY'],
                        marker='o',
                        markersize=6,
                        color='blue',
                        linestyle='solid')

                ax.plot(analysis.time_months_middle,
                        analysis.protein_fed / analysis.c["CONVERT_TO_PROTEIN"]
                        / analysis.c["inputs"]['NUTRITION']['PROTEIN_DAILY'],
                        marker='^',
                        markersize=6,
                        color='red',
                        linestyle='dotted')

                ax.plot(analysis.time_months_middle,
                        analysis.fat_fed / analysis.c["CONVERT_TO_FAT"]
                        / analysis.c["inputs"]['NUTRITION']['FAT_DAILY'],
                        marker='x',
                        markersize=6,
                        color='green',
                        linestyle='dashed')

                ax.set_ylabel('Fraction of minimum recommendation')
                ax.set_ylim([2, 3])


            if(label == 'c'):
                # ax.legend(loc='center left', frameon=False,bbox_to_anchor=(0, -0.2), shadow=False,)
                # get the handles
                handles, labels = ax.get_legend_handles_labels()
                plt.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.15, -0.5),
                    shadow=False,
                    handles=reversed(handles),
                    labels=reversed(labels))

            if(label == 'd'):
                ax.legend(
                    loc='center left',
                    frameon=False,
                    bbox_to_anchor=(-0.05, -0.3),
                    shadow=False,
                    labels=['Calories',
                            'Fat',
                            'Protein'])
                ax.set_ylim([0.95, 1.05])

            plt.xlabel('Months since May')

        fig.set_figheight(12)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_people_fed_kcals(analysis, title, xlim):

        font = {'family': 'normal',
                'weight': 'bold',
                'size': 16}

        plt.rcParams["figure.figsize"] = [17.50, 9]
        matplotlib.rc('font', **font)
        plt.close()
        plt.figure()
        ax = plt.subplot(111)
        legend = []

        patterns = ["/", "\\", "|", "-", "+", "x", "o", "O"]
        pal = ["#006ddb", "#b66dff", "6db6ff", "#b6dbff",
               "#920000", "#924900", "#db6d00", "#24ff24", "#ffff6d"]

        legend = Plotter.get_people_fed_legend(analysis)

        # https://jacksonlab.agronomy.wisc.edu/2016/05/23/15-level-colorblind-friendly-palette/
        #   "#000000","#004949","#009292","#ff6db6","#ffb6db",
        # "#490092","#006ddb","#b66dff","#6db6ff","#b6dbff",
        # "#920000","#924900","#db6d00","#24ff24","#ffff6d"
        # patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]

        # print(analysis.billions_fed_h_e_meat_kcals)
        ydata = []
        ydata.append(analysis.billions_fed_fish_kcals /
                     analysis.c["CONVERT_TO_KCALS"])
        ydata.append((np.array(analysis.billions_fed_CS_kcals) +
                      np.array(analysis.billions_fed_SCP_kcals)) /
                     analysis.c["CONVERT_TO_KCALS"])
        ydata.append(analysis.billions_fed_GH_kcals /
                     analysis.c["CONVERT_TO_KCALS"])
        ydata.append(analysis.billions_fed_seaweed_kcals /
                     analysis.c["CONVERT_TO_KCALS"])
        ydata.append((analysis.billions_fed_milk_kcals +
                      analysis.billions_fed_h_e_milk_kcals) /
                     analysis.c["CONVERT_TO_KCALS"])
        ydata.append((analysis.billions_fed_meat_kcals +
                      analysis.billions_fed_h_e_meat_kcals) / analysis.c["CONVERT_TO_KCALS"])
        ydata.append(analysis.billions_fed_immediate_OG_kcals /
                     analysis.c["CONVERT_TO_KCALS"])
        ydata.append(analysis.billions_fed_new_stored_OG_kcals /
                     analysis.c["CONVERT_TO_KCALS"])
        ydata.append(analysis.billions_fed_SF_kcals /
                     analysis.c["CONVERT_TO_KCALS"])

        stacks = ax.stackplot(analysis.time_months_middle,
                              ydata,
                              labels=legend,
                              colors=pal)
        for stack, hatch in zip(stacks, patterns):
            stack.set_hatch(hatch)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.695, box.height])
        handles, labels = ax.get_legend_handles_labels()  # get the handles
        ax.legend()
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                  handles=reversed(handles), labels=reversed(labels))
        # plt.title('Caloric Availability, Nuclear Winter, No Resilient Foods')
        plt.title(title)
        plt.ylabel('Calories per capita per day')

        if(not analysis.c['inputs']['IS_NUCLEAR_WINTER']):
            plt.xlabel('Months since May, baseline around 2020')
        else:
            plt.xlabel('Months since May ASRS onset')

        ax.set_xlim([0, xlim])

        # sometimes values later than month 70 are nonsense
        # get the sum of all the ydata up to month 70, then find max month
        maxy = max(sum([x[0:70] for x in ydata]))
        ax.set_ylim([0, maxy])

        plt.rcParams["figure.figsize"] = [17.50, 9]
        plt.tight_layout()
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()

    def plot_histogram(ax, data, N, xlabel, ylabel, title):
        num_bins = int(N / 10)
        # plt.title("Food Available After Delayed Shutoff and Waste ")
        # ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.hist(data, bins=num_bins, facecolor='blue', alpha=0.5)
        ax.set_xlabel(xlabel)
        # ax.set_title(title)
        # ax.set_ylabel()

    def plot_histogram_with_boxplot(data, N, xlabel, title):
        print("data")
        print(data)
        # https://www.python-graph-gallery.com/24-histogram-with-a-boxplot-on-top-seaborn
        # set a grey background (use sns.set_theme() if seaborn
        # version 0.11.0 or above)
        sns.set(style="darkgrid")

        # creating a figure composed of two matplotlib.Axes objects
        # (ax_box and ax_hist)
        f, (ax_box, ax_hist) = plt.subplots(2,
                                            sharex=True,
                                            gridspec_kw={"height_ratios":
                                                         (.15, .85)})

        # assigning a graph to each ax
        sns.boxplot(data, ax=ax_box, showfliers=True)
        sns.histplot(data=data, ax=ax_hist)

        # Remove x axis name for the boxplot
        ax_hist.set(xlabel=xlabel)
        ax_box.set(title=title)
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()
        print("95% lower")
        print(np.percentile(np.array(data), 2.5))
        print("95% upper")
        print(np.percentile(np.array(data), 97.5))

    def get_people_fed_legend(analysis):
        if(not analysis.c['inputs']['IS_NUCLEAR_WINTER']):
            stored_food_label = 'Crops consumed that month that were\nstored before simulation'
            OG_stored_label = 'Crops consumed that month that were\nstored after simulation start'
        else:
            stored_food_label = 'Crops consumed that month that were\nstored before ASRS onset'
            OG_stored_label = 'Crops consumed that month that were\nstored after ASRS onset'

        legend = []
        if(analysis.c['ADD_FISH']):
            legend = legend + ['Marine Fish']
        else:
            legend = legend + ['']

        if(analysis.c['ADD_CELLULOSIC_SUGAR'] or analysis.c['ADD_METHANE_SCP']):
            legend = legend + ['Industrial Foods']
        else:
            legend = legend + ['']

        if(analysis.c['ADD_GREENHOUSES']):
            legend = legend + ['Greenhouses']
        else:
            legend = legend + ['']

        if(analysis.c['ADD_SEAWEED']):
            legend = legend + ['Seaweed']
        else:
            legend = legend + ['']

        if(analysis.c['ADD_DAIRY']):
            legend = legend + ['Dairy Milk']
        else:
            legend = legend + ['']

        if(analysis.c['ADD_MEAT']):
            legend = legend + ['Meat']
        else:
            legend = legend + ['']

        if(analysis.c['ADD_OUTDOOR_GROWING']):
            legend = legend + [
                'Outdoor Crops consumed immediately']
        else:
            legend = legend + ['']

        if(analysis.c['ADD_OUTDOOR_GROWING']):
            legend = legend + [OG_stored_label]
        else:
            legend = legend + ['']

        if(analysis.c['ADD_STORED_FOOD']):
            legend = legend + [stored_food_label]
        else:
            legend = legend + ['']

        return legend

    def plot_people_fed_comparison(analysis):

        ls_cycler = cycler('linestyle',
                           [
                               (0, ()),  # solid
                               (0, ()),  # solid
                               (0, ()),  # solid
                               (0, (1, 1)),  # densely dotted
                               (0, (1, 1)),  # densely dotted
                               (0, (1, 1))  # densely dotted
                           ]
                           )

        color_cycler = cycler('color', [plt.get_cmap('viridis')(
            np.floor(i % 3)/3) for i in np.arange(len(ls_cycler))])

        new_cycler = color_cycler + ls_cycler
        plt.rc('axes', prop_cycle=new_cycler)
        title = "Population Fed Existing vs New Resilient Foods"
        plt.title(title)
        plt.plot(analysis.time_months_middle,
                 np.array(analysis.billions_fed_SF_kcals)
                 + np.array(analysis.billions_fed_meat_kcals)
                 + np.array(analysis.billions_fed_milk_kcals)
                 # +np.array(analysis.billions_fed_dairy_meat_kcals)
                 + np.array(analysis.billions_fed_OG_kcals), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle,
                 np.array(analysis.billions_fed_SF_fat)
                 + np.array(analysis.billions_fed_meat_fat)
                 + np.array(analysis.billions_fed_milk_fat)
                 # +np.array(analysis.billions_fed_dairy_meat_kcals)
                 + np.array(analysis.billions_fed_OG_fat), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle,
                 np.array(analysis.billions_fed_SF_protein)
                 + np.array(analysis.billions_fed_meat_protein)
                 + np.array(analysis.billions_fed_milk_protein)
                 # +np.array(analysis.billions_fed_dairy_meat_kcals)
                 + np.array(analysis.billions_fed_OG_fat), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle,
                 +np.array(analysis.billions_fed_seaweed_kcals)
                 + np.array(analysis.billions_fed_CS_kcals)
                 + np.array(analysis.billions_fed_GH_kcals), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle,
                 +np.array(analysis.billions_fed_seaweed_fat)
                 + np.array(analysis.billions_fed_GH_fat), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle,
                 +np.array(analysis.billions_fed_seaweed_protein)
                 + np.array(analysis.billions_fed_GH_protein), marker='o', markersize=3)

        legend = [
            'if added, Dairy+Meat+SF+OG, kcals',
            'if added, Dairy+Meat+SF+OG, fat',
            'if added, Dairy+Meat+SF+OG, protein',
            'if added, Seaweed+CS+GH, kcals',
            'if added, Seaweed+CS+GH, fat',
            'if added, Seaweed+CS+GH, protein'
        ]
        plt.ylabel('billions of people')
        plt.xlabel('Months since May ASRS onset')
        plt.legend(legend)

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        # os.system('firefox-esr plot.svg')
        plt.show()
