import requests
import json
import pandas as pd
import os
from shapely.geometry import Polygon, MultiPolygon

# Base URL
base_url = "https://lsa4.geohub.sa.gov.au/server/rest/services/LSA/LocationSAViewerV24/MapServer/124/query"

# Starting and ending OBJECTID
start_objectid = 0
end_objectid = 1122269
increment = 999

# Define the columns to include in the CSV
required_columns = [
    'objectid', 'plan_t', 'plan', 'parcel_t', 'parcel_subtype', 'parcel',
    'title_t', 'volume', 'folio', 'qualifier', 'floor_level', 'date_from',
    'parcel_id', 'accuracy_code', 'improved', 'dcdbid', 'planparcel',
    'st_area(shape)', 'st_perimeter(shape)', 'geometry'
]

# Output file
output_file = "29th_output.csv"

# Step 1: Loop through the OBJECTID range
for objectid in range(start_objectid, end_objectid + 1, increment):
    # Update URL parameters
    params = {
        "where": f"OBJECTID>{objectid}",
        "outFields": "*",
        "resultRecordCount": "999",
        "f": "json"
    }
    
    # Fetch data
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        rows = []
        for feature in data.get('features', []):
            # Extract attributes
            attributes = feature.get('attributes', {})
            # Add geometry as a JSON string
            rings = feature.get('geometry', {}).get('rings', [])
            if rings:
                try:
                    # Create polygons from rings
                    polygons = [Polygon(ring) for ring in rings]
                    if len(polygons) == 1:
                        geometry = polygons[0]  # Single polygon
                    else:
                        geometry = MultiPolygon(polygons)  # Multiple polygons
                    attributes['geometry'] = geometry.wkt  # Store as WKT (Well-Known Text)
                except Exception as e:
                    print(f"Error processing geometry for OBJECTID={attributes.get('objectid')}: {e}")
                    attributes['geometry'] = None
            else:
                attributes['geometry'] = None            # Include only required columns
            row = {col: attributes.get(col, None) for col in required_columns}
            rows.append(row)
        
        # Convert current batch to DataFrame
        batch_df = pd.DataFrame(rows, columns=required_columns)

        # Append or create CSV
        if os.path.exists(output_file):
            batch_df.to_csv(output_file, mode='a', index=False, header=False)  # Append to existing file
        else:
            batch_df.to_csv(output_file, index=False)  # Create new file
        print(f"Processed objectIds={objectid} successfully and saved to CSV.")
    else:
        print(f"Failed to fetch data for objectIds={objectid}: {response.status_code}")

print("All data successfully processed and saved.")