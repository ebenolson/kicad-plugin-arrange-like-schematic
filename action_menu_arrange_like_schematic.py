import pcbnew
import re
import datetime
import json

import Tkinter
from tkFileDialog import askopenfilename

class ArrangeLikeSchematic(pcbnew.ActionPlugin):
    def defaults( self ):
        self.name = "Arrange like schematic"
        self.category = "Modify PCB"
        self.description = "Arrange components so that layout is similar to schematic"

    def get_sch_filename(self):
        root = Tkinter.Tk()
        root.update()
        filename = askopenfilename(
            initialdir = "~",
            title = "Select file",
            filetypes = (("sch files","*.sch"),("all files","*.*")),
        )
        root.update()
        root.destroy()
        root.mainloop()
        return filename

    def get_component_positions(self, fn):
        import sch
        positions = {}
        s = sch.Schematic(fn)
        for c in s.components:
            ref = c.labels['ref']
            positions[ref] = c.position
        return positions

    def Run( self ):
        fn = self.get_sch_filename()
        positions = self.get_component_positions(fn)
        pcb = pcbnew.GetBoard()
        components = pcb.GetModules()
        for c in components:
            ref = c.GetReference()
            if ref in positions:
                x, y = int(positions[ref]['posx'])*25.4/1000, int(positions[ref]['posy'])*25.4/1000
                c.SetPosition(pcbnew.wxPointMM(x, y))

ArrangeLikeSchematic().register()