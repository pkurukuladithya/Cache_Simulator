import streamlit as st
import random
from cache_simulator import Cache

# Configure the page
st.set_page_config(
    page_title="Cache Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        padding: 20px;
        color: #1E88E5;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .team-member {
        padding: 10px 15px;
        border-left: 4px solid #1E88E5;
        margin: 8px 0;
        background-color: #E3F2FD;
        color: #0D47A1;
        font-weight: 500;
        border-radius: 0 4px 4px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .description {
        padding: 20px;
        background-color: #E1F5FE;
        border-radius: 8px;
        margin: 15px 0;
        color: #01579B;
        border: 1px solid #81D4FA;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #1565C0;
    }
    </style>
""", unsafe_allow_html=True)

# Main title and welcome message
st.markdown("<h1 class='main-title'>🖥️ Welcome to Cache Simulator Web App</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>ACOA Final Assignment</h2>", unsafe_allow_html=True)

# Team information
st.markdown("### 👥 Team Members")
st.markdown("<div class='team-member'>🎓 IT23689862 - KURUKULADITHYA H D P</div>", unsafe_allow_html=True)
st.markdown("<div class='team-member'>🎓 IT23690684 - HANSANA K K H</div>", unsafe_allow_html=True)

# Project description
st.markdown("<div class='description'>This web application simulates cache memory behavior and analyzes its performance metrics including hit/miss ratios and Average Memory Access Time (AMAT). Adjust the parameters in the sidebar to explore different cache configurations.</div>", unsafe_allow_html=True)

# Divider
st.markdown("---")

# Sidebar for cache parameters
st.sidebar.markdown("### ⚙️ Cache Configuration")
st.sidebar.markdown("---")

# L1 Cache Configuration
st.sidebar.markdown("#### 🔹 L1 Cache Parameters")
l1_size = st.sidebar.slider("Cache Size (KB)", 8, 256, 32, step=8, 
                          help="Size of L1 cache in kilobytes")
l1_assoc = st.sidebar.selectbox("Associativity", [1,2,4,8,16], index=2,
                               help="Number of ways in set-associative cache")
l1_block = st.sidebar.slider("Block Size (Bytes)", 8, 128, 64, step=8,
                           help="Size of each cache block in bytes")
l1_policy = st.sidebar.selectbox("Replacement Policy", ["LRU", "FIFO", "Random"],
                                help="Policy for replacing cache blocks when cache is full")
l1_cycles = st.sidebar.slider("Access Time (Cycles)", 1, 10, 4,
                            help="Number of CPU cycles needed to access L1 cache")

l2_enable = st.sidebar.checkbox("Enable L2 Cache", value=True)
if l2_enable:
    l2_size = st.sidebar.slider("L2 Cache Size (KB)", 32, 1024, 256, step=32)
    l2_assoc = st.sidebar.selectbox("L2 Associativity", [1,2,4,8,16], index=3)
    l2_block = st.sidebar.slider("L2 Block Size (Bytes)", 8, 128, 64, step=8)
    l2_policy = st.sidebar.selectbox("L2 Replacement Policy", ["LRU", "FIFO", "Random"])
    l2_cycles = st.sidebar.slider("L2 Access Time (Cycles)", 5, 20, 10)

mem_cycles = st.sidebar.slider("Main Memory Latency (Cycles)", 100, 500, 200)

# Generate memory trace
num_accesses = st.sidebar.slider("Number of Memory Accesses", 1000, 10000, 5000, step=1000)
trace_type = st.sidebar.radio("Memory Access Pattern", ["Random", "Sequential"], index=0)

# Generate addresses
if trace_type == "Random":
    addresses = [random.randint(0, 0xFFFFF) for _ in range(num_accesses)]
else:  # Sequential
    addresses = [i*4 for i in range(num_accesses)]

# Simulation section
st.markdown("### 🚀 Simulation Control")
col1, col2 = st.columns([3, 1])
with col1:
    st.info("Click the button below to run the cache simulation with the current configuration.")
with col2:
    simulate = st.button("▶️ Run Simulation", use_container_width=True)

if simulate:
    with st.spinner("Running simulation..."):
        # Initialize caches
        if l2_enable:
            L2 = Cache(l2_size, l2_block, l2_assoc, l2_policy, l2_cycles, next_level=None)
            L1 = Cache(l1_size, l1_block, l1_assoc, l1_policy, l1_cycles, next_level=L2)
        else:
            L1 = Cache(l1_size, l1_block, l1_assoc, l1_policy, l1_cycles, next_level=None)

        # Access memory
        for addr in addresses:
            L1.access(addr)

        # Calculate metrics
        l1_hr = L1.hits / L1.accesses * 100
        l1_mr = 100 - l1_hr
        l1_amat = (L1.access_cycles + (L1.misses / L1.accesses) * (L1.next_level.access_cycles if l2_enable else mem_cycles))

        # Display results in a modern layout
        st.markdown("### 📊 Simulation Results")
        
        # Create three columns for L1 metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="L1 Cache Hit Ratio", 
                     value=f"{l1_hr:.2f}%",
                     delta="Higher is better")
        
        with col2:
            st.metric(label="L1 Cache Miss Ratio",
                     value=f"{l1_mr:.2f}%",
                     delta="Lower is better",
                     delta_color="inverse")
        
        with col3:
            st.metric(label="AMAT (Cycles)",
                     value=f"{l1_amat:.2f}",
                     delta="Lower is better",
                     delta_color="inverse")

        # L2 Cache metrics if enabled
        if l2_enable:
            st.markdown("#### L2 Cache Performance")
            l2_hr = L2.hits / L2.accesses * 100
            l2_mr = 100 - l2_hr
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="L2 Cache Hit Ratio",
                         value=f"{l2_hr:.2f}%",
                         delta="Higher is better")
            with col2:
                st.metric(label="L2 Cache Miss Ratio",
                         value=f"{l2_mr:.2f}%",
                         delta="Lower is better",
                         delta_color="inverse")
            
        # Additional performance insights
        st.markdown("### 🔍 Performance Analysis")
        st.info(f"""
        - Total memory accesses: {num_accesses:,}
        - Access pattern: {trace_type}
        - L1 Cache hits: {L1.hits:,}
        - L1 Cache misses: {L1.misses:,}
        """)
