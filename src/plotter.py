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
matplotlib.use('Svg')
# matplotlib.use('QtAgg')


class Plotter:
    def __init__(self):
        pass

    def plot_stored_food(analysis):
        ls_cycler = cycler('linestyle',
                           [
                               (0, ()),  # solid
                               (0, (1, 1)),  # densely dotted
                               (0, (1, 5))  # dotted
                           ]
                           )

        color_cycler = cycler('color', [plt.get_cmap('viridis')(i/3) for i in np.arange(3)])

        new_cycler = color_cycler + ls_cycler
        plt.rc('axes', prop_cycle=new_cycler)

        plt.plot(analysis.time_months_middle, np.array(analysis.billions_fed_SF_kcals))
        plt.plot(analysis.time_months_middle, np.array(analysis.billions_fed_SF_fat))
        plt.plot(analysis.time_months_middle, np.array(analysis.billions_fed_SF_protein))
        plt.title('Stored Food')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Billion Person-Years')
        plt.legend(['kcals available', 'fat available', 'protein available'])

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_CS(analysis):
        ls_cycler = cycler('linestyle',
                           [
                               (0, ())  # solid
                               # (0, (1, 1)), # densely dotted
                               # (0, (1, 5)) # dotted
                           ]
                           )

        color_cycler = cycler('color', [plt.get_cmap('viridis')(i)
                                        for i in np.arange(len(ls_cycler))])

        new_cycler = color_cycler + ls_cycler
        plt.rc('axes', prop_cycle=new_cycler)

        plt.plot(analysis.time_months_middle, np.array(
            analysis.billions_fed_CS_kcals), marker='o', markersize=3)
        plt.title('Industrial Foods')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Billions fed from CS')

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_fish(analysis):
        ls_cycler = cycler('linestyle',
                           [
                               (0, ()),  # solid
                               (0, (1, 1)),  # densely dotted
                               (0, (1, 5))  # dotted
                           ]
                           )

        color_cycler = cycler('color', [plt.get_cmap('viridis')(i)
                                        for i in np.arange(len(ls_cycler))])

        new_cycler = color_cycler + ls_cycler
        plt.rc('axes', prop_cycle=new_cycler)

        plt.plot(analysis.time_months_middle, analysis.billions_fed_fish_kcals, marker='o', markersize=3)
        plt.plot(analysis.time_months_middle, analysis.billions_fed_fish_fat, marker='o', markersize=3)
        plt.plot(analysis.time_months_middle, analysis.billions_fed_fish_protein, marker='o', markersize=3)
        plt.legend(['kcals available', 'fat available', 'protein available'])

        plt.title('Fish')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Billions fed from fish')

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_GH(analysis):
        ls_cycler = cycler('linestyle',
                           [
                               (0, ()),  # solid
                               (0, (1, 1)),  # densely dotted
                               (0, (1, 5))  # dotted
                           ]
                           )

        color_cycler = cycler('color', [plt.get_cmap('viridis')(i)
                                        for i in np.arange(len(ls_cycler))])

        new_cycler = color_cycler + ls_cycler
        plt.rc('axes', prop_cycle=new_cycler)

        plt.plot(analysis.time_months_middle, np.array(
            analysis.billions_fed_GH_kcals), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle, np.array(
            analysis.billions_fed_GH_fat), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle, np.array(
            analysis.billions_fed_GH_protein), marker='o', markersize=3)
        plt.title('Greenhouses')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Billions Fed from Greenhouses')
        plt.legend(['kcals available', 'fat available', 'protein available'])

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_OG_with_resilient_foods(analysis):
        # ls_cycler = cycler('linestyle',
        #                   [\
        #                    (0,()), # solid
        #                    (0, (1, 1)), # densely dotted
        #                    (0, (1, 5)) # dotted
        #                    ]
        #                 )

        # color_cycler = cycler('color', [plt.get_cmap('viridis')(i) for i in np.arange(len(ls_cycler))] )

        # new_cycler = color_cycler + ls_cycler
        # plt.rc('axes',prop_cycle=new_cycler)
        plt.title('Outdoor Growing, Resilient Foods Deployment')
        plt.xlabel('Months since May ASRS')

        ax = plt.gca()
        ax2 = ax.twinx()

        ax.plot(analysis.time_months_middle,
                np.array(analysis.billions_fed_OG_produced_kcals),
                marker='o',
                markersize=3,
                color='green',
                linestyle='solid')
        ax.set_ylabel('Calories per capita per day')
        ax.legend(['kcals available', 'fat available', 'protein available'], loc=2)
        # ax2.set_x(['kcals available'])

        ax2.plot(analysis.time_months_middle, np.array(analysis.
                                              billions_fed_OG_produced_fat), marker='o', markersize=3, color='red', linestyle='dashed')
        ax2.plot(analysis.time_months_middle, np.array(analysis.
                                              billions_fed_OG_produced_protein), marker='o', markersize=3, color='blue', linestyle='dotted')
        ax2.set_ylabel('Grams per capita per day')
        ax2.set_ylim([0, 50])
        ax.legend(['fat available', 'protein available'], loc=1)

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_OG_before_nuclear_event(analysis):
        plt.title('Outdoor Growing, 2020 Baseline')
        plt.xlabel('Months since May')

        ax = plt.gca()
        ax2 = ax.twinx()

        ax.plot(analysis.time_months_middle, np.array(analysis.
                                             billions_fed_OG_produced_kcals), marker='o', markersize=3, color='green', linestyle='solid')
        ax.set_ylabel('Calories per capita per day')
        # ax2.set_x(['kcals available'])

        ax.plot(analysis.time_months_middle, np.array(analysis.
                                             billions_fed_OG_produced_fat), marker='o', markersize=3, color='red', linestyle='dashed')
        ax.plot(analysis.time_months_middle, np.array(analysis.
                                             billions_fed_OG_produced_protein), marker='o', markersize=3, color='blue', linestyle='dotted')
        # ax2.set_ylabel('Grams per capita per day')
        # ax2.set_ylim([0,50])
        # ax2.legend(['fat available','protein available'],loc=1)
        ax.legend(['kcals available', 'fat available', 'protein available'], loc=2)

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_OG_no_resilient_foods(analysis):
        plt.title('Outdoor Growing, No Resilient Foods Deployment')
        plt.xlabel('Months since May')

        ax = plt.gca()
        ax2 = ax.twinx()

        ax.plot(analysis.time_months_middle, np.array(analysis.
                                             billions_fed_OG_produced_kcals), marker='o', markersize=3, color='green', linestyle='solid')
        ax.set_ylabel('Calories per capita per day')
        # ax2.set_x(['kcals available'])

        ax.plot(analysis.time_months_middle, np.array(analysis.
                                             billions_fed_OG_produced_fat), marker='o', markersize=3, color='red', linestyle='dashed')
        ax.plot(analysis.time_months_middle, np.array(analysis.
                                             billions_fed_OG_produced_protein), marker='o', markersize=3, color='blue', linestyle='dotted')
        ax.legend(['kcals available', 'fat available', 'protein available'], loc=2)

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_meat(analysis):

        plt.plot(analysis.time_months_middle, np.array(analysis.billions_fed_meat_kcals))
        plt.plot(analysis.time_months_middle, np.array(analysis.billions_fed_meat_fat))
        plt.plot(analysis.time_months_middle, np.array(analysis.billions_fed_meat_protein))
        plt.title('Meat')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Billion Person-Years')
        plt.legend(['kcals available', 'fat available', 'protein available'])

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_dairy_cows(analysis):
        plt.plot(analysis.time_months_middle, np.array(
            analysis.millions_dairy_animals_midmonth), marker='o', markersize=3)
        plt.title('Millions of Dairy Animals')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Livestock Population, Millions')

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_dairy(time_months, analysis):
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

        plt.plot(time_months, np.array(analysis.billions_fed_milk_kcals))
        plt.plot(time_months, np.array(analysis.billions_fed_milk_fat))
        plt.plot(time_months, np.array(analysis.billions_fed_milk_protein))
        # plt.plot(time_months,np.array(analysis.billions_fed_dairy_meat_kcals))
        # plt.plot(time_months,np.array(analysis.billions_fed_dairy_meat_fat))
        # plt.plot(time_months,np.array(analysis.billions_fed_dairy_meat_protein))
        plt.title('Billions Fed from Milk and Eating Dairy Animals')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Billion Person-Years')
        plt.legend([
            'kcals available, milk',
            'fat available, milk',
            'protein available, milk',
            'kcals available, dairy cow meat',
            'fat available, dairy cow meat',
            'protein available, dairy cow meat'])

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

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

    def plot_all_histograms(variables, N):
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
        os.system('firefox-esr plot.svg')

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
        os.system('firefox-esr plot.svg')

    def plot_fig_1ab(analysis1, analysis2, xlim):
        legend = Plotter.get_people_fed_legend(analysis1)
        fig = plt.figure()
        pal = ["#006ddb", "#b66dff", "6db6ff", "#b6dbff",
               "#920000", "#924900", "#db6d00", "#24ff24", "#ffff6d"]
        for i, label in enumerate(('a', 'b')):
            if(label == 'a'):
                analysis = analysis1
            if(label == 'b'):
                analysis = analysis2
            ax = fig.add_subplot(2, 1, i+1)
            ax.set_xlim([0.5, xlim])
            ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                    fontsize=11, fontweight='bold', va='top', ha='right')
            ax.stackplot(analysis.time_months_middle,
                         analysis.billions_fed_fish_kcals /
                         analysis.c["CONVERT_TO_KCALS"],
                         (np.array(analysis.billions_fed_CS_kcals) +
                         np.array(analysis.billions_fed_SCP_kcals)) / analysis.c["CONVERT_TO_KCALS"],
                         analysis.billions_fed_GH_kcals /
                         analysis.c["CONVERT_TO_KCALS"],
                         analysis.billions_fed_seaweed_kcals /
                         analysis.c["CONVERT_TO_KCALS"],
                         (analysis.billions_fed_milk_kcals +
                          analysis.billions_fed_h_e_milk_kcals)
                         / analysis.c["CONVERT_TO_KCALS"],
                         (analysis.billions_fed_meat_kcals
                          + analysis.billions_fed_h_e_meat_kcals) /
                         analysis.c["CONVERT_TO_KCALS"],
                         analysis.billions_fed_immediate_OG_kcals /
                         analysis.c["CONVERT_TO_KCALS"],
                         analysis.billions_fed_new_stored_OG_kcals /
                         analysis.c["CONVERT_TO_KCALS"],
                         analysis.billions_fed_SF_kcals /
                         analysis.c["CONVERT_TO_KCALS"],
                         labels=legend, colors=pal)
            ax.set_ylim([0, analysis.people_fed_billions
                        / analysis.c["CONVERT_TO_KCALS"]])
            if(label == 'b'):
                # ax.legend(loc='center left', frameon=False,bbox_to_anchor=(0, -0.2), shadow=False,)
                handles, labels = ax.get_legend_handles_labels()  # get the handles
            plt.ylabel('Calories / capita / day')
            plt.xlabel('Months since May ASRS onset')

        ax.legend(loc='center left', frameon=False, bbox_to_anchor=(0, -0.5),
                  shadow=False, handles=reversed(handles), labels=reversed(labels))
        # plt.rcParams["figure.figsize"] = [12.50, 10]

        fig.set_figheight(10)
        fig.set_figwidth(8)
        plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_figure_2ab(analysis1, xlim):
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
        os.system('firefox-esr plot.svg')

    def plot_figure_supplement_before_catastrophe_abcd(analysis1,
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
        os.system('firefox-esr plot.svg')


    def plot_figure_supplement_primary_production_abcd(analysis1,
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
        os.system('firefox-esr plot.svg')

    def plot_fig_1abcd(analysis1, analysis2, xlim):
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
        os.system('firefox-esr plot.svg')

    def plot_fig_3(data, analyses, xlim):
        legend = Plotter.get_people_fed_legend(analysis1)
        fig = plt.figure()
        pal = ["#006ddb", "#b66dff", "6db6ff", "#b6dbff",
               "#920000", "#924900", "#db6d00", "#24ff24", "#ffff6d"]
        plt.rcParams["figure.figsize"] = [10, 8]
        for i, label in enumerate(('a', 'b')):
            if(label == 'a'):
                analysis = analysis1
            if(label == 'b'):
                analysis = analysis1
            if(label == 'c'):
                analysis = analysis2
                # plt.title('Resilient foods diet')
            if(label == 'd'):
                analysis = analysis2
            ax = fig.add_subplot(2, 2, i+1)
            ax.set_xlim([0.5, xlim])
            if(label == 'a' or label == 'c'):

                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                stacks = ax.stackplot(analysis.time_months_middle,
                                      analysis.billions_fed_fish_kcals /
                                      analysis.c["CONVERT_TO_KCALS"],
                                      (np.array(analysis.billions_fed_CS_kcals) +
                                       np.array(analysis.billions_fed_SCP_kcals)) / analysis.c["CONVERT_TO_KCALS"],
                                      analysis.billions_fed_GH_kcals /
                                      analysis.c["CONVERT_TO_KCALS"],
                                      analysis.billions_fed_seaweed_kcals /
                                      analysis.c["CONVERT_TO_KCALS"],
                                      (analysis.billions_fed_milk_kcals +
                                       analysis.billions_fed_h_e_milk_kcals) / analysis.c["CONVERT_TO_KCALS"],
                                      (analysis.billions_fed_meat_kcals+analysis.billions_fed_h_e_meat_kcals) /
                                      analysis.c["CONVERT_TO_KCALS"],
                                      analysis.billions_fed_immediate_OG_kcals /
                                      analysis.c["CONVERT_TO_KCALS"],
                                      analysis.billions_fed_new_stored_OG_kcals /
                                      analysis.c["CONVERT_TO_KCALS"],
                                      analysis.billions_fed_SF_kcals /
                                      analysis.c["CONVERT_TO_KCALS"],
                                      labels=legend, colors=pal)
                ax.set_ylim([0, (analysis.people_fed_billions) /
                             analysis.c["CONVERT_TO_KCALS"]])
                plt.ylabel('Calories / capita / day')
            if(label == 'b' or label == 'd'):
                ax.text(-0.06, 1.1, label, transform=ax.transAxes,
                        fontsize=11, fontweight='bold', va='top', ha='right')
                plt.xlabel('Months since May ASRS onset')

                ax2 = ax.twinx()
                ax.plot(analysis.time_months_middle,
                        np.array(analysis.billions_fed_SF_kcals /
                                 analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_meat_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_seaweed_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_milk_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_CS_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_SCP_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_GH_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_OG_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + np.array(analysis.billions_fed_fish_kcals /
                                   analysis.c["CONVERT_TO_KCALS"])
                        + analysis.billions_fed_h_e_meat_kcals /
                        analysis.c["CONVERT_TO_KCALS"]
                        + analysis.billions_fed_h_e_milk_kcals /
                        analysis.c["CONVERT_TO_KCALS"], marker='o', markersize=6, color='blue', linestyle='solid')
                ax.plot(np.linspace(analysis.c["inputs"]['NUTRITION']['KCALS_DAILY'], analysis.c["inputs"]['NUTRITION']['KCALS_DAILY'], len(
                    analysis.time_months_middle)), color='lightblue', markersize=6, marker='o', linestyle='dashed')
                ax2.plot(analysis.time_months_middle,
                         np.array(analysis.billions_fed_SF_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + np.array(analysis.billions_fed_meat_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + np.array(analysis.billions_fed_seaweed_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + np.array(analysis.billions_fed_milk_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + np.array(analysis.billions_fed_SCP_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + np.array(analysis.billions_fed_GH_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + np.array(analysis.billions_fed_OG_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + np.array(analysis.billions_fed_fish_protein) /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + analysis.billions_fed_h_e_meat_protein /
                         analysis.c["CONVERT_TO_PROTEIN"]
                         + analysis.billions_fed_h_e_milk_protein / analysis.c["CONVERT_TO_PROTEIN"], marker='^', markersize=6, color='red', linestyle='dotted')

                ax2.plot(np.linspace(analysis.c["inputs"]['NUTRITION']['PROTEIN_DAILY'], analysis.c["inputs"]['NUTRITION']['PROTEIN_DAILY'], len(
                    analysis.time_months_middle)), color='indianred', marker='^', linestyle='dashed', markersize=6)
                ax2.plot(analysis.time_months_middle,
                         np.array(analysis.billions_fed_SF_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + np.array(analysis.billions_fed_meat_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + np.array(analysis.billions_fed_seaweed_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + np.array(analysis.billions_fed_milk_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + np.array(analysis.billions_fed_SCP_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + np.array(analysis.billions_fed_GH_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + np.array(analysis.billions_fed_OG_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + np.array(analysis.billions_fed_fish_fat) /
                         analysis.c["CONVERT_TO_FAT"]
                         + analysis.billions_fed_h_e_meat_fat / analysis.c["CONVERT_TO_FAT"]
                         + analysis.billions_fed_h_e_milk_fat / analysis.c["CONVERT_TO_FAT"], marker='x', markersize=6, color='green', linestyle='dashed')
                ax2.plot(np.linspace(analysis.c["inputs"]['NUTRITION']['FAT_DAILY'], analysis.c["inputs"]['NUTRITION']['FAT_DAILY'], len(
                    analysis.time_months_middle)), color='lightgreen', markersize=6, marker='x', linestyle='dashed')

                ax.set_ylabel('Calories / capita / day')
                ax2.set_ylabel('Grams / capita / day')

                ax.set_ylim([2000, 4000])
                ax2.set_ylim([0, 100])

            if(label == 'c'):
                # ax.legend(loc='center left', frameon=False,bbox_to_anchor=(0, -0.2), shadow=False,)
                handles, labels = ax.get_legend_handles_labels()  # get the handles
                plt.legend(loc='center left', frameon=False, bbox_to_anchor=(-0.15, -0.7),
                           shadow=False, handles=reversed(handles), labels=reversed(labels))

            if(label == 'd'):
                ax.legend(loc='center left', frameon=False, bbox_to_anchor=(
                    0.13, -0.4), shadow=False, labels=['scenario calories', 'minimum recommended calories'])
                ax2.legend(loc='center left', frameon=False, bbox_to_anchor=(0.13, -0.7), shadow=False, labels=[
                           'scenario fat', 'minimum recommended fat, caloric equivalent', 'scenario protein, caloric equivalent', 'minimum recommended protein, caloric equivalent'])
            if(label == 'a'):
                plt.title("Resilient foods availability")
            if(label == 'b'):
                plt.title("Resilient foods macronutrition")
            if(label == 'c'):
                plt.title("Resulting human diet composition")
            if(label == 'd'):
                plt.title("Resulting human diet macronutrition")

            plt.xlabel('Months since May ASRS onset')

        fig.set_figheight(10)
        fig.set_figwidth(8)
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_people_fed_kcals_before_nuclear_event(analysis, title):

        font = {'family': 'normal',
                'weight': 'bold',
                'size': 16}

        matplotlib.rc('font', **font)
        fig = plt.figure()
        ax = plt.subplot(111)
        # https://jacksonlab.agronomy.wisc.edu/2016/05/23/15-level-colorblind-friendly-palette/
        #   "#000000","#004949","#009292","#ff6db6","#ffb6db",
        # "#490092","#006ddb","#b66dff","#6db6ff","#b6dbff",
        # "#920000","#924900","#db6d00","#24ff24","#ffff6d"
        # patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
        patterns = ["/", "\\", "|", "-", "+", "x", "o", "O"]
        pal = ["#006ddb", "#b66dff", "6db6ff", "#b6dbff",
               "#920000", "#924900", "#db6d00", "#24ff24", "#ffff6d"]

        stacks = ax.stackplot(analysis.time_months_middle,
                              analysis.billions_fed_fish_kcals/analysis.c["CONVERT_TO_KCALS"],
                              analysis.billions_fed_immediate_OG_kcals /
                              analysis.c["CONVERT_TO_KCALS"],
                              analysis.billions_fed_new_stored_OG_kcals /
                              analysis.c["CONVERT_TO_KCALS"],
                              analysis.billions_fed_SF_kcals/analysis.c["CONVERT_TO_KCALS"],
                              (analysis.billions_fed_milk_kcals
                               + analysis.billions_fed_h_e_milk_kcals)/analysis.c["CONVERT_TO_KCALS"],
                              (np.array(analysis.billions_fed_meat_kcals)
                               + analysis.billions_fed_h_e_meat_kcals)/analysis.c["CONVERT_TO_KCALS"],
                              analysis.billions_fed_GH_kcals/analysis.c["CONVERT_TO_KCALS"],
                              analysis.billions_fed_seaweed_kcals /
                              analysis.c["CONVERT_TO_KCALS"],
                              (np.array(analysis.billions_fed_CS_kcals) +
                                  np.array(analysis.billions_fed_SCP_kcals))/analysis.c["CONVERT_TO_KCALS"],
                              labels=[
                                  'Marine Fish',
                                  'Crops consumed \n immediately',
                                  'Crops consumed that month \n that were stored \n after simulation',
                                  'Crops consumed that month \n that were stored \n before simulation',
                                  'Dairy Milk',
                              ], colors=pal)
        for stack, hatch in zip(stacks, patterns):
            stack.set_hatch(hatch)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.695, box.height])
        handles, labels = ax.get_legend_handles_labels()  # get the handles
        ax.legend()
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                  handles=reversed(handles), labels=reversed(labels))
        plt.title('Primary Caloric Monthly Sources, Present-Day')
        plt.ylabel('Calories per capita per day')
        plt.xlabel('Months since May ASRS onset')
        # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
        #   ncol=3, fancybox=True, shadow=True)
        ax.set_xlim([0, 48])
        ax.set_ylim([0, (analysis.billions_fed_immediate_OG_kcals[-1]
                         + analysis.billions_fed_new_stored_OG_kcals[-1]
                         + analysis.billions_fed_SF_kcals[-1]
                         + analysis.billions_fed_fish_kcals[-1]
                         + analysis.billions_fed_milk_kcals[-1]
                         + analysis.billions_fed_meat_kcals[-1]
                         + analysis.billions_fed_h_e_milk_kcals[-1]
                         + analysis.billions_fed_h_e_meat_kcals[-1]
                         + analysis.billions_fed_GH_kcals[-1]
                         + analysis.billions_fed_seaweed_kcals[-1]
                         + analysis.billions_fed_CS_kcals[-1]
                         + analysis.billions_fed_SCP_kcals[-1])/analysis.c["CONVERT_TO_KCALS"]])

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    def plot_people_fed_combined(analysis):
        fig = plt.figure()
        ax = plt.subplot(111)
        title = "Population Fed"
        plt.title(title)
        plt.xlabel('Months since May ASRS onset')

        ax = plt.gca()
        ax.plot(analysis.time_months_middle,
                np.array(analysis.billions_fed_SF_kcals /
                         analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_meat_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_seaweed_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_milk_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_CS_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_SCP_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_GH_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_OG_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + np.array(analysis.billions_fed_fish_kcals /
                           analysis.c["CONVERT_TO_KCALS"])
                + analysis.billions_fed_h_e_meat_kcals /
                analysis.c["CONVERT_TO_KCALS"]
                + analysis.billions_fed_h_e_milk_kcals /
                analysis.c["CONVERT_TO_KCALS"], marker='o', markersize=3, color='blue', linestyle='solid')
        ax.set_ylabel('Calories per capita per day')

        ax.plot(analysis.time_months_middle,
                np.array(analysis.billions_fed_SF_protein)
                + np.array(analysis.billions_fed_meat_protein)
                + np.array(analysis.billions_fed_seaweed_protein)
                + np.array(analysis.billions_fed_milk_protein)
                + np.array(analysis.billions_fed_SCP_protein)
                + np.array(analysis.billions_fed_GH_protein[0:len(analysis.time_months_middle)
                                                            ])
                + np.array(analysis.billions_fed_OG_protein)
                + np.array(analysis.billions_fed_fish_protein)
                + analysis.billions_fed_h_e_meat_protein
                + analysis.billions_fed_h_e_milk_protein, marker='o', markersize=3, color='red', linestyle='dotted')

        ax.plot(analysis.time_months_middle,
                np.array(analysis.billions_fed_SF_fat)
                + np.array(analysis.billions_fed_meat_fat)
                + np.array(analysis.billions_fed_seaweed_fat)
                + np.array(analysis.billions_fed_milk_fat)
                + np.array(analysis.billions_fed_SCP_fat)
                + np.array(analysis.billions_fed_GH_fat)
                + np.array(analysis.billions_fed_OG_fat)
                + np.array(analysis.billions_fed_fish_fat)
                + analysis.billions_fed_h_e_meat_fat
                + analysis.billions_fed_h_e_milk_fat, marker='o', markersize=3, color='green', linestyle='dashed')

        ax.legend(['kcals_available', 'protein available', 'fat available'], loc=1)

        plt.rcParams["figure.figsize"] = [17.50, 9]
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

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
        os.system('firefox-esr plot.svg')

    def plot_seaweed(analysis):
        ls_cycler = cycler('linestyle',
                           [
                               (0, ()),  # solid
                               (0, (1, 1)),  # densely dotted
                               (0, (1, 5))  # dotted
                           ]
                           )

        color_cycler = cycler('color', [plt.get_cmap('viridis')(i/3) for i in np.arange(3)])

        new_cycler = color_cycler + ls_cycler
        plt.rc('axes', prop_cycle=new_cycler)

        plt.plot(analysis.time_months_middle, np.array(
            analysis.billions_fed_seaweed_kcals), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle, np.array(
            analysis.billions_fed_seaweed_fat), marker='o', markersize=3)
        plt.plot(analysis.time_months_middle, np.array(
            analysis.billions_fed_seaweed_protein), marker='o', markersize=3)
        plt.title('Seaweed People Fed')
        plt.xlabel('Months since May ASRS')
        plt.ylabel('Billion People Fed by macronutrient')
        plt.legend(['kcals available', 'fat available', 'protein available'])

        plt.rcParams["figure.figsize"] = [17.50, 9]
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

    # plot comparison between Aron's Data and this model's data
    def plot_seaweed_comparison(time_days_daily, time_days_monthly, analysis):
        # aron's food produced data for each day
        food_spreadsheet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 102562183, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1878422073, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2225588498, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2572754922, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2919921347]

        # aron's wet on farm data for each day
        wet_on_farm_spreadsheet = [1000, 1100, 1210, 1331, 1464, 1611, 1772, 1949, 2144, 2358, 2594, 2853, 3138, 3452, 3797, 4177, 4595, 5054, 5560, 6116, 6727, 7400, 8140, 8954, 9850, 10835, 11918, 13110, 14421, 15863, 17449, 19194, 21114, 23225, 25548, 28102, 30913, 34004, 37404, 41145, 45259, 49785, 54764, 60240, 66264, 72890, 80180, 88197, 97017, 106719, 117391, 129130, 142043, 156247, 171872, 189059, 207965, 228762, 251638, 276801, 304482, 334930, 368423, 405265, 445792, 490371, 539408, 593349, 652683, 717952, 789747, 868722, 955594, 1051153, 1156269, 1271895, 1399085, 1538993, 1692893, 1862182, 2048400, 2253240, 2478564, 2726421, 2999063, 3298969, 3628866, 3991753, 3792289, 4171517, 4588669, 5047536, 5552290, 6107519, 6718271, 7390098, 8129107, 8942018, 9836220, 10819842, 11901826, 13092009, 14401210, 15841331, 17425464, 19168010, 21084811, 23193292, 25512621, 28063884, 30870272, 33957299, 37353029, 35493925, 39043318, 42947650, 47242415, 51966656, 57163322, 62879654, 69167619, 76084381, 83692820, 92062102, 101268312, 111395143, 122534657, 134788123, 148266935, 163093629, 179402992, 197343291, 217077620, 238785382, 262663920, 288930312, 317823343,
                                   349605677, 229643215, 252607536, 277868290, 305655119, 336220630, 369842693, 406826963, 447509659, 492260625, 541486687, 595635356, 655198892, 720718781, 792790659, 872069725, 959276697, 1055204367, 1160724804, 1276797284, 1404477013, 1544924714, 1699417185, 1869358904, 2056294794, 2261924274, 271172782, 298290061, 328119067, 360930973, 397024071, 436726478, 480399126, 528439038, 581282942, 639411236, 703352360, 773687596, 851056355, 936161991, 1029778190, 1132756009, 1246031610, 1370634771, 1507698248, 1658468072, 1824314880, 2006746368, 2207421004, 2428163105, 2670979415, 312702350, 343972585, 378369844, 416206828, 457827511, 503610262, 553971288, 609368417, 670305259, 737335785, 811069363, 892176299, 981393929, 1079533322, 1187486655, 1306235320, 1436858852, 1580544737, 1738599211, 1912459132, 2103705045, 2314075550, 2545483105, 2800031415, 3080034557, 354231918, 389655110, 428620621, 471482683, 518630951, 570494046, 627543451, 690297796, 759327576, 835260333, 918786367, 1010665003, 1111731504, 1222904654, 1345195119, 1479714631, 1627686094, 1790454704, 1969500174, 2166450192, 2383095211, 2621404732, 2883545205, 3171899726, 3489089698, 395761486]

        spreadsheet_days = np.linspace(
            0, len(wet_on_farm_spreadsheet), len(wet_on_farm_spreadsheet))

        max_seaweed = np.linspace(analysis.max_seaweed,
                                  analysis.max_seaweed,
                                  len(wet_on_farm_spreadsheet))

        plt.plot(spreadsheet_days, max_seaweed)
        plt.plot(time_days_daily, analysis.seaweed_built_area_max_density)
        plt.plot(time_days_daily, analysis.seaweed_used_area_max_density)
        plt.plot(spreadsheet_days, np.array(wet_on_farm_spreadsheet) / 1000)
        plt.plot(time_days_daily, analysis.seaweed_wet_on_farm)
        plt.legend([
            'Max Density times Max Area Seaweed',
            'Built Area times Max Density',
            'Used Area times Max Density',
            'Aron\'s Spreadsheet Wet on Farm Estimate',
            'Optimizer Estimate Wet On Farm'
        ])
        plt.title('Seaweed Wet, 1000s of tons')
        plt.xlabel('Days since May ASRS')
        plt.yscale('log')

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

        plt.plot(spreadsheet_days, np.array(food_spreadsheet).cumsum() /
                 1000*analysis.c["SEAWEED_KCALS"]/analysis.c["KCALS_MONTHLY"])
        plt.plot(time_days_daily, np.array(analysis.seaweed_food_produced_daily).cumsum()
                 * analysis.c["SEAWEED_KCALS"]/analysis.c["KCALS_MONTHLY"])
        legend = [
            'Aron\'s Spreadsheet Food Wet Harvest Estimate',
            'Optimizer Estimate Food Wet Harvest Estimate'
        ]

        plt.legend(legend)
        plt.xlabel('Days since May ASRS')
        plt.title('Cumulative Seaweed Harvest, 1000s Tons Wet')
        # plt.yscale('log')

        plt.rcParams["figure.figsize"] = [17.50, 9]
        # plt.tight_layout()
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')

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
        f, (ax_box, ax_hist) = plt.subplots(2, sharex=True,
                                            gridspec_kw={"height_ratios": (.15, .85)})

        # assigning a graph to each ax
        sns.boxplot(data, ax=ax_box, showfliers=False)
        sns.histplot(data=data, ax=ax_hist)

        # Remove x axis name for the boxplot
        ax_hist.set(xlabel=xlabel)
        ax_box.set(title=title)
        plt.savefig("plot.svg")
        os.system('firefox-esr plot.svg')
        print("95% lower")
        print(np.percentile(np.array(data), 2.5))
        print("95% upper")
        print(np.percentile(np.array(data), 97.5))

    def plot_fig_4ab(monte_carlo_data, food_names, removed, added):
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
                ax3.set(xlabel="Calories / capita / day")
                plt.ylabel('')
                handles, labels = ax3.get_legend_handles_labels()
                ax4.legend(handles, labels, frameon=False, bbox_to_anchor=(.8, .8))
                ax4.axis("off")
            if(label == 'b'):
                sns.boxplot(monte_carlo_data, ax=ax_box, showfliers=False)
                sns.histplot(data=monte_carlo_data, ax=ax_hist)
                ax_hist.set(xlabel="Calories / capita / day")
                ax_box.set(title="Monte Carlo outcomes")

        plt.tight_layout()
        plt.savefig("plot.svg")
        plt.rcParams["figure.figsize"] = [15, 8]
        os.system('firefox-esr plot.svg')
