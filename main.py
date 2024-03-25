from qiskit import *
# from qiskit.providers.ibmq import least_busy
# from qiskit.tools.jupyter import *
# from qiskit.visualization import *

# from qiskit_ibm_runtime.fake_provider import FakeVigo
from qiskit import transpile
# from qiskit import IBMQ, transpile
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
# from qiskit.tools.visualization import plot_histogram

"""
Converts input integer from decimal into a binary string.
"""
def num_to_bin(num : int):
    end = ""
    if (num == 0):
        return end
    if num >= 1:
        end = num_to_bin(num // 2)
    return end + str(num % 2)

"""
Converts input string from binary into a decimal integer.
Raises an exception if an unexpected character is contained in the string.
"""
def str_to_dec(s:str):
    out = 0
    power = 0
    chars = reversed(list(s))
    for i in chars:
        if i == "1":
            out = out + pow(2, power)
        elif i != "0":
            raise Exception("Input string must be 1 or 0")
        power = power + 1
    return out

"""
If the input integer is odd, the integer will be converted into the
nearest even integer using a version of the BV algorithm.
If the integer is 1, it will be rounded up to 2.
Raises an error if the input number is less than the desired range of [1, n).
"""
def convert_to_even(input_num : int):
    if input_num < 1:
        raise Exception("Numbers must be in range [1, n)")
    n = num_to_bin(input_num)
    # catch edge case
    if len(n) == 1 and n[0] == "1":
        n = n + "0"

    circuit = QuantumCircuit(len(n)+1,len(n))

    circuit.h(range(len(n)))
    circuit.x(len(n))
    circuit.h(len(n))

    circuit.barrier()
    first = True

    for digit, query in enumerate(reversed(n)):
        if query == "1" and not first:
            circuit.cx(digit, len(n))
    
        first = False
    circuit.barrier()

    circuit.h(range(len(n)))
    circuit.barrier()
    circuit.measure(range(len(n)),range(len(n)))

    simulator = AerSimulator()
    result = simulator.run(transpile(circuit, simulator)).result()
    data = list(dict(result.get_counts()).keys())[0]
    
    return str_to_dec(data)

"""
Converts each integer in a list
Raises an error if an non-integer value is put in.
"""
def convert_list_to_even(input_list):
    for i in range(len(input_list)):
        if type(input_list[i]) != type(1):
            raise Exception("Input must be a list of integers.")
        input_list[i] = convert_to_even(input_list[i])

"""
To run, enter "python main.py" into the terminal.
"""
def main():
    # get input from user
    num_list = input("Please enter the list of numbers you wish to convert, separated by spaces: ")
    
    # parse inputs
    num_list = [int(i) for i in num_list.split(" ")]

    print(f"Converting {num_list}")
    
    # convert output
    convert_list_to_even(num_list)
    print(f"Even list: {num_list}")

if __name__=="__main__":
    main()