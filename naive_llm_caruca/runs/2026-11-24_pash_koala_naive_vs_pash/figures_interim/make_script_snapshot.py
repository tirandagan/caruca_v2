import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
src=open("figures_interim/spell.sh.txt").read().rstrip("\n").splitlines()
src=[l for l in src if l.strip()!="" or True]
fig,ax=plt.subplots(figsize=(3.4,0.3*len(src)+0.7),dpi=300); ax.axis("off")
ax.text(0.02,0.98,"spell.sh  (Koala, oneliners)",fontsize=9.5,fontweight="bold",va="top",ha="left",family="monospace",transform=ax.transAxes)
ax.text(0.02,0.86,"\n".join(src),fontsize=8.5,va="top",ha="left",family="monospace",transform=ax.transAxes,linespacing=1.35)
fig.patch.set_facecolor("#f6f6f4")
plt.savefig("figures_interim/spell_snapshot.png",bbox_inches="tight",facecolor=fig.get_facecolor()); print("snapshot ok")
