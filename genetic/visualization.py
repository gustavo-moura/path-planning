import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

import plotly.graph_objects as go

from sklearn import preprocessing


cor_area_nn = "#25283d"  # Yankees Blue
cor_area_p = "#8f3985"  # Plum
cor_area_b = "#07beb8"  # Tiffany Blue
cor_waypoints = "#aa1155"  # Jazzberry Jam
cor_ori_dest = "#880044"  # Pink Raspberry


def new_shape(vertices, color="navajowhite", lw=0.25):

    assert len(vertices) >= 3, "At least 3 vertices to form a shape"

    vertices.append(vertices[0])  # corrects the final movement point

    colors = {"n": cor_area_nn, "p": cor_area_p, "b": cor_area_b}

    color = colors[color] if color in colors else color

    codes = [Path.MOVETO]
    for _ in range(1, len(vertices) - 1):
        codes.append(Path.LINETO)
    codes.append(Path.CLOSEPOLY)

    path = Path(vertices, codes)

    patch = patches.PathPatch(path, facecolor=color, lw=lw, alpha=0.6)

    return patch


def plot_map(wp_style="-x", **kwargs):
    # Optional arguments:
    # areas, labels, origem, destino, waypoints, texts

    _, ax = plt.subplots(figsize=(8, 8))

    # Plot areas
    if "areas" in kwargs and "labels" in kwargs:
        areas = kwargs["areas"]
        labels = kwargs["labels"]
        patches = [
            new_shape(vertices, color=label) for vertices, label in zip(areas, labels)
        ]
        for patch in patches:
            ax.add_patch(patch)

    # Plot origin and destination
    if "origem" in kwargs and "destino" in kwargs:
        origem = kwargs["origem"]
        destino = kwargs["destino"]
        ax.plot(
            [origem[0], destino[0]], [origem[1], destino[1]], "o", color=cor_ori_dest
        )

    # Plot a route with its waypoints
    if "waypoints" in kwargs:
        waypoints = kwargs["waypoints"]
        waypoints = list(map(list, zip(*waypoints)))
        # marker='x', linestyle='solid'
        ax.plot(waypoints[0], waypoints[1], wp_style, color=cor_waypoints, linewidth=2)
        if "texts" in kwargs:
            for i, text in enumerate(kwargs["texts"]):
                ax.annotate(text, (waypoints[0][i], waypoints[1][i]))

    # Plot multiple routes with waypoints, along with name and specific colors
    if "multi_waypoints" in kwargs:
        for waypoints, label, color in zip(
            kwargs["multi_waypoints"], kwargs["names"], kwargs["colors"]
        ):
            waypoints = list(map(list, zip(*waypoints)))
            ax.plot(
                waypoints[0],
                waypoints[1],
                wp_style,
                color=color,
                linewidth=2,
                label=label,
            )  # marker='x', linestyle='solid'
            if "texts" in kwargs:
                for i, text in enumerate(kwargs["texts"]):
                    ax.annotate(text, (waypoints[0][i], waypoints[1][i]))

    if "stress" in kwargs:
        # Plot waypoints
        if "points" in kwargs:
            for wp, text in zip(kwargs["points"], kwargs["texts"]):
                if text == "T":
                    in_color = cor_area_b
                else:
                    in_color = cor_waypoints

                ax.plot(wp[0], wp[1], wp_style, color=in_color, linewidth=2)
                ax.annotate(text, (wp[0], wp[1]))

        # Plot segments
        if "segments" in kwargs and "texts" in kwargs:
            i = 0
            for segment, text in zip(kwargs["segments"], kwargs["texts"]):
                X = [segment[0].x, segment[1].x]
                Y = [segment[0].y, segment[1].y]

                if text == "T":
                    in_color = cor_area_b
                else:
                    in_color = cor_waypoints
                ax.plot(X, Y, wp_style, color=in_color, linewidth=2)

                ax.annotate(text + str(i), (X[0], Y[0]))
                i += 1

        # Plot chance constraints tests
        if "chance" in kwargs:

            base_das_normais = []

            for segment, normal, segment_text in zip(
                kwargs["segments"], kwargs["normals"], kwargs["segment_texts"]
            ):
                X = [segment[0].x, segment[1].x]
                Y = [segment[0].y, segment[1].y]
                ax.plot(X, Y, wp_style, color=cor_waypoints, linewidth=3)
                ax.annotate(segment_text[0], (X[0], Y[0]))
                ax.annotate(segment_text[1], (X[1], Y[1]))

                x = _graph_sub(segment[0].x, segment[1].x)
                y = _graph_sub(segment[0].y, segment[1].y)
                base_das_normais.append([x, y])
                ax.quiver(
                    x, y, normal.x, normal.y, angles="xy", scale_units="xy", scale=1
                )

            for P, point_text in zip(kwargs["pointes"], kwargs["point_texts"]):
                ax.plot(P.x, P.y, "o", color=cor_area_nn, linewidth=4)
                ax.annotate(point_text, (P.x, P.y * 1.05))

                for normal, dist in zip(base_das_normais, kwargs["distances"]):
                    X = [P.x, normal[0]]
                    Y = [P.y, normal[1]]
                    ax.plot(X, Y, "", color=cor_area_nn, linewidth=2)

                    x = _graph_sub(P.x, normal[0])
                    y = _graph_sub(P.y, normal[1])
                    ax.annotate(str(dist), (x, y * 1.05))

    # Set size
    if "margin" in kwargs:
        sl = kwargs["margin"]
    else:
        sl = 1

    automin, automax = ax.get_xlim()
    plt.xlim(automin - sl, automax + sl)
    automin, automax = ax.get_ylim()
    plt.ylim(automin - sl, automax + sl)
    plt.gca().set_aspect("equal", adjustable="box")

    if "title" in kwargs:
        plt.title(kwargs["title"])

    plt.show()
    # plt.savefig('out.png')


def plot_stats(ag_trace, normalize=True):
    dft = pd.DataFrame.from_dict(ag_trace)

    if normalize:
        x = dft.values  # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        dft = pd.DataFrame(x_scaled, columns=dft.columns)

    fig = go.Figure()

    for column in dft.columns:
        fig.add_trace(go.Scatter(x=dft.index, y=dft[column], name=column))
    fig.show()


def _graph_sub(A, B):
    menor = min(A, B)
    maior = max(A, B)

    return menor + ((maior - menor) / 2)
