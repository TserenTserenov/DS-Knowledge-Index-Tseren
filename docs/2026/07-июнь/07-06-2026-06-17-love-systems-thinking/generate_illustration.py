"""
Illustration for the post "What is love from systems thinking perspective"
Visual idea: two circles (persons A and B) with a larger enclosing ellipse (Pair system).
Inside: three characteristic axes + arrows showing emergent properties.
Color palette: warm/soft, readable in club context.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Ellipse, FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#FDF6F0')
ax.set_facecolor('#FDF6F0')

# ---- color palette ----
C_PERSON = '#E8C4A0'
C_PERSON_BORDER = '#C98B5A'
C_PAIR = '#F5DDD0'
C_PAIR_BORDER = '#C97C5A'
C_TEXT_DARK = '#3D2B1F'
C_TEXT_MID = '#6B4C3B'
C_ARROW = '#C97C5A'
C_AXIS_BOX = '#FAE5D3'
C_AXIS_BORDER = '#D4956A'
C_EMERG = '#A8D5BA'
C_EMERG_BORDER = '#5C9E78'

# ---- Pair system (large ellipse, background) ----
pair_ellipse = Ellipse(
    xy=(5, 3.5), width=8.8, height=5.2,
    angle=0,
    linewidth=2.5, edgecolor=C_PAIR_BORDER,
    facecolor=C_PAIR, zorder=1, linestyle='--'
)
ax.add_patch(pair_ellipse)
ax.text(5, 6.25, 'Надсистема «Пара»', ha='center', va='center',
        fontsize=13, color=C_TEXT_DARK, fontweight='bold',
        fontfamily='DejaVu Sans')
ax.text(5, 5.85, '(держится на устойчивых связях, а не на чувстве)',
        ha='center', va='center', fontsize=8.5, color=C_TEXT_MID,
        fontfamily='DejaVu Sans')

# ---- Person A (left circle) ----
circA = plt.Circle((2.5, 3.2), 1.3,
                   color=C_PERSON, ec=C_PERSON_BORDER, lw=2.5, zorder=2)
ax.add_patch(circA)
ax.text(2.5, 3.55, 'Человек А', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_TEXT_DARK,
        fontfamily='DejaVu Sans', zorder=3)
ax.text(2.5, 3.05, 'состояние', ha='center', va='center',
        fontsize=9, color=C_TEXT_MID, fontstyle='italic',
        fontfamily='DejaVu Sans', zorder=3)
ax.text(2.5, 2.65, 'любви', ha='center', va='center',
        fontsize=9, color=C_TEXT_MID, fontstyle='italic',
        fontfamily='DejaVu Sans', zorder=3)

# ---- Person B (right circle) ----
circB = plt.Circle((7.5, 3.2), 1.3,
                   color=C_PERSON, ec=C_PERSON_BORDER, lw=2.5, zorder=2)
ax.add_patch(circB)
ax.text(7.5, 3.55, 'Человек Б', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_TEXT_DARK,
        fontfamily='DejaVu Sans', zorder=3)
ax.text(7.5, 3.05, 'состояние', ha='center', va='center',
        fontsize=9, color=C_TEXT_MID, fontstyle='italic',
        fontfamily='DejaVu Sans', zorder=3)
ax.text(7.5, 2.65, 'любви', ha='center', va='center',
        fontsize=9, color=C_TEXT_MID, fontstyle='italic',
        fontfamily='DejaVu Sans', zorder=3)

# ---- Connecting arrows (links/interactions between persons) ----
arrow_props = dict(arrowstyle='<->', color=C_ARROW, lw=2.2,
                   connectionstyle='arc3,rad=0.25')
ax.annotate('', xy=(6.2, 3.5), xytext=(3.8, 3.5),
            arrowprops=arrow_props, zorder=4)
ax.text(5.0, 3.75, 'связи и взаимодействия', ha='center', va='center',
        fontsize=8.5, color=C_ARROW, fontweight='bold',
        fontfamily='DejaVu Sans', zorder=5)

# second arrow below
arrow_props2 = dict(arrowstyle='<->', color=C_ARROW, lw=1.5,
                    connectionstyle='arc3,rad=-0.25')
ax.annotate('', xy=(6.2, 2.9), xytext=(3.8, 2.9),
            arrowprops=arrow_props2, zorder=4)
ax.text(5.0, 2.45, 'общие дела, договорённости, опора', ha='center', va='center',
        fontsize=8, color=C_TEXT_MID, fontstyle='italic',
        fontfamily='DejaVu Sans', zorder=5)

# ---- Three characteristic axes (bottom boxes) ----
boxes = [
    (1.5, 1.05, 'ДЕЛАЕТ', 'внимание, ресурсы,\nдолгосрочный план'),
    (5.0, 1.05, 'ЧУВСТВУЕТ', 'чувствительность\nк другому, тяга'),
    (8.5, 1.05, 'КАКИМ СТАНОВИТСЯ', '«мы», расширение\nцелей, агентность↑'),
]
for bx, by, title, desc in boxes:
    box = FancyBboxPatch((bx - 1.25, by - 0.62), 2.5, 1.1,
                         boxstyle='round,pad=0.08',
                         facecolor=C_AXIS_BOX, edgecolor=C_AXIS_BORDER,
                         lw=1.5, zorder=2)
    ax.add_patch(box)
    ax.text(bx, by + 0.3, title, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=C_TEXT_DARK,
            fontfamily='DejaVu Sans', zorder=3)
    ax.text(bx, by - 0.17, desc, ha='center', va='center',
            fontsize=7.8, color=C_TEXT_MID,
            fontfamily='DejaVu Sans', zorder=3)

# label for the boxes row
ax.text(5.0, 1.85, 'Характеристики состояния «человек в любви»',
        ha='center', va='center', fontsize=9, color=C_TEXT_MID,
        fontfamily='DejaVu Sans')

# ---- Emergent properties badge (top right of pair) ----
emerg = FancyBboxPatch((7.9, 4.4), 1.7, 0.95,
                       boxstyle='round,pad=0.08',
                       facecolor=C_EMERG, edgecolor=C_EMERG_BORDER,
                       lw=1.5, zorder=6)
ax.add_patch(emerg)
ax.text(8.75, 4.97, 'Эмерджентность:', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#2D6B47',
        fontfamily='DejaVu Sans', zorder=7)
ax.text(8.75, 4.68, 'возможности пары >', ha='center', va='center',
        fontsize=7.8, color='#2D6B47', fontfamily='DejaVu Sans', zorder=7)
ax.text(8.75, 4.45, 'сумма частей', ha='center', va='center',
        fontsize=7.8, color='#2D6B47', fontfamily='DejaVu Sans', zorder=7)

# arrow from pair to emergent badge
ax.annotate('', xy=(7.95, 4.7), xytext=(7.0, 4.1),
            arrowprops=dict(arrowstyle='->', color=C_EMERG_BORDER, lw=1.5),
            zorder=5)

# ---- Two-axis note for "opposite of love" ----
ax.text(0.3, 0.38, 'Оси противоположности:', ha='left', va='center',
        fontsize=8, fontweight='bold', color=C_TEXT_MID,
        fontfamily='DejaVu Sans')
ax.text(0.3, 0.15, 'значимость → безразличие  |  знак связи → ненависть',
        ha='left', va='center', fontsize=7.8, color=C_TEXT_MID,
        fontfamily='DejaVu Sans')

plt.tight_layout(pad=0.3)
out_path = 'illustration.png'
plt.savefig(out_path, dpi=150, bbox_inches='tight',
            facecolor='#FDF6F0')
print(f'Saved: {out_path}')
