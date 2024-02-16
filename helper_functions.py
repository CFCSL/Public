import streamlit as st
import pandas as pd


import re
import base64
from io import BytesIO

# Define a function to create a download link
def download_link(df_dict, file_name, file_label='Download Excel file'):
	"""
	Generates a link to download the given pandas DataFrame as an Excel file.

	Parameters:
	- df: pandas DataFrame
	- file_name: str, the name of the downloaded file (without the extension)
	- file_label: str, the label of the download link

	Returns:
	- str, the HTML code for the download link
	"""
	# Create a BytesIO object to write the Excel file to
	excel_buffer = BytesIO()
	with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as w:
		for sheet_name, df in df_dict.items():
			df.to_excel(w, sheet_name=sheet_name, index=False)
	# Convert the Excel file in the BytesIO object to a base64 string
	b64 = base64.b64encode(excel_buffer.getvalue()).decode()
	# Create the download link
	href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}.xlsx">{file_label}</a>'
	return href


collect_numbers = lambda x : [float(i) for i in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", x)  if i != "" ]


#%% Logo and header


def logo():
	logo_css = """
	<style>
		[data-testid="stSidebarNav"] {
			background-image: url(https://raw.githubusercontent.com/CFCSL/Images-in-Public/main/figures/CFC_LOGO_20220510_Negro_jpeg.jpg);
			background-repeat: no-repeat;
			padding-top: 100px;
			background-position: 20px 20px;
			background-size: 300px;
		}
		[data-testid="stSidebarNav"]::before {
			content: "Carlos Fernandez Casado, S.L.";
			margin-left: 40px;
			margin-top: 20px;
			font-size: 20px;
			position: relative;
			top: 50px;
		}
	</style>
	"""
	
	st.markdown(logo_css, unsafe_allow_html=True)
	
def header():
	t1, t2,t3 = st.columns((0.7,1, 1))


	logo_path = "https://raw.githubusercontent.com/CFCSL/Images-in-Public/main/figures/CFC_LOGO_20220510_Negro_jpeg.jpg"
	# Display the image from the URL with a specified width
	
	t2.image(logo_path, width=350)
	
 # Use HTML to center-align the text vertically and add the link
	centered_text_html = """
	<div style="display: flex; align-items: center; height: 100%;">
		<div style="flex:0.8;"></div>  <!-- Create space on the left -->
		<div style="flex: 4; text-align: center;">
			<a href="https://www.cfcsl.com/" target="_blank">https://www.cfcsl.com/</a>
		</div>  <!-- Centered text -->
		<div style="flex: 1;"></div>  <!-- Create space on the right -->
	</div>
	"""
	st.markdown(centered_text_html, unsafe_allow_html=True)


def download_sofistik(df, file_name):
	text1 = '\n'.join([
		"$WIND PRESSURE CORRESPONDS TO THE PEAK VELOCITY \n",
		"$THE MAXIMUM ALLOWED HEIGHT IS 200 [m] \n", 
		"$THE UNIT OF WIND PRESSURE IS IN KILONEWTONS [kN] \n" 
	])

	local_text_z = "\n"
	for i, z in zip(df.z.index, df.z):
		z = round(z, 3)
		local_text_z += f"LET#z({i})  {z}\n"
		#local_text_z = local_text_z.rstrip(", ")

	local_text_qp="\n"
	for i, q in zip(df.qp.index, df.qp):
		q=round(q,3)
		local_text_qp += f"LET#qp({i})  {q}\n"
	#local_text_qp=local_text_qp.rstrip(", ")
		
	text3= "LET#qp_func 'TAB(z,qp)'"
	
	# Concatenate the existing text and the DataFrame
	combined_text = text1 + local_text_z + local_text_qp +"\n\n"+ text3
	
	
	# Create a BytesIO object and write the combined text to it
	text_bytes = combined_text.encode('utf-8')
	buffer = BytesIO()
	buffer.write(text_bytes)
	buffer.seek(0)
	
	 # Create the download link
	b64 = base64.b64encode(buffer.read()).decode()
	href = f'<a href="data:text/plain;base64,{b64}" download="{file_name}_SOFISTIK.dat">Download Sofistik dat</a>'
	st.markdown(href, unsafe_allow_html=True)
	
