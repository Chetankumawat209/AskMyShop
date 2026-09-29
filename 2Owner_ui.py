import streamlit as st

st.header("Owner page",text_alignment="center")

work=st.selectbox(index=None,placeholder="Choose",label="Choose option",options=["Add Business","Get Business",'Add Product','Get Products','Get Product_by_name',"Update Product","Delect Product"])

if work:
    match work:
        case "Add Business":
            pass

        case "Get Business":
            pass

        case "Add Product":
            pass

        case "Get Products":
            pass

        case "Get Product_by_name":
            pass

        case "Add Business":
            pass

        case "Update Product":
            pass

        case "Delect Product":
            pass
        
