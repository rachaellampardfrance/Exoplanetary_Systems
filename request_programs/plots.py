"""functions to create visual figures from dataframes"""

from matplotlib import pyplot as plt
import matplotlib.figure
import numpy as np
import pandas as pd

from helpers import format_name_for_file, render_figlet
from database_helpers import get_stellar_hosts_db_data
from save import save_dated_figure

TEXT_COLOUR = '#581845'
# colour map with id's for correct allocation
PLANET_COLOUR_MAP = {
    1: '#519DE9',
    2: '#7CC674',
    3: '#73C5C5',
    4: '#8481DD',
    5: '#F6D173',
    6: '#EF9234',
    7: '#A30000',
    8: '#D2D2D2'
}

# incase planet colors are wanted without mapping
PLANET_COLOURS = PLANET_COLOUR_MAP.values()

STAR_COLOURS = [
    '#F4C145',
    '#EC7A08',
    '#A30000',
    '#470000'
]

def main():
    # get dataframe from stellar_hosts database table
    render_figlet("Plots...")

    sh_df = get_stellar_hosts_db_data()
    systems_df = create_systems_df(sh_df)

    star_series = create_star_series(systems_df)
    planet_to_star_df = create_planet_to_star_df(systems_df)

    save_figures(
        star_series=star_series,
        planet_to_star_df=planet_to_star_df
    )

    print("figures saved")


def create_systems_df(data: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(data)

def create_star_series(data: pd.DataFrame) -> pd.DataFrame:
    """group df by sy_snum size all instance of star count are combined,
    see the occurance of systems that contain any amount of planets
    """
    star_srs = data.groupby('sy_snum').size()
    # see the series
    print(star_srs)
    # # see series index values
    # print(star_srs.index.values)
    # # see sum of data
    # print(star_srs.sum())

    return star_srs

def create_planet_to_star_df(data):
    planet_to_star_df = data.groupby(['sy_snum', 'sy_pnum']).size().unstack(fill_value=0)

    # see visual dataframe representation
    print(planet_to_star_df)

    return planet_to_star_df


def save_figures(star_series, planet_to_star_df):
    """save all figures"""

    # create figure
    fig1, fig1_name = create_fig_star_pie(star_series=star_series)
    # save figure
    save_fig(fig1, fig1_name)

    # create figure
    fig2, fig2_name = create_fig_nested_bar(planet_to_star_df=planet_to_star_df)
    # save figure
    save_fig(fig2, fig2_name)

    # create figure
    fig3, fig3_name = create_fig_system_pies(planet_to_star_df=planet_to_star_df)
    # save figure
    save_fig(fig3, fig3_name)

def save_fig(fig: matplotlib.figure.Figure, fig_name: str) -> None:
    """formats file names and saves figures"""

    # overwrite top level figure
    fig.savefig(("static/"+fig_name+".png"))
    # save with datestamp to dated folder
    save_dated_figure(fig, fig_name, "png")

def create_fig_star_pie(star_series):
    """generate Occurance of Planetary Systems by Star System Type pie figure"""

    # create figure for chart and text to display on
    fig, ax = plt.subplots(figsize=(8, 6))
    # Array of the dataframe index == star count for the legend
    labels = star_series.index.values
    # explode hard to see data
    explode = (0, 0, 0, 0.5)

    # create pie chart
    ax.pie(
        star_series,
        colors=STAR_COLOURS,
        explode=explode,
        labels=labels,
        autopct='%1.2f%%',
        pctdistance=0.5,
        labeldistance=1.2,
        textprops={
            'size' : 'large',
            'color': '#581845',
            'weight': 'bold'}
    )

    plt_title = "Occurrence of Planetary\nSystems by Star System Type"

    ax.set_title(
        plt_title,
        fontsize=16
        )

    # allow legend to be set to fig not ax
    fig.legend(
        labels,
        title="Stars in system",
        title_fontsize=12,
        loc=1,
        fontsize=12
        )

    # file saving name reference
    fig_name = format_name_for_file(plt_title)

    return fig, fig_name


def create_fig_nested_bar(planet_to_star_df):
    """generate exoplanet_systems_by_star_count nested bar figure"""

    # create a figure that contains 2 plots
    fig, ax = plt.subplots(1, 2, figsize=(16, 5))

    bar_width = 0.1
    # returns [0, 1, 2, 3]
    indices = np.arange(len(planet_to_star_df))

    # for both plts (as they are the same in exception of 1 being log)
    i = 0
    while i < 2:
        #********************
        # Author: ChatGPT
        # Date: 2024
        for j, planet_count in enumerate(planet_to_star_df.columns):
            # label = creates the planets 1-8 side labels legend
            bars = ax[i].bar(
                x=indices + j * bar_width,
                height=planet_to_star_df[planet_count],
                width=bar_width,
                label=f'{planet_count}',
                color=PLANET_COLOUR_MAP[planet_count]
            )

            # print observation values atop the bars
            for bar in bars:
                yval = bar.get_height()
                if yval > 0:
                    ax[i].text(
                        bar.get_x() + bar.get_width()/2,
                        yval + 0.1, int(yval),
                        ha='center',
                        va='bottom',
                        fontsize=8,
                    )
        # *******************

        ax[i].set_xlabel('System Star Count')
        ax[i].set_ylabel('Observations')
        ax[i].set_xticks(indices + bar_width * 4)
        ax[i].set_xticklabels(planet_to_star_df.index)
        ax[i].legend(title='Planets')
        i += 1

    ax[0].set_title('Planetary Systems by Star Count (SCALE)')

    # for visualisation of smaller data
    ax[1].set_yscale('log')
    ax[1].set_title('Planetary Systems by Star Count (LOG)')

    fig_name = "planetary_systems_by_star_count"

    return fig, fig_name


def create_fig_system_pies(planet_to_star_df):
    """generate Most Common Exoplanet Systems pies figure"""

    # assign axes to automate axes columns for charts
    axes = len(planet_to_star_df)
    fig, ax = plt.subplots(1, axes, figsize=(16, 5))

    # generate each ax automatically on star count
    i = 0
    while i < axes:
        # get row of data from grouped (this will be in relation to star)
        star_system = planet_to_star_df.iloc[i]

        # calculate the 1% value to leave remove from dataset (small data)
        less_1_percent = 0.01 * star_system.sum()
        star_system = star_system[star_system > less_1_percent]
        # get labels == planet count
        lables = star_system.index.values
        # explode wedges by data count
        explode = [0.1] * len(lables)

        # create a color map with only the labels in current data
        # *************
        # Author: ChatGPT
        # Date: 2024
        colors = [
            PLANET_COLOUR_MAP[label]
            for label in star_system.index
            if label in PLANET_COLOUR_MAP
        ]
        # *************

        ax[i].pie(
            star_system,
            labels=lables,
            colors=colors,
            autopct='%1.2f%%',
            pctdistance=0.5,
            explode=explode,
            textprops={'color': TEXT_COLOUR, 'weight': 'bold'}
        )

        # systems_df.name makes sure that the right star count if printed out if there
        # was a missing star count i.e no 5 star systems but there was a 6 star system
        ax[i].set_title(
            f"{star_system.name} star",
        )
        i += 1

    # *************
    # Author: ChatGPT
    # Date: 2024
    # ChatGPT wrote this for me as I struggled with the handles documentation
    handles = [
        plt.Line2D([0], [0],
        marker='o',
        markerfacecolor=PLANET_COLOUR_MAP[label],
        markersize=12) for label in PLANET_COLOUR_MAP.keys()
    ]
    # *************

    # create legend with corrosponding colours for
    # planet counts and colours
    fig.legend(
        handles,
        PLANET_COLOUR_MAP.keys(),
        title="Number of Planets",
        loc=1,
    )

    fig_title = "Most Common Planetary Systems"
    fig_under_title = "(excluding Planetary Systems falling under 1%)"
    fig.text(0.51, 0.95, fig_title, size=14, horizontalalignment='center')
    fig.text(0.51, 0.9, fig_under_title, size=10, horizontalalignment='center', fontstyle='italic')

    # file saving name reference
    fig_name = format_name_for_file(fig_title)

    return fig, fig_name


if __name__ == "__main__":
    main()
