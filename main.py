import numpy as np
import matplotlib.pyplot as plt
import imageio


ref_img = imageio.v2.imread('chart_reference.png')

#Transmission function and what it looks like
def Transmission(Gamma, wavelength):
    L = np.sin(np.pi*Gamma/wavelength)
    return L
Gamma = np.arange(0,10E3,10)
wavelength = np.arange(350,850,1)
plotimage = np.zeros([len(wavelength), len(Gamma)])
for n,wl in enumerate(wavelength):
    for m,G in enumerate(Gamma):
        plotimage[n,m] = Transmission(G, wl)
fig,ax = plt.subplots(1, figsize=(7,7))
im = ax.imshow(np.flipud(plotimage), origin="upper",
        extent=[min(Gamma), max(Gamma),
            min(wavelength), max(wavelength)],
    aspect=10, interpolation="none", cmap="seismic")
ax.set_title("transmission")
ax.set_ylabel("wavelength [nm]")
ax.set_xlabel("path difference [nm]")
fig.colorbar(im, orientation="horizontal")
ax.grid("on")
plt.tight_layout()
plt.show()
Transmission_white = np.sum(plotimage, axis= 0)
fig,ax = plt.subplots(1, figsize=(7,5))
ax.plot(Gamma, Transmission_white, color="black" )
ax.set_title("transmission for white light ($\mathrm{\sum_{i}\;L(\lambda_i,\Gamma_j}$))",
        y=1.1)
ax.set_xlabel("path difference [nm]")
ax.set_ylabel("transmission")
plt.tight_layout()
plt.show()

#Building the Michel-Levy chart

#parameters
""" figure parameters """
min_thickness = 0*1E3
max_thickness = 50*1E3
thickn_step = 1
thicknesses = np.arange(min_thickness, max_thickness+thickn_step, thickn_step)
min_birefringence = 0.0
max_birefringence = 0.05
birefstep = 0.00002
birefringences = np.arange(min_birefringence, max_birefringence+birefstep, birefstep)
min_wavelength = 360
max_wavelength = 830
wlstep = 1
wavelengths = np.arange(min_wavelength, max_wavelength+wlstep, wlstep)

""" read CIE data and interpolate for given wavelengths """
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
filename = "ciexyz31_1.csv"
csvdata = read_csv(filename)
xdata = csvdata.T[0,:]
XYZ = csvdata.T[1:]
XYZ_interpol = np.ones([3,len(wavelengths)])
for i,ydata in enumerate(XYZ):
    XYZ_interpol[i, :] = np.interp(wavelengths, xdata, ydata)


""" plot the CIE-data and check interpolation """
fig,ax = plt.subplots(1)
ax.set_title("CIE colormatching functions (original data)")
ax.plot(xdata,XYZ[0], color="red")
ax.plot(xdata,XYZ[1], color="green")
ax.plot(xdata,XYZ[2], color="blue")
ax.set_xlabel(r"$\lambda$ in nm")
ax.set_ylabel(r"relative intensity")
fig,ax = plt.subplots(1)
ax.set_title("CIE colormatching functions (interpolated)")
ax.plot(xdata,XYZ[0], color="red")
ax.plot(xdata,XYZ[1], color="green")
ax.plot(xdata,XYZ[2], color="blue")
ax.plot(wavelengths, XYZ_interpol[0], color="black", ls="", marker="+",
    markersize=5)
ax.plot(wavelengths, XYZ_interpol[1], color="black", ls="", marker="+",
    markersize=5)
ax.plot(wavelengths, XYZ_interpol[2], color="black", ls="", marker="+",
    markersize=5)
ax.set_xlabel(r"$\lambda$ in nm")
ax.set_ylabel(r"relative intensity")
plt.show()

""" calculate transmission L """
L = np.zeros([len(wavelengths),len(birefringences)])
# calculate for one thickness and all birefringences
Gamma = max_thickness * birefringences #<--- warum max. thickness?
for i,wl in enumerate(wavelengths):
    val = (Gamma/wl)*180
    val = np.sin(val*np.pi/180)
    val = val**2
    L[i,:] = val

""" calculate L_XYZ """
L_XYZ = np.dot(XYZ_interpol, L)

""" convert to RGB (comment out SRGB to use Adobe RGB)"""
# Adobe RGB
XYZ_to_RGB = np.array([[2.04414, -0.5649, -0.3447],
[-0.9693, 1.8760, 0.0416],
[0.0134, -0.1184, 1.0154]])
# SRGB
XYZ_to_RGB = np.array([[3.2406, -1.5372, -0.4986],
[-0.9689, 1.8758, 0.0415],
[0.0557, -0.2040, 1.0570]])
RGB = np.dot(XYZ_to_RGB, L_XYZ)


""" clipping and normalizing; firt look at the results """
# clipping
RGB[RGB>100] = 100
RGB[RGB<0] = 0
# normalize to 1
RGB/=100
# prepare plot (stack RGB-vs Gamma arrays)
RGB_plot = np.zeros([len(wavelengths),len(birefringences),3])
RGB_plot[:,:,0] = RGB[0,:]
RGB_plot[:,:,1] = RGB[1,:]
RGB_plot[:,:,2] = RGB[2,:]
# plot
fig,ax = plt.subplots(1)
ax.imshow(RGB_plot, origin="upper")
plt.show()

""" simple gamma correction """
# gamma correction
gamma_factor = 1/2.0 # <-- change for your screen
RGB_plot_gamma = RGB_plot**gamma_factor
# plot
fig,ax = plt.subplots(1)
ax.imshow(RGB_plot_gamma, origin="upper")
plt.show()

fig = plt.figure(figsize=(7,7))
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
ax1.imshow(ref_img)
ax1.set_xticks([])
ax2.set_xticks([])
#--- plot only a slice, since referenc image doesn't cover the whole range
ax2.imshow(RGB_plot[:,:1751,:])
ax3.imshow(RGB_plot_gamma[:,:1751,:])
for ax in [ax1, ax2, ax3]:
    ax.set_xticks([])
    ax.set_yticks([])
ax1.set_title("Zeiss")
ax2.set_title("Calculated")
ax3.set_title("Calculated (gamma corrected, factor {:.1f})".format(gamma_factor))
plt.show()

""" finishing the diagram """
#--- define what data to plot
RGB_plot_final = RGB_plot_gamma
#--- setup
plt.close("all")
fig = plt.figure(figsize=(9,5))
ax = fig.add_subplot(111)
textprops = {"zorder":200, "size":9}
aspect = 20

xlims = [min(Gamma), max(Gamma)]
ylims = [min(thicknesses)*1E-3, max(thicknesses)*1E-3]

#--- plot image
ax.imshow(RGB_plot_final, origin="upper",
    extent=xlims+ylims,
    zorder=1, aspect=aspect)
#--- adding lines of constant birefringence (and labels)
biref_label = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03,
0.035, 0.04, 0.045, 0.05, 0.06, 0.07,
0.08, 0.09, 0.1, 0.12, 0.14, 0.16, 0.2]
minx = np.min(birefringences)
maxx = np.max(birefringences)
miny = np.min(thicknesses)
xscaler = (xlims[1]-xlims[0])/(max(birefringences)-min(birefringences))
for i,bl in enumerate(biref_label):
    xval = bl*xscaler
    ax.plot((xlims[0], xval), ylims, zorder=100, color="black",lw=0.5, alpha=0.5)
    #--- add text
    textrot = 180/np.pi*np.arctan(aspect*(ylims[1]-ylims[0])/(xval-xlims[0]))
    if xval <= xlims[1]:
        ax.text(xval, ylims[1], " "+str(bl), ha="left", va="bottom", rotation=textrot, **textprops)
    else:
        ytext = ylims[0] + ( (xlims[1]-xlims[0])*((ylims[1]-ylims[0])/(xscaler*bl)) )
        ax.text(xlims[1], ytext, " "+str(bl), ha="left", va="bottom", rotation=textrot, **textprops)
#--- adding lines and text for color orders
orders = np.arange(550, xlims[1]+550, 550)
orders_letters = ["I", "II", "III", "IV", "V", "VI", "VII"]
for order, letter in zip(orders, orders_letters):
    if order <= xlims[1]:
        ax.vlines(order, ylims[0], ylims[0]-13, clip_on=False, alpha=0.5, zorder=0, color="red", lw=2)
    ax.text(order-225, -13, letter, color="red", ha="center", va="bottom")
#--- finalize plot (ticks, grid-lines)
yticks = np.arange(ylims[0], ylims[1]+5, 5)
xticks = np.arange(xlims[0], xlims[1]+400, 400)
ax.set_xticklabels(["{:.0f}".format(_) for _ in xticks], rotation=90)
for y in yticks:
    ax.axhline(y, zorder=100, color="black",lw=0.5, alpha=0.5)
ax.set_yticks(yticks)
ax.set_xticks(xticks)
xminorticks = np.arange(xlims[0], xlims[1], 100)
ax.set_xticks(xminorticks, minor=True)
ax.tick_params(axis="both", which="both",direction="out", top="off", right="off")
#--- finalize plot (labels, title)
ax.text(xlims[0], ylims[1]+2, "birefringence\n"+r"$\longrightarrow$", ha="center", va="bottom", **textprops)
ax.text(xlims[0], ylims[0]-4.5, r"path difference [nm]"+"\n"r"$\longrightarrow$", ha="center", va="top", **textprops)
ax.text(xlims[0], ylims[0]-13, r"color order", ha="center", va="bottom", color="red")
ax.set_ylabel(r"sample thickness [$\mathrm{\mu m}$]", **textprops)
plt.title("Calculated Michel-Lévy color chart", y=1.15)
# NOTE: If you're using python 2, you need to declare this as unicode (because of the accent):
#plt.title(u"Calculated Michel-Lévy color chart", y=1.15)
#--- finalize plot (axis-limits)
ax.set_xlim(*xlims)
ax.set_ylim(*ylims)
#--- show and/or save
plt.savefig("calculated_chart.pdf") # <--- uncomment to save
plt.tight_layout()
plt.show()