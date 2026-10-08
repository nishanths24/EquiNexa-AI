import os

pages = [
    "Dashboard", "Markets", "ChartWorkspace", "AIAnalyst", "News", "Forex", 
    "Macro", "Screener", "Watchlist", "Alerts", "Portfolio", "Profile", 
    "Settings", "Admin"
]

template = """import React from 'react';

const {name} = () => {
  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-6">
      <h1 className="text-2xl font-bold mb-4">{name}</h1>
      <div className="bg-card-bg border border-border-subtle rounded-lg p-6 flex-1 flex items-center justify-center">
        <p className="text-text-muted">V2 {name} Component - Development in Progress</p>
      </div>
    </div>
  );
};

export default {name};
"""

base_dir = r"c:\Users\nisha\OneDrive\Desktop\EquiNexa AI\frontend\src\pages"

for p in pages:
    path = os.path.join(base_dir, f"{p}.tsx")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(template.replace("{name}", p))
            
print("Pages generated.")
