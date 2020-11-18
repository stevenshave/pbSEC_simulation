"""
Plot pbSEC rounds, pKd vs concentration

"""

import numpy as np
from pbSEC_equations import pbSEC_simulate_n_rounds
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

XAXIS_BEGINNING = 3  # pKD of 3 is 1 mM
XAXIS_END = 9  # pKD of 12 is 1 pM
NUM_POINTS_ON_XAXIS = 200  # Publication used 2000 pts along X
PROTEIN_CONC = 10.0
LIGAND_CONC = 8.0  # Singular compound conc in pool
NUM_ROUNDS = 1
RECOVERY_EFFICIENCY_START = 0
RECOVERY_EFFICIENCY_END = 100
recovery_efficiencies = np.linspace(
    RECOVERY_EFFICIENCY_START, RECOVERY_EFFICIENCY_END, num=10
)


x_axis = np.linspace(XAXIS_BEGINNING, XAXIS_END, NUM_POINTS_ON_XAXIS)
ligand_kd_range = 10 ** (-x_axis) * 1e6
protein_concs = np.full(
    (NUM_ROUNDS, recovery_efficiencies.shape[0], NUM_POINTS_ON_XAXIS), np.nan
)

for recovery_efficiency_i, recovery_efficiency in enumerate(recovery_efficiencies):
    for kd_i, kd in enumerate(ligand_kd_range):
        protein_concs[:, recovery_efficiency_i, kd_i] = pbSEC_simulate_n_rounds(
            PROTEIN_CONC,
            LIGAND_CONC,
            kd,
            NUM_ROUNDS,
            recovery_efficiency=recovery_efficiency,
        )
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

protein_concs *= 1e-2

X, Y = np.meshgrid(x_axis, recovery_efficiencies)
Z = np.full(X.shape, np.nan)
for round in reversed(range(NUM_ROUNDS)):
    for i in range(x_axis.shape[0]):
        for j in range(recovery_efficiencies.shape[0]):
            Z[j][i] = protein_concs[round, j, i]
    ax.plot_surface(X, Y, Z, label="Round " + str(round + 1))

# ax.hlines(1,3,9)
ax.set_xticklabels(["3 (mM)", "4", "5", r"6 ($\mathrm{\mu}$M)", "7", "8", "9 (nM)"])
# ax.set_xticks(range(XAXIS_BEGINNING, XAXIS_END+1))
ax.set_xlim(3, 9)
# ax.set_ylim(0, 8)
ax.set_xlabel(r"Ligand pK$_\mathrm{D}$", fontsize=16)
ax.set_ylabel(r"Recovery efficiency (%))", fontsize=16)
ax.set_zlabel(r"[Ligand] ($\mathrm{\mu}$M)", fontsize=16)
ax.set_title(
    "pbSEC kinetic scheme, [Prot] = 10 $\mathrm{\mu}$M, [Ligand] = 8 $\mathrm{\mu}$M"
)
plt.show()
