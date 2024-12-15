import matplotlib.pyplot as plt
import pandas as pd


def draw_bar_chart(
    df: pd.DataFrame,
    title: str,
    bar_label_format: str = "%.2f",
    grey_colors: list = ["#E6E6E6", "#CDCDCD", "#909090"],
    highlight_colors: list = ["#C9E6F0", "#80C4E9", "#78B3CE"],
    numeric_labels_padding=-30,
    to_highlight: list = [],
    size=(10, 6),
):
    k_labels = list(df.columns)

    axes = df.plot(
        y=k_labels,
        kind="barh",
        width=0.8,
        figsize=(10, 6),
        color=highlight_colors,
        title=title,
    )
    # axes.legend(loc='lower right')
    axes.get_legend().remove()
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    axes.set_xlim(0, df.max().max() * 1.2)

    y_axis = axes.get_yaxis()
    y_label = y_axis.get_label()
    y_label.set_visible(False)

    x_axis = axes.get_xaxis()
    x_label = x_axis.get_label()
    x_label.set_visible(True)

    # Get y-axis labels (index values)
    y_labels = df.index.tolist()

    axes.title.set_fontsize(16)

    for i, container in enumerate(axes.containers):
        labels = axes.bar_label(
            container,
            label_type="edge",
            fmt=bar_label_format,
            padding=numeric_labels_padding,
        )

        # Then update colors for specific bars and their labels
        for j, (bar, label) in enumerate(zip(container.patches, labels)):
            label_text = y_labels[j]

            if len(to_highlight) > 0:
                if label_text in to_highlight:
                    label.set_color("black")
                    width = bar.get_width()
                    label_y = bar.get_y() + bar.get_height() / 2
                    if len(k_labels) > 1:
                        axes.text(
                            width * 1.03, label_y, k_labels[i], va="center", ha="left"
                        )
                else:
                    bar.set_color(grey_colors[i])
                    label.set_color("#555555")

            if bar.get_width() == 0:
                label.set_visible(False)

    figure = axes.get_figure()
    if figure is not None:
        figure.set_size_inches(size[0], size[1])

    plt.tight_layout()
