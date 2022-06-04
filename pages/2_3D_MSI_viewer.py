import streamlit as st

import plotly.express as px
import pandas as pd


import ms_logic.gh_3d_data_reader as xdr
import matplotlib.pyplot as plt


class XiC3DViewer:

    def render(self):
        print("render")
        self.lower_thresh = st.sidebar.number_input("Lower Threshold", value = 2000)
        self.upper_thresh = st.sidebar.number_input("Upper Threshold", value = 40000)
        self.mass_select = st.sidebar.number_input("Mass Selection", min_value=1, max_value=32)
        self.show_all_layers = st.sidebar.checkbox("Show All layers")
        self.layer_of_interest = st.sidebar.number_input("Show Layer", min_value=0, max_value=100)
        self.cmap = st.sidebar.selectbox("Color Map", ["viridis", "plasma", "inferno", "magma"])

        self.opacity = st.sidebar.number_input("Opacity", min_value=0.05, max_value=1.0, value=0.05)
        self.select_file = st.sidebar.file_uploader("Upload 3D file" , "csv")
        self.run_button = st.sidebar.button("Run With Demo Data")
        

    def thresh(self, df:pd.DataFrame, column_name:str) -> pd.DataFrame:
        print("Column Name = " + column_name)
        todrop = df[df[column_name] < self.lower_thresh].index
        df.drop(todrop, inplace=True)
        todrop = df[df[column_name] > self.upper_thresh].index
        df.drop(todrop, inplace=True)
        return df


    def draw_xic(self, df:pd.DataFrame, mass_name:str):
        print("Draw xic")

        layers = df["z"].unique().tolist()
        len_layers = len(layers)
        st.write("layers = " + str(len_layers))
        cols = 4
        rows = round(len_layers / cols) + 1

        #this should write out n rows of 4 images 
        for row_index in range(0, rows):
            columns = st.columns(cols)
            for col_index in range(0, cols):                
                calc_len = (cols * row_index) + col_index
                if calc_len < len_layers:  
                    with columns[col_index]:                        
                        z_df = df[df["z"]==layers[calc_len]]
                        x = [float(xs) for xs in z_df["x"].to_list()]
                        y = [float(ys) for ys in z_df["y"].to_list()]
                        t = [float(ts) for ts in z_df[mass_name].to_list()]
                
                        fig, axes = plt.subplots(1, 1)
                        axes.set_axis_off()    
                        axes.get_xaxis().set_visible(False)
                        axes.get_yaxis().set_visible(False)
                        axes.scatter(x, y, c=t, cmap=self.cmap, marker="s")#, s=5)
                        st.pyplot(fig)


    def draw_from_3d_obj(self, xic3D:xdr.MSI3DXiCParser):
            st.write("Num Masses = " + str(xic3D.NumMasses()))
            mass_name = "m" + str(self.mass_select)


            if mass_name in self.xic3D.df.columns:

                #col1, col2 = st.columns(2)
                df = xic3D.df
                #Now draw the layer of interest                
                #with col2:
                
                if self.show_all_layers==True:
                    self.draw_xic(df, mass_name=mass_name)
                else:
                    z_df = df[df["z"]==self.layer_of_interest]
                    self.draw_xic(z_df, mass_name=mass_name)

                #with col1:
                self.thresh(xic3D.df, mass_name)
                st.write(mass_name + " has " + str(len(df[mass_name].to_list())) + " data points")
                fig = px.scatter_3d(df, x='x', y='y', z='z', color = mass_name, opacity=self.opacity)
                st.plotly_chart(fig, use_container_width=True)

                
            else:
                st.error("No mass " + mass_name + " exists")

            

    def checks(self):
        print("checks")
        if self.select_file is not None:     
            print("Selected Files")
            self.xic3D= xdr.MSI3DXiCParser(xdr.get_data_lines_from_file_obj(self.select_file))
            self.draw_from_3d_obj(self.xic3D)
            
        if self.run_button:
            print("Run with default data")
            self.xic3D= xdr.MSI3DXiCParser(xdr.get_defaut_data_lines())
            self.draw_from_3d_obj(self.xic3D)


    def run(self):
        print("run")
        self.render()
        self.checks()


if __name__=="__main__":
    xicPage = XiC3DViewer()
    xicPage.run()