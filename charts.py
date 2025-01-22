import matplotlib.pyplot as plt

def draw_pie_chart(match_percentage):
    """Draw a pie chart for match percentage."""
    fig, ax = plt.subplots()
    labels = ['Match', 'Remaining']
    sizes = [match_percentage, 100 - match_percentage]
    colors = ['#4CAF50', '#FF5733']
    explode = (0.1, 0)
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')
    return fig
