import csv
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

arr = np.random.rand(100,1)
def quick_sort(arr):
    if(len(arr) < 2):
        return arr
    
    else:
        pivot = arr[0]  #the pivot is the element taken as a reference to partition the array into two seperate arrays
        less = [i for i in arr[1:len(arr)] if i <= pivot]
        greater = [i for i in arr[1:len(arr)] if i>pivot]
        """both of the sibstrings are created with the criteria of being lesser and greater than the pivot element and are seperately
        sorted using the recursion function. The elements from index 1 to end is analysed and split"""
        return quick_sort(less) + [pivot] + quick_sort(greater)


def algorithm_a(arr):
        # Implement Bubble Sort to sort the input array
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def algorithm_b(arr):
    quick_sort(arr)
    

def findMean(values):
    return np.mean(values)

def returnX(correlation, Yvalue, x, y):
    xValue = correlation * (Yvalue - y) + x
    return xValue

def measure_and_store_runtimes(filename_a, filename_b, num_samples):
    runtimes_a = []
    runtimes_b = []

    for _ in range(num_samples):
        start_time = time.time()
        algorithm_a(arr)
        end_time = time.time()
        runtimes_a.append((end_time - start_time)+random.random()) #digital noise

        start_time = time.time()
        algorithm_b(arr)
        end_time = time.time()
        runtimes_b.append((end_time - start_time)+random.random())

    with open(filename_a, 'w', newline='') as file_a:
        writer = csv.writer(file_a)
        writer.writerow(runtimes_a)

    with open(filename_b, 'w', newline='') as file_b:
        writer = csv.writer(file_b)
        writer.writerow(runtimes_b)

    return runtimes_a, runtimes_b

num_samples = 100

file_a = 'algorithm_a_runtimes.csv'
file_b = 'algorithm_b_runtimes.csv'

runtimes_a, runtimes_b = measure_and_store_runtimes(file_a, file_b, num_samples)

correlation = np.corrcoef(runtimes_a, runtimes_b)[0, 1]
correlation = 0 if np.isnan(correlation) else correlation  # Handle division by zero

# Check if both datasets have data before calculating the correlation
if len(runtimes_a) > 0 and len(runtimes_b) > 0:
    print("Correlation between runtimes:", correlation)
else:
    print("Correlation cannot be calculated as one or both datasets are empty.")

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)

initial_value = correlation

axcolor = 'lightgoldenrodyellow'
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
slider = Slider(ax_slider, 'correlation', -1.0, 1.0, valinit=initial_value)


#plt.scatter(runtimes_a, runtimes_b, c='blue', alpha=0.6, label=f'Correlation: {correlation:.2f}')
plt.xlabel('Algorithm A Runtimes')
plt.ylabel('Algorithm B Runtimes')
plt.title('Scatter Plot of Runtimes')

def update(val):
    correlation = slider.val
    x_mean = findMean(runtimes_a)
    y_mean = findMean(runtimes_b)

    # Clear the plot
    ax.clear()

    # Calculate the new points based on correlation
    x_on_y = [returnX(correlation, value_y, x_mean, y_mean) for value_y in runtimes_b]
    y_on_x = [returnX(correlation, value_x, y_mean, x_mean) for value_x in runtimes_a]

    # Add the new points to the plot
    ax.scatter(runtimes_a, runtimes_b, c='red', alpha=0.6, label=f'Correlation: {correlation:.2f}')
    ax.plot(x_on_y, runtimes_b, color='green', linestyle="dashed", label='X on Y')
    ax.plot(runtimes_a, y_on_x, color="blue", linestyle="dashed", label='Y on X')

    ax.set_xlabel('Algorithm A Runtimes')
    ax.set_ylabel('Algorithm B Runtimes')
    ax.set_title('Scatter Plot of Runtimes')
    ax.legend()

    fig.canvas.draw_idle()


slider.on_changed(update)

plt.legend()
plt.show()
