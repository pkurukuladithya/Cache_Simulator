Cache Simulator Web App
=======================

Project Name: CacheWebSim
Description:
-------------
A web-based interactive cache simulator built with Python and Streamlit. 
It allows users to simulate single-level (L1) and multi-level (L1 + L2) cache architectures, 
explore replacement policies, and analyze performance metrics like hit ratio, miss ratio, and average memory access time (AMAT).

Features:
---------
- Fully configurable cache parameters: size, block size, associativity, replacement policy, and access cycles.
- Multi-level caching support (L1 + optional L2).
- Interactive sliders and dropdowns for user-friendly configuration.
- Choice of memory access patterns: Random or Sequential.
- Real-time calculation of:
  - L1 and L2 Hit Ratio
  - L1 and L2 Miss Ratio
  - Approximate AMAT
- Easy to extend for visual cache block simulation and advanced analytics.

Requirements:
-------------
- Python 3.8+
- Streamlit
- NumPy
- Matplotlib / Plotly (optional)

Install dependencies:
---------------------
pip install -r requirements.txt

Installation and Setup:
-----------------------
1. Clone or download the project folder.
2. Navigate to the project directory:
   cd CacheWebSim
3. (Optional) Create a virtual environment:
   python -m venv venv
   # Activate the environment
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
4. Install dependencies:
   pip install -r requirements.txt

Running the App:
----------------
1. Run the Streamlit app using:
   streamlit run app.py
2. A browser window/tab will open automatically.
3. Use the sidebar to adjust cache parameters (size, block size, associativity, replacement policy, etc.).
4. Select the memory access pattern: Random or Sequential.
5. Click "Run Simulation" to see performance metrics like:
   - L1/L2 Hit Ratio
   - L1/L2 Miss Ratio
   - Average Memory Access Time (AMAT)

File Structure:
---------------
CacheWebSim/
│
├── app.py               # Main Streamlit application
├── cache_simulator.py   # Cache simulation logic
├── requirements.txt     # Python dependencies
└── README.txt           # This file

Simulation Details:
-------------------
- Cache Access Logic: Checks if the requested address is in the cache. On a miss, accesses the next level (L2 or main memory).
- Replacement Policies Supported:
  - LRU (Least Recently Used)
  - FIFO (First-In-First-Out)
  - Random Replacement
- Metrics Calculated:
  - Hit Ratio = Hits / Total Accesses
  - Miss Ratio = 1 – Hit Ratio
  - AMAT = L1 Access Time + (Miss Ratio × Miss Penalty)

Future Improvements:
--------------------
- Add L3 cache visualization for multi-core systems.
- Include real-time cache block display (color-coded hits/misses).
- Use benchmark memory traces instead of random addresses.
- Add graphs of hit ratio vs cache size or associativity.
- Implement write policies (write-back vs write-through).

License:
--------
For educational purposes and academic demonstrations. 
Feel free to modify and extend for personal or research use.
