from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from windrose import WindroseAxes

# ==================================================
# PLOT STYLE
# ==================================================

plt.rcParams.update({
    "figure.dpi": 300,
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "legend.fontsize": 11,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
})

# ==================================================
# CSV FILES
# ==================================================

CSV_FILES = [
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (3).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (4).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (5).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (6).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (7).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (8).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (9).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (10).csv",
    "/home/mateusfernandes/Pictures/gifiguape/windetec/generatedBy_react-csv (11).csv",
]

# ==================================================
# DATA LOADING
# ==================================================

def load_data():

    dataframes = []

    for file in CSV_FILES:

        if not Path(file).exists():
            print(f"File not found: {file}")
            continue

        df = pd.read_csv(
            file,
            sep=";",
            decimal=","
        )

        dataframes.append(df)

    if len(dataframes) == 0:
        raise FileNotFoundError(
            "No CSV files were found."
        )

    df = pd.concat(
        dataframes,
        ignore_index=True
    )

    print("\nAvailable columns:")
    print(df.columns.tolist())

    df = df[
        [
            "Data",
            "Hora (UTC)",
            "Vel. Vento (m/s)",
            "Dir. Vento (m/s)",
            "Raj. Vento (m/s)",
        ]
    ]

    df = df.dropna()

    df["Hora (UTC)"] = (
        df["Hora (UTC)"]
        .astype(str)
        .str.zfill(4)
    )

    df["datetime"] = pd.to_datetime(
        df["Data"] + " " + df["Hora (UTC)"],
        format="%d/%m/%Y %H%M"
    )

    df = df.set_index("datetime")

    df = df.drop(
        columns=["Data", "Hora (UTC)"]
    )

    return df.sort_index()

# ==================================================
# STATISTICS
# ==================================================

def print_statistics(df):

    print("\n===== WIND STATISTICS =====")

    print(
        f"Mean wind speed: "
        f"{df['Vel. Vento (m/s)'].mean():.2f} m/s"
    )

    print(
        f"Maximum wind speed: "
        f"{df['Vel. Vento (m/s)'].max():.2f} m/s"
    )

    print(
        f"Mean gust speed: "
        f"{df['Raj. Vento (m/s)'].mean():.2f} m/s"
    )

    print(
        f"Maximum gust speed: "
        f"{df['Raj. Vento (m/s)'].max():.2f} m/s"
    )

# ==================================================
# WIND ROSE
# ==================================================

def plot_windrose(df):

    speed = df["Vel. Vento (m/s)"]
    direction = df["Dir. Vento (m/s)"]

    fig = plt.figure(figsize=(8, 8))

    ax = WindroseAxes.from_ax()

    ax.bar(
        direction,
        speed,
        normed=True,
        opening=0.9,
        edgecolor="white"
    )

    ax.set_title(
        "Wind Rose",
        pad=20
    )

    ax.set_legend(
        title="Wind Speed (m/s)",
        loc="lower left"
    )

    plt.tight_layout()
    plt.show()

# ==================================================
# DAILY MEAN WIND SPEED
# ==================================================

def plot_daily_mean(df):

    daily_mean = (
        df.resample("D")
        .mean(numeric_only=True)
    )

    plt.figure(figsize=(14, 5))

    plt.plot(
        daily_mean.index,
        daily_mean["Vel. Vento (m/s)"],
        linewidth=1.8
    )

    plt.scatter(
        daily_mean.index,
        daily_mean["Vel. Vento (m/s)"],
        s=12
    )

    plt.title("Daily Mean Wind Speed")

    plt.xlabel("Date")
    plt.ylabel("Wind Speed (m/s)")

    plt.grid(
        alpha=0.3,
        linestyle="--"
    )

    plt.tight_layout()
    plt.show()

# ==================================================
# MONTHLY MEAN WIND SPEED
# ==================================================

def plot_monthly_mean(df):

    monthly_mean = (
        df.resample("MS")
        .mean(numeric_only=True)
        .dropna(how="all")
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        monthly_mean.index,
        monthly_mean["Vel. Vento (m/s)"],
        marker="o",
        linewidth=2
    )

    plt.title("Monthly Mean Wind Speed")

    plt.xlabel("Month")
    plt.ylabel("Wind Speed (m/s)")

    plt.grid(
        alpha=0.3,
        linestyle="--"
    )

    plt.tight_layout()
    plt.show()

# ==================================================
# DIURNAL CYCLE
# ==================================================

def plot_diurnal_cycle(df):

    df_hour = df.copy()

    df_hour["hour"] = df_hour.index.hour

    hourly_mean = (
        df_hour.groupby("hour")
        ["Vel. Vento (m/s)"]
        .mean()
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        hourly_mean.index,
        hourly_mean.values,
        marker="o",
        linewidth=2
    )

    plt.fill_between(
        hourly_mean.index,
        hourly_mean.values,
        alpha=0.25
    )

    plt.title("Mean Diurnal Wind Cycle")

    plt.xlabel("Hour (UTC)")
    plt.ylabel("Wind Speed (m/s)")

    plt.xticks(range(24))

    plt.grid(
        alpha=0.3,
        linestyle="--"
    )

    plt.tight_layout()
    plt.show()

# ==================================================
# WIND SPEED DISTRIBUTION
# ==================================================

def plot_histogram(df):

    plt.figure(figsize=(10, 5))

    plt.hist(
        df["Vel. Vento (m/s)"],
        bins=25
    )

    plt.title("Wind Speed Distribution")

    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Frequency")

    plt.grid(
        alpha=0.3,
        linestyle="--"
    )

    plt.tight_layout()
    plt.show()

# ==================================================
# MAIN
# ==================================================

def main():

    df = load_data()

    print_statistics(df)

    plot_windrose(df)

    plot_daily_mean(df)

    plot_monthly_mean(df)

    plot_diurnal_cycle(df)

    plot_histogram(df)

if __name__ == "__main__":
    main()