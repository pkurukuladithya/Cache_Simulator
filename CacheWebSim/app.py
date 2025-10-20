import streamlit as st
import random
from cache_simulator import Cache

st.set_page_config(page_title="Cache Simulator", layout="wide")
st.title("🖥️ Cache Simulator Web App")

# Sidebar for cache parameters
st.sidebar.header("Cache Configuration")

l1_size = st.sidebar.slider("L1 Cache Size (KB)", 8, 256, 32, step=8)
l1_assoc = st.sidebar.selectbox("L1 Associativity", [1,2,4,8,16], index=2)
l1_block = st.sidebar.slider("L1 Block Size (Bytes)", 8, 128, 64, step=8)
l1_policy = st.sidebar.selectbox("L1 Replacement Policy", ["LRU", "FIFO", "Random"])
l1_cycles = st.sidebar.slider("L1 Access Time (Cycles)", 1, 10, 4)

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

# Run simulation
if st.button("Run Simulation"):
    # Initialize caches
    if l2_enable:
        L2 = Cache(l2_size, l2_block, l2_assoc, l2_policy, l2_cycles, next_level=None)
        L1 = Cache(l1_size, l1_block, l1_assoc, l1_policy, l1_cycles, next_level=L2)
    else:
        L1 = Cache(l1_size, l1_block, l1_assoc, l1_policy, l1_cycles, next_level=None)

    # Access memory
    for addr in addresses:
        L1.access(addr)

    # Metrics
    l1_hr = L1.hits / L1.accesses * 100
    l1_mr = 100 - l1_hr
    l1_amat = (L1.access_cycles + (L1.misses / L1.accesses) * (L1.next_level.access_cycles if l2_enable else mem_cycles))

    st.subheader("Simulation Results")
    st.write(f"✅ **L1 Cache Hit Ratio:** {l1_hr:.2f}%")
    st.write(f"❌ **L1 Cache Miss Ratio:** {l1_mr:.2f}%")
    st.write(f"⏱️ **Approx. Average Memory Access Time (AMAT):** {l1_amat:.2f} cycles")
    
    if l2_enable:
        l2_hr = L2.hits / L2.accesses * 100
        l2_mr = 100 - l2_hr
        st.write(f"✅ **L2 Cache Hit Ratio:** {l2_hr:.2f}%")
        st.write(f"❌ **L2 Cache Miss Ratio:** {l2_mr:.2f}%")
