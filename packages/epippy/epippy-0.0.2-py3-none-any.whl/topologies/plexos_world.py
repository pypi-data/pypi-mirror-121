

import pandas as pd

from epippy import data_path


def preprocess(plotting=False):

    # Get buses
    link_data_fn = f"{data_path}topologies/plexos-world/source/PLEXOS-World 2015 Gold V1.1.xlsx"
    data = pd.read_excel(link_data_fn, sheet_name='Attributes')
    buses_df = data[data['class'] == 'Node']

    def get_coordinates(x):
        lat = x[x.attribute == 'Latitude']["value"].values[0]
        lon = x[x.attribute == 'Longitude']["value"].values[0]
        return lon, lat

    buses_df = buses_df.groupby("name")[["attribute", "value"]].apply(lambda x: get_coordinates(x)).to_frame()
    buses_df['x'] = buses_df.apply(lambda p: p[0][0], axis=1)
    buses_df['y'] = buses_df.apply(lambda p: p[0][1], axis=1)
    buses_df = buses_df.drop(0, axis=1)
    buses_df.index = buses_df.index.map(lambda x: ''.join(x.split('-')[1:]))
    buses_df.index.names = ["id"]
    print(buses_df)

    link_data_fn = f"{data_path}topologies/plexos-world/source/PLEXOS-World 2015 Gold V1.1.xlsx"
    data = pd.read_excel(link_data_fn, sheet_name='Properties', usecols=[1, 4, 7],
                         names=["type", "name", "value"], dtype={'type': str, 'name': str, 'value': int})
    lines_df = data[data.type == "Line"]
    lines_df["value"] = lines_df["value"].abs()
    lines_df = lines_df.groupby("name")["value"].max().to_frame()
    print(lines_df)

    def find_bus0(x):
        print(x)
        bus = buses_df.loc[[x.startswith(bus) for bus in buses_df.index]]
        print(bus)
        return bus
    lines_df["bus0"] = lines_df.index.map(lambda x: find_bus0(x))
    print(lines_df)

    exit()
    if plotting:
        from epippy.topologies.core.plot import plot_topology
        plot_topology(buses, links)
        plt.show()


if __name__ == '__main__':
    preprocess()
