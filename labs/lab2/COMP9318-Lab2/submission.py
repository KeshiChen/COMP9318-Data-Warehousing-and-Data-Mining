## import modules here 
import pandas as pd
import numpy as np


################# Question 1 #################
def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)
# helper functions
def project_data(df, d):
    # Return only the d-th column of INPUT
    return df.iloc[:, d]

def select_data(df, d, val):
    # SELECT * FROM INPUT WHERE input.d = val
    col_name = df.columns[d]
    return df[df[col_name] == val]

def remove_first_dim(df):
    # Remove the first dim of the input
    return df.iloc[:, 1:]

def slice_data_dim0(df, v):
    # syntactic sugar to get R_{ALL} in a less verbose way
    df_temp = select_data(df, 0, v)
    return remove_first_dim(df_temp)
def copy(src_list):
    return [i for i in src_list]
def cart_product(row, cols):
    dims = row[:-1][1-cols:]
    dim = len(dims)
    result = []
    for i in range(2 ** dim):
        new_row = list(row)
        for j in range(dim):
            gap = 2 ** j
            if i % (2 * gap) > gap -1: 
                new_row[len(new_row) - 2 -j] = 'ALL'
        result.append(new_row)
    return result

def buc_rec_0(input, result, prev = []):
    # Note that input is a DataFrame
    #dump_input2(input)
    dims = input.shape[1]
    rows = input.shape[0]
    new_prev = copy(prev)
    if rows ==1 and dims > 1:
        #print("haha")
        new_prev += input.iloc[0,].tolist()
        #for i in range(len(rows)-1):
        #    rows[i] = [str(rows[i]), '*']
        new_rows = cart_product(tuple(new_prev), dims)
        result += new_rows
        #print("sssss",result)
        return result
    if dims == 1:
        # only the measure dim
        input_sum = sum( project_data(input, 0) )
        new_prev.append(input_sum)
        result.append(new_prev)
        return result
        #for i in prev:
        #    print('%-5s'%str(i), end='')
        #output(input_sum)
    else:
        # the general case
        dim0_vals = set(project_data(input, 0).values)
        for dim0_v in dim0_vals:
            new_prev.append(dim0_v)
            sub_data = slice_data_dim0(input, dim0_v)
            result = buc_rec_0(sub_data, result, new_prev)
            new_prev = copy(prev)
        ## for R_{ALL}
        sub_data = remove_first_dim(input)
        new_prev.append('ALL')
        result = buc_rec_0(sub_data, result, new_prev)
        #print("aaa",result)
    return result
def buc_rec_optimized(df):# do not change the heading of the function
    result = []
    result = buc_rec_0(df,result)
    result = pd.DataFrame(result, columns = df.columns.values)
    return result    
input_data = read_data('./asset/a_.txt')
output = buc_rec_optimized(input_data)
print(output)
################# Question 2 #################
def partition(List):
    for i in range(1, len(List)):
        for j in partition(List[i:]):
            yield [List[:i]] + j
    yield [List]
    
def sse(arr):
    if len(arr) == 0:
        return 0.0
    avg = np.average(arr)
    val = sum( [(x-avg)*(x-avg) for x in arr] )
    return val

def bin_cost(partition,costs):
    cost_sum = 0
    for part in partition:
        if part not in costs:
            costs[part] = sse(part)
        cost_sum += costs[part]
    #print(cost_sum, costs)
    return cost_sum, costs
        
def v_opt_dp(x, num_bins):# do not change the heading of the function
    x = tuple(x)
    sfxLen = len(x)
    M_Result = [-1 for x in range(sfxLen)]
    M_Cost = [[-1 for x in range(sfxLen)] for y in range(num_bins)]
    costs = {}
    for bins in range(1, num_bins+1):
        for i in reversed(range(sfxLen)):
            suffix = x[i:]
            prefix = x[:i]
            if len(prefix) + bins >= num_bins:
                if bins > len(suffix) :
                    continue
                elif bins == 1:
                    min_cost = sse(suffix)
                    costs[suffix] = min_cost
                    opt = suffix
                else:
                    partitions = [part for part in partition(suffix) if len(part) == bins]
                    #print("partitions",partitions)
                    par_costs = []
                    for part in partitions:
                        cost, costs = bin_cost(part, costs)
                        par_costs.append(cost)
                    #if len(par_costs) != 0:
                    min_cost = min(par_costs)
                    opt = partitions[par_costs.index(min_cost)]
                M_Cost[bins - 1][i] = min_cost
                #opt = list(opt)
                #print(opt)
                M_Result[i] = opt
    for i in range(len(M_Result[0])):
        M_Result[0][i] = list(M_Result[0][i])
    return M_Cost, M_Result[0]