"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    gap = (width-2*GRAPH_MARGIN_SIZE)//len(YEARS)
    x_coordinate = gap*year_index+GRAPH_MARGIN_SIZE
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    canvas.create_line(0, GRAPH_MARGIN_SIZE, CANVAS_WIDTH, GRAPH_MARGIN_SIZE)
    canvas.create_line(0, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, 0, GRAPH_MARGIN_SIZE, CANVAS_HEIGHT)
    canvas.create_line(CANVAS_WIDTH-GRAPH_MARGIN_SIZE, 0, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, CANVAS_HEIGHT)
    for i in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), 0, get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, anchor=tkinter.NW, text=YEARS[i])


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    gap_height = (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) / 1000
    c = 0
    for name in lookup_names:
        if name in name_data:
            y_r_dict = name_data[name]
            y_r_lst = []
            if c >= len(COLORS):
                c = c - len(COLORS)
            color = COLORS[c]
            c += 1
            for j in range(len(YEARS)):
                if str(YEARS[j]) in y_r_dict:
                    rank = y_r_dict[str(YEARS[j])]
                    y_r_lst.append((YEARS[j], rank))
                else:
                    y_r_lst.append((YEARS[j], 2000))
            for i in range(len(y_r_lst)-1):
                rank1 = int(y_r_lst[i][1])
                rank2 = int(y_r_lst[i+1][1])
                if rank1 > 1000:
                    rank1 = 1000
                    canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i)+TEXT_DX, gap_height * rank1+GRAPH_MARGIN_SIZE,
                                       anchor=tkinter.SW, text=str(name)+'*', fill=color)
                else:
                    canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i)+TEXT_DX, gap_height * rank1+GRAPH_MARGIN_SIZE,
                                       anchor=tkinter.SW, text=(name, rank1), fill=color)
                if rank2 > 1000:
                    rank2 = 1000
                canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), gap_height * rank1 + GRAPH_MARGIN_SIZE,
                                   get_x_coordinate(CANVAS_WIDTH, i+1), gap_height * rank2 + GRAPH_MARGIN_SIZE,
                                   width=LINE_WIDTH, fill=color)

            if rank2 < 1000:
                canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i+1)+TEXT_DX, gap_height * rank2 + GRAPH_MARGIN_SIZE,
                                   anchor=tkinter.SW, text=(name, rank2), fill=color)
            else:
                canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i+1)+TEXT_DX, gap_height * rank2 + GRAPH_MARGIN_SIZE,
                                   anchor=tkinter.SW, text=str(name)+'*', fill=color)



# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
