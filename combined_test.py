from threading import Thread
import graphicUI as gui
import Path_det_ball_track_fin as pbt


path = Thread(target=pbt.main, daemon=True)
path.start()
 
graphic = Thread(target=gui.main, daemon=True)
graphic.start()