import matplotlib.pyplot as plt

# Initialize empty lists to store data
x_values = []
y_values = []

# Specify the path to your file
file_path = 'plot.txt'

# Read the data from the file
with open(file_path, 'r') as file:
    for line in file:
            # Append the value to the lists
            y_values.append(line)
            
# Create x-values (assuming 1-based index for each entry)
x_values = list(range(1, len(y_values) + 1))

# Create the plot
plt.plot(x_values, y_values, linestyle='-')

# Add labels and a title
plt.xlabel('Entry')
plt.ylabel('Output Values')
plt.title('Output Values vs. Entry')

# Show the plot
plt.show()
