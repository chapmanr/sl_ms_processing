import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from io import StringIO
import sys
sys.path.append('../')

import ms_logic.gh_xic_data_reader as xdr


class XiCViewer:

    def render(self):
        print("render")
        self.cmap = st.sidebar.selectbox("Color Map", ["viridis", "plasma", "inferno", "magma"])
        self.select_file = st.sidebar.file_uploader("Upload RTE file" , "xyi")
        self.run_button = st.sidebar.button("Run With Demo Data")

    def draw_xic(self, df:pd.DataFrame):
        print("Draw xic")

        x = [float(xs) for xs in df["x"].to_list()]
        y = [float(ys) for ys in df["y"].to_list()]
        
        for i in range(4, len(df.columns)+1):
            fig, axes = plt.subplots(1, 1)
            key_str = "m"+str(i-3) 
            t = [float(ts) for ts in df[key_str].to_list()]
            axes.scatter(x, y, c=t, cmap=self.cmap, marker="s")#, s=5)
            st.pyplot(fig)

    def draw_xic(self, reader : xdr.RTEParser):
        print("draw single")

        num_masses = len(reader.masses)
        df = reader.df
        
        x = [float(xs) for xs in df["x"].to_list()]
        y = [float(ys) for ys in df["y"].to_list()]
        ui_cols = st.columns(num_masses)
        for mass_num in range(0, num_masses):
                with ui_cols[mass_num]:
                    t = [float(ts) for ts in df["m"+str(mass_num + 1)].to_list()]
                    fig, axes = plt.subplots(1, 1)
                    axes.set_axis_off()    
                    axes.get_xaxis().set_visible(False)
                    axes.get_yaxis().set_visible(False)
                    axes.scatter(x, y, c=t, cmap=self.cmap, marker="s")#, s=5)                    
                    st.pyplot(fig)

    def checks(self):
        print("checks")
        if self.select_file is not None:     
            rte_parser = xdr.RTEParser(xdr.get_data_lines_from_file_obj(self.select_file))
            self.draw_xic(rte_parser)
        
        if self.run_button:
            rte_parser = xdr.RTEParser(xdr.get_defaut_data_lines())  
            self.draw_xic(rte_parser)
        
        
    def run(self):
        print("run")
        self.render()
        self.checks()




if __name__=="__main__":
    xicPage = XiCViewer()
    xicPage.run()