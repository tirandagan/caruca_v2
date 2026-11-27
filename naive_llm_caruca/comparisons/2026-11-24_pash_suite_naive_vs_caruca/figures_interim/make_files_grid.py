import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
cmds=["cat","sed","col","tr","sort","uniq","comm"]
rows=[("PaSh's own files","#4a4a4a",{"cat","sed","col","tr","sort","uniq","comm"}),
      ("Naive LLM's files","#2f7fd6",{"cat","sed","col","sort","uniq","comm"}),
      ("Caruca's files (both grammars)","#e8622b",{"cat","sort"})]
fig,ax=plt.subplots(figsize=(6.5,2.6),dpi=300)
for r,(name,col,have) in enumerate(rows):
    for c,cmd in enumerate(cmds):
        filled=cmd in have
        ax.add_patch(Rectangle((c,2-r),0.9,0.8,facecolor=col if filled else "white",edgecolor=col,linewidth=1.5))
        ax.text(c+0.45,2-r+0.4,"has files" if filled else "PaSh's\nown",ha="center",va="center",fontsize=6.5,color="white" if filled else "#555")
    ax.text(-0.15,2-r+0.4,f"{name}\n({len(have)} of 7)",ha="right",va="center",fontsize=9)
for c,cmd in enumerate(cmds): ax.text(c+0.45,2.95,cmd,ha="center",va="bottom",fontsize=10,family="monospace")
ax.set_xlim(-3.2,7); ax.set_ylim(-0.1,3.4); ax.axis("off")
ax.set_title("Which of the script's seven commands each source has its own annotation files for",fontsize=9.5,loc="left",x=-0.42)
plt.tight_layout(); plt.savefig("figures_interim/files_grid.png",bbox_inches="tight"); print("ok")
