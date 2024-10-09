import json

def load_data(json_path: str)->dict:
    data = {}
    with open("data.json","r") as f:
        data = json.loads(f.read()) 
    return data

def create_element_html(data:dict, granularity:int|list[int])->str: 
    website_height = f"{int(data['height'])}px"
    website_width = f"{int(data['width'])}px"

    if isinstance(granularity,int):
        GRID_X = granularity
        GRID_Y = granularity
    elif isinstance(granularity,list) or isinstance(granularity,tuple):
        GRID_X = granularity[0]
        GRID_Y = granularity[1]
    else:
        raise ValueError("Granularity can only be int, list[int] or tuple[int]")

    wrapper_div = f"""
    <div id="website_part" style="
        width: {website_width};
        height: {website_height};
        display: grid;
        background-color: #ff96f8AA;
        grid-template-columns: repeat({GRID_X}, 1fr);
        grid-template-rows: repeat({GRID_Y}, 1fr);
    ">
    """

    for i in range(len(data["bounding_boxes"])):
        box = data["bounding_boxes"][i]
        points = box['xywh']
        col_start = int(points[0] * GRID_X) + 1  # X position in grid (1-indexed)
        row_start = int(points[1] * GRID_Y) + 1  # Y position in grid (1-indexed)
        col_width = int(points[2] * GRID_X)  # Width in Grid
        row_height = int(points[3] * GRID_Y)  # Height in Grid

        wrapper_div += f"""
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
    wrapper_div += "</div>"

    return wrapper_div

def main():

    data = load_data("data.json")
    wrapper_div = create_element_html(data,(100,50))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Define the property of the wrapper div for the data elements -->   
    </head>
    <body>
    {wrapper_div}
    </body>
    </html>
    """

    with open("test.html", "w") as f:
        f.write(html_content)

main() # run main function 