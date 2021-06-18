from Graph import *
import time
import numpy as np
import pandas as pd
from math import sqrt
import random
import matplotlib


def main():
    functions = ['0b111',
                '0b101',
                ]
    code = '111011111000'
    encoded = encode(code, functions)
    graph = Graph(steps=len(code) + 1, functions=functions)
    decoded = graph.decode(encoded, show=2)

    print('Encoded: {}'.format(encoded))
    print('Decoded: {}'.format(decoded))
    graph.show()

    '''create an csv file for an analise of ability to decode codes with an errors'''
    # create_statistics()

    '''show result of created statistics'''
    read_csv('end_code64.csv')


def create_statistics():
    functions = ['0b010011',
                '0b011101',
                ]
    '''
    '0b11001',
    '0b10111',
    0110011111110111110010001100
    '''

    code_len = 64
    code = rand_code_str(code_len)
    graph = Graph(steps=len(code) + 1, functions=functions)
    encoded = encode(code, functions)
    whole_list = []
    signal = bits_to_signal(encoded)
    E_Ns = np.arange(0., 12., 0.5)
    sigmas = np.array([sqrt(1 / 10 ** (E_N / 10)) for E_N in E_Ns])
    print(sigmas)
    print(len(sigmas))
    start = time.time()
    counter = 0
    for sigma, E_N in zip(sigmas, E_Ns):
        for i in range(100):
            lstart = time.time()
            signal_with_errors = add_noise_to_signal(signal, sigma=sigma)
            decoded_signal = signal_to_bits(signal_with_errors)
            result = graph.decode(decoded_signal)
            result_errors = str_compare(code, result)
            item = [
                sigma,
                E_N,
                str_compare(encoded, decoded_signal),
                result_errors,
                result_errors / code_len
            ]
            whole_list.append(item)
            lend = time.time()
            if not i % 100:
                print(counter, lend - lstart)
            counter += 1
    end = time.time()
    print('Overall time: ', end - start)
    np_array = np.array(whole_list)
    df = pd.DataFrame({'Sigma': np_array[:, 0],
                       'E_N': np_array[:, 1],
                       'Encoded errors': np_array[:, 2],
                       'Solved errors': np_array[:, 3],
                       'BER': np_array[:, 4]
                       })
    print(df)

    result = input('Save or not? Y/N')
    if result == 'Y' or result == 'y':
        name = 'end_code' + str(code_len) + '.csv'
        df.to_csv(name, index=False)
        print('Saved ' + name)
    else:
        print("Didn't save")


def read_csv(file_name):
    df = pd.read_csv(file_name)
    result = {
        'E_b/N_0': [],
        'BlockER': [],
        'BitER': [],
    }
    for index in df['E_N'].unique():
        slice = df[df['E_N'] == index]
        result['E_b/N_0'].append(
            index
        )
        result['BlockER'].append(
            1 - slice[slice['Solved errors'] == 0].count()[0] / slice.count()[0]
        )
        result['BitER'].append(
            slice['BER'].sum() / (64 * 3000)
        )
    # print(result['E_b/N_0'])
    # print(result['BlockER'])
    # print(result['BitER'])
    fig, ax = plt.subplots()
    ax.plot(result['E_b/N_0'], result['BlockER'], '.', label='BlockER')
    ax.plot(result['E_b/N_0'], result['BitER'], '.', label='BitER')
    ax.set_ylabel('p')
    ax.set_xlabel('E_b/N_0')
    plt.legend(loc='upper right')
    plt.yscale('log')
    plt.grid(True)
    plt.show()


def bits_to_signal(bits):
    bits_list = list(bits)
    signal_array = [1. if i == '1' else -1. for i in bits_list]
    return np.array(signal_array)


def signal_to_bits(signal):
    res = (signal >= 0).astype(int)
    return ''.join(str(i) for i in res)


def add_noise_to_signal(signal, sigma):
    errors = np.random.normal(0, sigma, signal.shape[0])
    return signal + errors


def rand_code_str(length):
    return '{:0{}b}'.format(
        random.getrandbits(length),
        length,
    )


def create_error(code, sigma=0.1, error_threshold=0.15):
    code_list = list(code)
    code_len = len(code_list)
    errors = np.random.normal(0, sigma, code_len)
    for code_item, item, error in zip(code_list, range(code_len), errors):
        if error >= error_threshold or error <= -error_threshold:
            if code_item == '0':
                code_list[item] = '1'
            if code_item == '1':
                code_list[item] = '0'
    return ''.join(code_list)


def str_compare(str1, str2):
    if len(str1) != len(str2):
        return None
    splitted_str1 = list(str1)
    splitted_str2 = list(str2)
    result = 0
    for word_str1, word_str2 in zip(splitted_str1, splitted_str2):
        if word_str1 != word_str2:
            result += 1
    return result

if __name__ == '__main__':
    main()
