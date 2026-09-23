# main.py
from invoke_info import InvokeInfo  # Import the InvokeInfo class

def main():
    # Read input
    input_str = input().strip()
    input_str = input_str.replace('[', '').replace(']', '').replace(' ', '')
    input_data = input_str.split(',')
    
    invokes = []
    for i in range(0, len(input_data), 2):
        time = int(input_data[i])
        interface_id = int(input_data[i + 1])
        invokes.append(InvokeInfo(interface_id, time))
    
    # Read time segment and minimum limits
    time_segment = int(input())
    min_limits = int(input())
    
    # Call the solution and print the result
    result = get_interfaces(invokes, time_segment, min_limits)
    print(result)

if __name__ == "__main__":
    main()
