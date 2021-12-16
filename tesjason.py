''''
Nama: Dezatama Thabay iwary
NIM: 12219060
'''
# import library
import streamlit as st
import pandas as pd
import numpy as np
import json
import csv
from bokeh.plotting import figure, show

#inisiasi variabel untuk membangun dataframe utama
kode_negara=list()
region=list()
sub_region=list()
nama__negara=list()
DataFrame_minyak=list()
negara=list()

#mengambil data dari json
with open("kode_negara_lengkap.json") as f:
    data=json.load(f)
    for line in data:
        kode_negara.append(line["alpha-3"])
        nama__negara.append(line["name"])
        region.append(line["region"])
        sub_region.append(line["sub-region"])

#mengambil data dari csv dan melakukan filtrasi kode negara
with open("produksi_minyak_mentah.csv") as c:
    minyak=csv.reader(c, delimiter=",")
    for line in minyak:
        for i in range(len(kode_negara)):
            if line[0] == kode_negara[i]:
                isi=dict()
                isi["kode"]=line[0]
                isi["name"]=nama__negara[i]
                isi["region"]=region[i]
                isi["sub-region"]=sub_region[i]
                isi["tahun"]=line[1]
                isi["produksi"]=float(line[2])
                DataFrame_minyak.append(isi)
                break
for line in DataFrame_minyak:
    if line["name"] not in negara:
        negara.append(line["name"])

#membangun dataframe utama
Data_minyak=pd.DataFrame(DataFrame_minyak)

#memasukkan pilihan negara dari user
negara_input=st.selectbox("Pilih nama negara untuk di plot",negara)

#ploting fungsi wajib a
header1="Produksi Minyak Negara " +negara_input+" dari tahun ke tahun"
data_sorted=Data_minyak.loc[Data_minyak.name == negara_input]
plot_1= figure(title=header1, x_axis_label='Tahun', y_axis_label='Jumlah Produksi')
plot_1.line(data_sorted["tahun"], data_sorted["produksi"], legend_label="Temp.", line_width=2)
st.subheader(header1)
st.bokeh_chart(plot_1)

#input B negara dan T tahun
tahun_input=str(st.number_input('Pilih Tahun Produksi', 1971,2015))
jumlah_negara_input=int(st.number_input("Jumlah Negara",1,100))
header2="Produksi "+str(jumlah_negara_input)+" besar negara pada tahun "+tahun_input
header3="Produksi "+str(jumlah_negara_input)+" besar negara secara kumulatif"

#filter data untuk ploting fungsi wajib b
data_sorted_tahun=Data_minyak.loc[Data_minyak.tahun == tahun_input]
data_sorted_tahun=data_sorted_tahun.sort_values(["produksi"],ascending=False)
data_sorted_tahun=data_sorted_tahun[0:jumlah_negara_input]

#plotting fungsi wajib b
plot2 = figure(x_range=data_sorted_tahun["name"], height=350, title=header2,
           toolbar_location=None, tools="",x_axis_label='Nama Negara', y_axis_label='Jumlah Produksi tahun '+str(tahun_input))

plot2.vbar(x=data_sorted_tahun["name"], top=data_sorted_tahun["produksi"], width=0.9)

plot2.xgrid.grid_line_color = None
plot2.y_range.start = 0
st.subheader(header2)
st.bokeh_chart(plot2)

#filter data untuk ploting fungsi wajib c
minyak_kumulatif =  Data_minyak.groupby(['name'],as_index=False).produksi.sum()
minyak_kumulatif=minyak_kumulatif.nlargest(jumlah_negara_input, 'produksi', keep='first')

#ploting fungsi wajib c
plot3 = figure(x_range=minyak_kumulatif["name"], height=350, title=header3,
           toolbar_location=None, tools="",x_axis_label='Nama Negara', y_axis_label='Jumlah Produksi kumulatif')
plot3.vbar(x=minyak_kumulatif["name"], top=minyak_kumulatif["produksi"], width=0.9)
plot3.xgrid.grid_line_color = None
plot3.y_range.start = 0
st.subheader(header3)
st.bokeh_chart(plot3)

#filtering awal data untuk fungsi wajib d 
data_kumulatif=Data_minyak.groupby(['name'],as_index=False).produksi.sum()
data_kumulatif=data_kumulatif.values.tolist()

for line in DataFrame_minyak:
    for i in data_kumulatif:
        if i[0]==line["name"]:
            line["produksi kumulatif"]=i[1]
            break

data_final=pd.DataFrame(DataFrame_minyak)

#memisah data yang produksinya ada nol dan tidak
data_final_tanpa_zero= data_final[data_final['produksi'] != 0]
data_final_zero= data_final[data_final['produksi'] == 0]

#negara terbesar produksi pada tahun B
data_terbesar=data_final_tanpa_zero.loc[data_final_tanpa_zero.tahun == tahun_input]
data_terbesar=data_terbesar.sort_values(["produksi"],ascending=False)
data_terbesar=data_terbesar[0:1]

#negara terbesar produksi pada tahun B
data_terkecil=data_final_tanpa_zero.loc[data_final_tanpa_zero.tahun == tahun_input]
data_terkecil=data_terkecil.sort_values(["produksi"],ascending=True)
data_terkecil=data_terkecil[0:1]

#negara dengan produksi 0 pada tahun n
data_zero=data_final_zero.loc[data_final_zero.tahun == tahun_input]

if st.checkbox('Perlihatkan Negara yang memiliki produksi minyak terbesar pada tahun '+str(tahun_input)):
    st.subheader('Negara dengan produksi minyak terbesar pada tahun '+str(tahun_input))
    st.write(data_terbesar)

if st.checkbox('Perlihatkan Negara yang memiliki produksi minyak terkecil pada tahun '+str(tahun_input)):
    st.subheader('Negara dengan produksi minyak terkecil pada tahun '+str(tahun_input))
    st.write(data_terkecil)

if st.checkbox('Perlihatkan Negara yang memiliki produksi minyak 0 pada tahun '+str(tahun_input)):
    st.subheader('Negara dengan produksi minyak 0 pada tahun '+str(tahun_input))
    st.write(data_zero)