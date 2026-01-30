import wx
import sys
import threading
import psutil

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class Window(wx.Frame):
        def __init__(self, title):
                super().__init__(parent=None, title=title)
                self.panel = wx.Panel(self)

                self.menubar = wx.MenuBar()

#--------------------Status Bar--------------------#

                self.status = wx.Menu()
                self.menubar.Append(self.status, "Status")

                networkDia = self.status.Append(wx.ID_ABOUT, "Network", "Open Network Diagnostics")
                componentDia = self.status.Append(wx.ID_ABOUT, "Component", "Open Component Diagnostics")

#---------------------Test Bar---------------------#
        
                self.tests = wx.Menu()
                self.menubar.Append(self.tests, "Tests")

                pingTest = self.tests.Append(wx.ID_FILE, "Ping Test", "Test Connection to Any IP")
                ddosTest = self.tests.Append(wx.ID_FILE, "DDoS Detect", "Checks Network for Malicious Activity")

#---------------------CPU Graph---------------------#    

                self.figure = Figure(figsize=(3,3),layout="constrained", facecolor="none")
                self.canvas = FigureCanvas(self.panel, -1, self.figure)
                self.canvas.SetBackgroundColour(self.panel.GetBackgroundColour())
                self.canvas.SetMinSize((288, 288))
                self.canvas.SetMaxSize((288, 288))
                self.ax = self.figure.add_subplot(111)
                self.ax.set_facecolor("none")

                self.ax.set_aspect("equal", adjustable="box")
                self.ax.axis("off")

                self.used = 0
                self.free = 100
                self.cpu = 0

                wedges, _ = self.ax.pie(
                        [self.free, self.used],
                        startangle=0,
                        counterclock=True,
                        wedgeprops=dict(width=0.3),
                        colors=['purple', 'black']
                )

                self.used_wedge = wedges[0]
                self.free_wedge = wedges[1]
                
                self.text_obj = self.ax.text(
                        0, 0,
                        f"{self.used}%",
                        ha="center",
                        va="center",
                        fontsize=24,
                        weight="bold",
                        color="white"
                )
                
                self.figure.suptitle("CPU", fontsize=24, fontweight="bold", color="white")

                self.timer = wx.Timer(self)
                self.Bind(wx.EVT_TIMER, self.update_cpu)
                self.timer.Start(1000)

                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(self.canvas, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 20)
                sizer.AddStretchSpacer()
                self.panel.SetSizer(sizer)

#---------------------Show GUI---------------------#     

                self.SetMenuBar(self.menubar)
                self.SetSize(1000, 800)
                self.Centre()
                self.Show()
                
#--------------------Update CPU--------------------#   

        def update_cpu(self, event):
                self.cpu = psutil.cpu_percent()
                self.used = self.cpu
                self.free = 100 - self.cpu

                self.used_wedge.set_theta2(90)
                self.used_wedge.set_theta1(90 - (self.used) / 100 * 360)

                self.free_wedge.set_theta2(90 - (self.used) / 100 * 360)
                self.free_wedge.set_theta1(90)

                self.text_obj.set_text(f"{self.cpu:.0f}%")

                self.canvas.draw_idle()

#----------------------Run UI----------------------# 

def start_ui():

        app = wx.App()
        window = Window("Python Utility Program (PUP)")
        app.MainLoop()
