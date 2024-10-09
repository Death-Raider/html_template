import json

data = {}
with open("data.json","r") as f:
    data = json.loads(f.read()) 

website_height = f"{data['height']}px"
website_width = f"{data['width']}px"
GRID_X = 100
GRID_Y = 100

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Define the property of the wrapper div for the data elements -->   
    <style>
        #website_part {{
            width: {website_width};
            height: {website_height};
            display: grid;
            background-color: #ff96f8AA;
            grid-template-columns: repeat({GRID_X}, 1fr);
            grid-template-rows: repeat({GRID_Y}, 1fr);
        }}
    </style>
</head>
<body>
    <div id="website_part">
"""

for i in range(len(data["bounding_boxes"])):
    box = data["bounding_boxes"][i]
    points = box['xywh']
    col_start = int(points[0] * GRID_X) + 1  # X position in grid (1-indexed)
    row_start = int(points[1] * GRID_Y) + 1  # Y position in grid (1-indexed)
    col_width = int(points[2] * GRID_X)  # Width in Grid
    row_height = int(points[3] * GRID_Y)  # Height in Grid

    html_content += f"""
        <{box['class']} style="
            grid-column: {col_start} / span {col_width};
            grid-row: {row_start} / span {row_height};
            background-color: {box['color']};
            overflow: hidden;
            height: 100%;
            width: 100%;
            margin: 0 auto;
            padding: 0;
        ">
            {box['data']}
        </{box['class']}>
    """

html_content += """
    </div>
</body>
</html>
"""

with open("test.html", "w") as f:
    f.write(html_content)