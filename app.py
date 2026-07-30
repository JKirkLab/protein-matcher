import io

import pandas as pd
import streamlit as st

import src.plots as vplt
import src.process_sheets as ps
import src.outputs as out

st.title("Protein Overlap Viewer")

uploaded_files = st.file_uploader(
    "Upload two or three proteomics Excel files",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
)

if not uploaded_files:
    st.stop()

if len(uploaded_files) < 2 or len(uploaded_files) > 3:
    st.error("Please upload exactly 2 or 3 files.")
    st.stop()

dfs = [pd.read_excel(f) for f in uploaded_files]
labels = [f.name.rsplit(".", 1)[0] for f in uploaded_files]

set_list = ps.generate_sets(dfs)
overlap = ps.find_intersection(set_list)

res_lists = out.merge_metrics(overlap,dfs)

filtered_dfs = out.filter_metrics(res_lists)

fig = vplt.plot_venn(overlap, labels=labels, title="Accession overlap")
st.pyplot(fig)

st.subheader("Download filtered data")
for (indices, _), filtered_df in zip(overlap.items(), filtered_dfs):
    region_label = " ∩ ".join(labels[i] for i in indices)
    only = set(range(len(labels))) - set(indices)
    display_name = region_label + (" only" if only else " (all)")
    file_name = "_".join(labels[i] for i in indices) + ("_only" if only else "_shared")

    buf = io.BytesIO()
    filtered_df.to_excel(buf, index=False)
    buf.seek(0)

    st.download_button(
        label=f"Download: {display_name}",
        data=buf,
        file_name=f"{file_name}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    with st.expander(display_name):
        st.dataframe(filtered_df)

