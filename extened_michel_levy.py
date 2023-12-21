import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider
from matplotlib.patches import Rectangle

wavelengths = np.arange(360, 830, 1)

""" import and interpolate CIE data """

def read_csv(filename):
    with open(filename, "r") as f:
        content = f.read()
    data = []
    for line in content.splitlines():
        row = []
        for element in line.split(","):
            if element == "":
                element = 0
            row.append(float(element))
        data.append(row)
    return np.array(data)


# --- interpolation
filename = "ciexyz31_1.csv"
csvdata = read_csv(filename)

xdata = csvdata.T[0, :]
XYZ = (csvdata.T[1:])

XYZ_interpol = np.ones([3, len(wavelengths)])

for i, ydata in enumerate(XYZ):
    XYZ_interpol[i, :] = np.interp(wavelengths, xdata, ydata)

""" all calculations in one function """


def calculate_color(Gamma, gamma_factor=0.5):
    """ Calculate and correct the interference color for one path difference (Gamma).

    Parameters
    ----------
    Gamma : path difference
    gamma_factor : factor for gamma correction (optional; default=0.5)

    Returns
    -------
    RGB-value normalized to 1 as numpy-array
    """

    # --- calculate transmission
    L = np.array(wavelengths, ndmin=2).T
    L = (np.sin(np.pi * Gamma / L)) ** 2

    # --- convert to XYZ and sum over wavelengths
    L_XYZ = np.dot(XYZ_interpol, L)

    # --- conversion to SRGB
    XYZ_to_RGB = np.array([[3.2406, -1.5372, -0.4986],
                           [-0.9689, 1.8758, 0.0415],
                           [0.0557, -0.2040, 1.0570]])
    RGB = np.dot(XYZ_to_RGB, L_XYZ)

    # --- clipping
    RGB[RGB > 100] = 100
    RGB[RGB < 0] = 0

    # --- normalize
    RGB /= 100

    # ---gamma correction
    RGB = RGB ** gamma_factor

    return RGB.ravel()


# --- setup
birefringences = np.linspace(0, 0.1, 1000, endpoint=True)
thicknesses = np.linspace(0, 50, 100, endpoint=True)

thickness = max(thicknesses) * 1000
RGB = np.zeros([len(birefringences), 3])

# --- actual calculation
for i, biref in enumerate(birefringences):
    color = calculate_color(biref * thickness)
    RGB[i, :] = color.ravel()
RGB = np.array(RGB)

# --- preparation of plotimage
plotimage = np.zeros([len(thicknesses), len(birefringences), 3])
plotimage[:, :, 0] = RGB[:, 0]
plotimage[:, :, 1] = RGB[:, 1]
plotimage[:, :, 2] = RGB[:, 2]

# --------------------------------------------------------
# --- below is is just plotting

# --- setup
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
textprops = {"zorder": 200, "size": 9}
aspect = 30

# --- define axis limits
xlims = [min(thicknesses) * 1000 * min(birefringences),
         max(thicknesses) * 1000 * max(birefringences)]
ylims = [min(thicknesses), max(thicknesses)]

# --- plot image
ax.imshow(plotimage, origin="upper",
          extent=xlims + ylims,
          zorder=1, aspect=aspect)

# --- adding lines of constant birefringence (and labels)
biref_label = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03,
               0.035, 0.04, 0.045, 0.05, 0.06, 0.07,
               0.08, 0.09, 0.1, 0.12, 0.14, 0.16, 0.2, 0.22, 0.4]
minx = np.min(birefringences)
maxx = np.max(birefringences)
miny = np.min(thicknesses)

# ------ example: mark an area of a certain birefringence and thickness:
biref_marked = [0.12, 0.14]
thickness_marked = [1,4]

xscaler = (xlims[1] - xlims[0]) / (max(birefringences) - min(birefringences))
for i, bl in enumerate(biref_label + biref_marked):
    xval = bl * xscaler
    if bl in biref_marked:
        lw = 1
        alpha = 1
    else:
        lw = 0.5
        alpha = 0.5
    ax.plot((xlims[0], xval), ylims, zorder=100, color="black", lw=lw, alpha=alpha)

    # --- add text
    textrot = 180 / np.pi * np.arctan(aspect * (ylims[1] - ylims[0]) / (xval - xlims[0]))
    if xval <= xlims[1]:
        ax.text(xval, ylims[1], "  " + str(bl), ha="left", va="bottom", rotation=textrot, **textprops)
    else:
        ytext = ylims[0] + ((xlims[1] - xlims[0]) * ((ylims[1] - ylims[0]) / (xscaler * bl)))
        ax.text(xlims[1], ytext, "  " + str(bl), ha="left", va="bottom", rotation=textrot, **textprops)

# --- adding lines and text for color orders
orders = np.arange(550, xlims[1] + 550, 550)
orders_letters = ["I", "II", "III", "IV", "V", "VI", "VII", "IIX", "IX", "X"]

for order, letter in zip(orders, orders_letters):
    if order <= xlims[1]:
        ax.vlines(order, ylims[0], ylims[0] - 13, clip_on=False, alpha=0.5, zorder=0,
                  color="red", lw=2)
    ax.text(order - 225, -13, letter, color="red", ha="center", va="bottom")

# --- finalize plot (ticks, grid-lines)
yticks = list(np.arange(ylims[0], ylims[1] + 5, 5)) + thickness_marked
xticks = np.arange(xlims[0], xlims[1] + 400, 400)
ax.set_xticklabels(["{:.0f}".format(_) for _ in xticks], rotation=90)

for yt in yticks:
    if yt in thickness_marked:
        lw = 1
        alpha = 1
    else:
        lw = 0.5
        alpha = 0.5
    ax.axhline(yt, zorder=100, color="black", lw=lw, alpha=alpha)

ax.set_yticks(yticks)
ax.set_xticks(xticks)
xminorticks = np.arange(xlims[0], xlims[1], 100)
ax.set_xticks(xminorticks, minor=True)

ax.tick_params(axis="both", which="both", direction="out", top="off", right="off")

# --- finalize plot (labels, title)
ax.text(xlims[0], ylims[1] + 1, "birefringence\n" + r"$\longrightarrow$", ha="center", va="bottom", **textprops)
ax.text(xlims[0], ylims[0] - 4.5, r"path difference [nm]" + "\n"r"$\longrightarrow$", ha="center", va="top",
        **textprops)
ax.text(xlims[0], ylims[0] - 13, r"color order", ha="center", va="bottom", color="red")
ax.set_ylabel(r"sample thickness [$\mathrm{\mu m}$]", **textprops)
plt.title("Extended calclulated Michel-Lévy color chart", y=1.15)
# NOTES: For python 2 you need to declare this as unicode (because of the accent):
# plt.title(u"Calculated Michel-Lévy color chart", y=1.15)

# --- finalize plot (set limits)
ax.set_xlim(*xlims)
ax.set_ylim(*ylims)

# plt.savefig("./images/extended_chart.pdf") #<-- uncomment to save
# plt.savefig("./images/extended_chart.png") #<-- uncomment to save
plt.show()

#--- setup
birefringences = np.linspace(0, 0.1, 1000, endpoint=True)
thicknesses    = np.linspace(0,50, 100, endpoint=True)

#--- calculation
plotimage = np.zeros([len(thicknesses), len(birefringences), 3])
for n, thickness in enumerate(thicknesses):
    for m, biref in enumerate(birefringences):
        color = calculate_color(biref*thickness*1000)
        plotimage[n,m,:] = color
# Note: The nested for loop is slow. Could be be faster in numpy form,
# but it's easier to understand if it uses the function.

#--- plotting

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)

xlims = [min(birefringences), max(birefringences)]
ylims = [min(thicknesses), max(thicknesses)]
aspect = 10**-3

ax.imshow(np.flipud(plotimage), origin="upper", extent=xlims+ylims, aspect=aspect,zorder=1)
ax.set_xlabel("birefringence")
ax.set_ylabel("sample thickness [$\mathrm{\mathrm{\mu m}}$]")

ax.minorticks_on()
ax.grid("on", which="major", ls="-", lw=0.5, alpha=0.5)
ax.grid("on", which="minor", ls="-", lw=0.5, alpha=0.2)
ax.tick_params(which="both", direction="out", right="off", top="off")

# plt.savefig("./images/chart2.pdf")
# plt.savefig("./images/chart2.png")
plt.show()

# --- same plot, but with added rectangles for minerals

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)

xlims = [min(birefringences), max(birefringences)]
ylims = [min(thicknesses), max(thicknesses)]
aspect = 10 ** -3

ax.imshow(np.flipud(plotimage), origin="upper", extent=xlims + ylims, aspect=aspect, zorder=1)
ax.set_xlabel("birefringence")
ax.set_ylabel("sample thickness [$\mathrm{\mathrm{\mu m}}$]")

ax.minorticks_on()
ax.grid("on", which="major", ls="-", lw=0.5, alpha=0.5)
ax.grid("on", which="minor", ls="-", lw=0.5, alpha=0.2)
ax.tick_params(which="both", direction="out", right="off", top="off")

thickness = [28, 32]
enstatite = [0.007, 0.011]
diopsid = [0.03, 0.025]
olivine = [0.035, 0.05]

loopdict = {"En": [thickness, enstatite],
            "Di": [thickness, diopsid],
            "Ol": [thickness, olivine]}

for key, val in loopdict.items():
    text = key
    xspan = val[1]
    yspan = val[0]
    R = Rectangle((xspan[0], yspan[0]),  # x,y of lower left corner
                  (xspan[1] - xspan[0]),  # width
                  (yspan[1] - yspan[0]),  # height
                  facecolor="none",
                  edgecolor="black",
                  zorder=100)
    ax.add_patch(R)
    ax.text(xspan[0] + 0.5 * (xspan[1] - xspan[0]), yspan[1], text,
            color="black",
            ha="center", va="bottom")

# plt.savefig("./images/chart2_wboxes.pdf")
# plt.savefig("./images/chart2_wboxes.png")
plt.show()

# --- setup
birefs = np.linspace(0.12, 0.17, 1000, endpoint=True)
thickness = 3E3

# --- calculation
RGB_one_thickness = []

for biref in birefs:
    RGB_one_thickness.append(calculate_color(biref * thickness))
RGB_one_thickness = np.array(RGB_one_thickness)

plotimage = np.zeros([100, len(birefs), 3])
plotimage[:, :, :] = RGB_one_thickness[:, :]

# --- plot
fig, ax = plt.subplots(1)

xlims = [min(birefs), max(birefs)]
ylims = [0, 100]

aspect = 1E-4
ax.imshow(plotimage, origin="upper", extent=xlims + ylims, aspect=aspect)

ax.set_yticks([])

xticks = np.arange(xlims[0], xlims[1] + 0.01, 0.01)
xticks_gamma = xticks * thickness
xticklabels = ["{:}\n({:})".format(a, b) for a, b in zip(xticks, xticks_gamma)]
ax.set_xticklabels(xticklabels, rotation=90)

ax.set_title("Interference colors for fixed thickness ({:.0f} $\mu m$)".format(thickness * 1E-3))
ax.set_xlabel("birefringence\n(path difference [nm])")
ax.tick_params(direction="out", top="off")

plt.savefig("fixed_thickness.pdf")
plt.savefig("fixed_thickness.png")
plt.show()

# --- setup
biref = 0.13
thicknesses = np.linspace(0, 5, 1000, endpoint=True)

# --- calculation

RGB_one_biref = []
for thickness in thicknesses:
    RGB_one_biref.append(calculate_color(biref * thickness * 1000))
RGB_one_biref = np.array(RGB_one_biref)

plotimage = np.zeros([100, len(thicknesses), 3])
plotimage[:, :, :] = RGB_one_biref[:, :]

# --- plot
fig, ax = plt.subplots(1)

xlims = [min(thicknesses), max(thicknesses)]
ylims = [0, 100]

aspect = 1E-1
ax.imshow(plotimage, origin="upper", extent=xlims + ylims, aspect=aspect)

ax.set_yticks([])

xticks = np.arange(xlims[0], xlims[1] + 10, 10)
xticks_gamma = xticks * biref * 1000
xticklabels = ["{:g}\n({:g})".format(a, b) for a, b in zip(xticks, xticks_gamma)]
ax.set_xticklabels(xticklabels, rotation=90)

ax.set_title("Interference colors for fixed birefringence ({:g})".format(biref))
ax.set_xlabel("thickness [$\mu m$]\n(path difference [nm])")

ax.tick_params(direction="out", top="off")

plt.savefig("fixed_birefringence.pdf")
plt.savefig("fixed_birefringence.png")
plt.show()


def plot_color(birefringence, thickness, compensator=0):
    # --- Calculate path difference and optional and shift
    Gamma = birefringence * thickness * 1E3
    Gamma += 550 * compensator
    # --- determine color order
    order = 0
    check = 0
    while True:
        if Gamma < check:
            break
        check += 550
        order += 1

    # --- get color
    color = calculate_color(Gamma)

    # --- plot
    plotimage = np.zeros([20, 20, 3])
    plotimage[:, :, :] = color
    plt.close("all")
    fig, ax = plt.subplots(1)
    ax.imshow(plotimage, origin="upper")
    ax.set_xticks([])
    ax.set_yticks([])
    text = "birefringence = {:}\n tickness = {:}".format(birefringence, thickness)
    ax.set_title(text)

    ax.text(0, 0, "Order: {:d}".format(order), backgroundcolor="white",
            ha="left", va="top")

    plt.show()

interact(plot_color,
         birefringence=FloatSlider(min=0, max=0.2, step=0.0001),
         thickness=FloatSlider(min=20, max=40, step=2),
         compensator=IntSlider(min=-2, max=2, step=1))
