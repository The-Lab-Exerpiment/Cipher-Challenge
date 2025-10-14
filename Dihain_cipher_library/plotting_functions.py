from matplotlib.image import AxesImage
import matplotlib.pyplot as plt
from matplotlib import font_manager, ticker
import numpy as np
from os import getcwd

from numpy._typing import _AnyShape
from typing import Any

font_path = "JetBrainsMono-VariableFont_wght.ttf"
font_entry = font_manager.FontEntry(fname=font_path, name="JetBrainsMono")
font_manager.fontManager.ttflist.append(font_entry)

plt.rcParams["font.family"] = font_entry.name
plt.style.use("dark_background")


def plot_bar_chart(
    data_set_x,
    data_set_y,
    name_x="",
    name_y="",
    title="",
    fig=None,
    ax=None,
    **kw,
):
    if fig is None or ax is None:
        fig, ax = plt.subplots()
    else:
        ax.bar(data_set_x, data_set_y, **kw)
        return fig, ax
    ax.set_xlabel(name_x)
    try:
        ax.set_xticks(range(len(data_set_x)), data_set_x)
    except:
        pass
    ax.set_title(title)
    ax.set_ylabel(name_y)
    ax.bar(data_set_x, data_set_y, **kw)
    return fig, ax


def heatmap(
    data_param: list[list[Any]],
    row_labels: list[str],
    column_labels: list[str],
    colour_bar_label: str = "",
    title: str = "",
    name_x="",
    name_y="",
    colour_map="magma_r",
):
    fig, ax = plt.subplots()
    data = np.array(data_param)

    im = ax.imshow(data, cmap=colour_map)  # type: ignore
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel(colour_bar_label, rotation=-90, va="bottom")
    ax.set_title(title)

    xticks = list(range(len(data[0])))
    yticks = list(range(len(data)))

    ax.set_xticks(
        xticks, labels=column_labels, rotation=0
    )  # ha="right" # rotation_mode="anchor"
    ax.set_yticks(yticks, labels=row_labels)

    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)

    ax.spines[:].set_visible(False)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    ax.set_ylabel(name_y)
    ax.set_xlabel(name_x)

    return fig, im, cbar


def annotate_heatmap(
    im: AxesImage,
    data_param=None,
    valfmt: str = "{x:.2f}",
    textcolors: tuple[str] = ("black", "white"),  # type: ignore
    threshold: None = None,
):
    data: np.ndarray[_AnyShape, np.dtype[Any]]
    if data_param is None:
        data = im.get_array()  # type: ignore
    else:
        data = data_param

    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2  # type: ignore

    strformatter = ticker.StrMethodFormatter(valfmt)

    kw = dict(horizontalalignment="center", verticalalignment="center")

    for i in range(data.shape[0]):  # type: ignore
        for j in range(data.shape[1]):  # type: ignore
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            im.axes.text(j, i, strformatter(data[i, j], None), kw)


def save_figure_as_svg(fig, target_file: str):
    fig.set_size_inches(24, 13.5)
    if target_file:
        target_file = target_file
        plt.savefig(target_file, bbox_inches="tight")
