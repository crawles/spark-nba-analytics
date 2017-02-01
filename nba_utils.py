from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style("white")

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    '''Draws NBA court on axis. 
    Source: http://savvastjortjoglou.com/nba-shot-sharts.html'''
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def plot_shot_chart(x,y,kind = 'hex', gridsize = 15, norm = None, label = '', title = ''):
    ''' Add source '''
    cmap=plt.cm.gist_heat_r
    joint_shot_chart = sns.jointplot(x, y, stat_func=None,
                                     kind=kind, space=0, color=cmap(.2), 
                                     cmap=cmap, size = 20, joint_kws=dict(gridsize=gridsize,
                                                                          norm = norm))
    joint_shot_chart.fig.set_size_inches(9,8.25)
    

    if kind == 'hex':# color bar
        cax = joint_shot_chart.fig.add_axes([.77, .04, .03, .2]) # size and placement of bar
        plt.colorbar(cax=cax)
    
    # A joint plot has 3 Axes, the first one called ax_joint 
    # is the one we want to draw our court onto 
    ax = joint_shot_chart.ax_joint
    draw_court(ax)

    # Adjust the axis limits and orientation of the plot in order
    # to plot half court, with the hoop by the top of the plot
    ax.set_xlim(-250,250)
    ax.set_ylim(422.5, -47.5)

    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')

    # Add Data Source
    ax.text(-250,442,'Data source: stats.nba.com via NBAsavant\nPlotting code source: Savvas Tjortjoglou', fontsize=9)
    
    # label
    ax.text(-200,405,label, fontsize=20)
    return joint_shot_chart

sns_colors = sns.color_palette('deep',8)
def draw_3pt_piechart(per_3, per_midrange):
    '''Draws a pie chart showing percentage of 3's on shotchart'''
    plt.axes([.05, .1, .2, .2], axisbg='y')
    patches,_ = plt.pie(x = [per_3,per_midrange],
                    startangle = 180,
                    counterclock = False)
    labels = ['3 pointer','midrange']
    #     colors = ['red', 'orange']
    colors = [sns_colors[1], sns_colors[4]]
    patches,_ = plt.pie(x = [per_3,per_midrange],
                    startangle = 180,
                    colors = colors,
    #                         labels = labels,
    #                         labeldistance = .4,
                    counterclock = False)
    plt.legend(patches, labels, loc=3 ,shadow=True, fontsize='large', frameon = True) 
    plt.title('Percentage of shots', y = -0.08)
