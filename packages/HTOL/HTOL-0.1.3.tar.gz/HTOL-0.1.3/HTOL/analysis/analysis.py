from scipy.stats import norm
from pathlib import Path
import xarray as xr
import pandas as pd
from HTOL.support import *
from numpy import nan, polyfit
import numpy as np
from itertools import product
import matplotlib as mpl
import matplotlib.pyplot as plt

FILTER_ARGUMENTS = ["stress_max", "purpose", "lot", "structure", "wafer", "process", "d_pos", "subdie", "orientation", "status_flag"]
OVERFLOW_OVERWRITE = nan

def generate_das_list(working_dir):
    gen = Path(working_dir).glob("*_*_*.nc")
    das = [xr.open_dataarray(file) for file in gen]
    c_d = get_contents_list(das)
    return das, c_d

def get_contents_list(das):
    # a = ["lab_setup"] + FILTER_ARGUMENTS
    # contents_dict = dict(zip(a, [set()] * len(a)))
    contents_dict = {"lab_setup": set(), "stress_max": set(), "purpose": set(), "lot": set(), "structure": set(), "wafer": set(),
         "process": set(), "d_pos": set(), "subdie": set(), "orientation": set(), "status_flag": set() }

    for da in das:
        for k in contents_dict.keys():
            if k in da.attrs.keys(): contents_dict[k].add(da.attrs[k])
            else: contents_dict[k] |= set(da[k].data)
    for k, v in contents_dict.items():
        s = list(v)
        s.sort()
        contents_dict[k] = s
    return contents_dict

def filter_ds_attrs(das, **kwargs):
    lab_setup = kwargs.get("lab_setup", None)
    ret = []
    for da in das:
        attrs = da.attrs.copy()
        attrs.pop("setup")
        if lab_setup == None: attrs.pop("lab_setup")
        elif not attrs["lab_setup"] in lab_setup: continue 
        ret.append(da)
    return ret

def filter_ds_dataarray(das, **kwargs):
    ret = []
    for da in das:
        dies_set = set(da.dies.data)
        for k, v in kwargs.items():
            if not k in FILTER_ARGUMENTS: continue
            attr = getattr(da, k)
            dies_set &= set(attr[attr.isin(v)].dies.data)

        if len(dies_set) > 0: ret.append(da.sel(dies = list(dies_set)))
    return ret
    
def filter_ds(l, **kwargs):
    ret = filter_ds_attrs(l, **kwargs)
    ret = filter_ds_dataarray(ret, **kwargs)
    return ret

def match_relevant_set(contents, cat, regex):
    ser = pd.Series(data = contents[cat])
    return list(ser[ser.str.match(regex)])

def contains_relevant_set(contents, cat, string):
    ser = pd.Series(data = contents[cat])
    return list(ser[ser.str.contains(string)])

def xs_at_hours(das, hr, **kwargs):
    subset = []
    for da in das:
        temp = (da.stress_time - hr).to_series().abs()
        if temp.min() > hr * kwargs.get("relative_deviation_allowed", 0.01): continue
        t_ind = temp[temp == temp.min()].index[0]
        if kwargs.get("relative", False): da.values = da.values / da[(da.meas_type == Subtest.STRESS.value) & (da.stress_time == 0.0)].values
        subset.append(da.sel(time = t_ind))
    return subset

def process_plot_criteria(subset, plot_criteria):
    # mpl copy config
    colors = [list(d.values())[0] for d in mpl.rcParams["axes.prop_cycle"]]
    # process data
    subset_c_d = get_contents_list(subset)
    plot_filter = dict(zip(plot_criteria, [subset_c_d.get(k) for k in plot_criteria]))
    plot_tuples = list(product(*plot_filter.values()))
    label_map = dict(zip(plot_tuples, [None] * len(plot_tuples)))
    return plot_filter, plot_tuples, label_map, colors

def plot(func):
    def inner(das, hrs = None, ax = None, **kwargs):
        # configure ax
        if ax == None:
            new_image = True
            fig, ax = plt.subplots(1, 1)
        else: 
            new_image = False

        # initial data filtering
        filtered = filter_ds(das, **kwargs.get("subset_filter", {}))
        if hrs == None: pass
        elif isinstance(hrs, (tuple, list)) and len(hrs) == 2 and not "_xs_" in func.__name__:
            for da in filtered:
                da = da[(hrs[0] <= da.stress_time) & (da.stress_time <= hrs[1])]
                if len(da.values) == 0: filtered.remove(da)
        elif "_xs_" in func.__name__:
            pass
        if len(filtered) == 0: raise AttributeError("filtering/timing is too strict - no data left")

        dec = kwargs.get("decimate", 1)
        if dec != 1 and isinstance(dec, int): filtered = [da[::dec] for da in filtered]

        inner_ret = func(filtered, hrs, ax, **kwargs)

        # return if necessary
        if new_image == True: return fig, ax, inner_ret
        else: return inner_ret
    return inner

@plot
def plot_stress_time_indexing(filtered_das, hrs, ax, plot_criteria = [], **kwargs):
    colors = [list(d.values())[0] for d in mpl.rcParams["axes.prop_cycle"]]
    relative = kwargs.get("relative", False)
    i = 0

    label_map = pd.DataFrame(columns = ["color", "line"])
    for da in filtered_das:
        # s = set(product(*[da[e].data for e in plot_criteria]))
        for r in da.dies.values:
            temp = da.sel(dies = r, time = da[da.meas_type == Subtest.STRESS.value].time.values)
            if relative: temp.values = temp.values / temp.values[0]
            crits = []
            for e in plot_criteria:
                crits.append(str(temp[e].values))
            string = "_".join(crits)        
            if string in label_map.index: ax.plot(temp.stress_time, temp.values, c = label_map.at[string, "color"])
            else:
                c = colors[i % len(colors)] 
                line = ax.plot(temp.stress_time, temp.values, c = c)[0]
                label_map.loc[string, ["color", "line"]] = [c, line]
                i += 1

    ax.legend(list(label_map.line), list(label_map.index), title = "_".join(plot_criteria), loc = "best")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Current (A)" if not relative else "Relative change (dimensionless)")
    # ax.grid()

@plot
def plot_stress_time(filtered_das, hrs, ax, plot_criteria = [], **kwargs):
    _, plot_tuples, label_map, colors = process_plot_criteria(filtered_das, plot_criteria)

    for i, t in enumerate(plot_tuples):
        filter_dict = dict(zip(plot_criteria, [[e] for e in t]))
        ret = filter_ds(filtered_das, **filter_dict)

        for da in ret:
            temp = da.swap_dims({"time": "meas_type"}).sel(meas_type = Subtest.STRESS.value)
            # temp = da.sel(time = da.meas_type[da.meas_type == Subtest.STRESS.value].time.data)
            # temp.values[temp.values == 9.9e+37] = OVERFLOW_OVERWRITE #! how to handle overflow?
            if label_map[t] == None: label_map[t] = ax.plot(temp.stress_time, temp.data, c = colors[i % len(colors)])[0]
            else: ax.plot(temp.stress_time, temp.values, c = colors[i % len(colors)])

    ax.legend(list(label_map.values()), ["_".join([str(e) for e in t]) for t in label_map.keys()], title = "_".join(plot_criteria), loc = "best")
    ax.set_ylabel("Current (A)")
    ax.set_xlabel("Stress time (h)")
    # ax.grid()

@plot
def plot_type_scatter(filtered_das, hrs, ax, plot_criteria = [], **kwargs):    
    _, plot_tuples, label_map, colors = process_plot_criteria(filtered_das, plot_criteria)
    x_ax = kwargs.get("x_ax", ("CHARDOWN", 2.0, 0))
    y_ax = kwargs.get("y_ax", ("STRESS", None, 0))
    fits = dict()

    for i, t in enumerate(plot_tuples):
        filter_dict = dict(zip(plot_criteria, [[e] for e in t]))
        ret = filter_ds(filtered_das, **filter_dict)
        x_co, y_co = [], []
        for da in ret:
            for e in da[(da.meas_type == Subtest.STRESS.value) & (da.step_change)].stress_time.data:
                if not hrs[0] <= e <= hrs[1]: 
                    # print("No suitable stress time found within limits")
                    continue

                if x_ax[1] != None: x = da[(da.stress_time == e) & (da.meas_type == Subtest[x_ax[0]].value) & (da.set_voltage == x_ax[1])]
                else: x = da[(da.stress_time == e) & (da.meas_type == Subtest[x_ax[0]].value)]
                
                if y_ax[1] != None: x = da[(da.stress_time == e) & (da.meas_type == Subtest[y_ax[0]].value) & (da.set_voltage == y_ax[1])]
                else: y = da[(da.stress_time == e) & (da.meas_type == Subtest[y_ax[0]].value)]

                if x.values.size == 0 or y.values.size == 0:
                    # print("x and/or y size is 0")
                    continue
                x_co += list(x.values[0])
                y_co += list(y.values[0])
        if len(x_co) != len(y_co): raise Exception("x and y not the same length, something went wrong")
        if len(x_co) == 0:
            print(f"No suitable coordinates found for {da.setup}")
            continue

        fits["_".join([str(e) for e in t])] = polyfit(x_co, y_co, kwargs.get("polyfit_grade", 3)) 
        if label_map[t] == None: label_map[t] = ax.scatter(x_co, y_co, c = colors[i % len(colors)])
        else: ax.scatter(x_co, y_co, c = colors[i % len(colors)])
        # ax.scatter(x_co, y_co, c = colors[i % len(colors)])

    ax.legend(list(label_map.values()), ["_".join([str(e) for e in t]) for t in label_map.keys()], title = "_".join(plot_criteria), loc = "best")
    ax.set_title(f"{y_ax[0]}{f'_{y_ax[1]:01f}V' if y_ax[1] != None else ''} ifo {x_ax[0]}{f'_{x_ax[1]:.1f}V' if x_ax[1] != None else ''}")
    ax.set_xlabel("Current (A)")
    ax.set_ylabel("Current (A)")
    # ax.grid()
    return fits

@plot
def plot_stress_xs_prob(filtered_das, hrs, ax, plot_criteria = [], **kwargs):
    if not isinstance(hrs, list): hrs = [hrs]
    for hr in hrs:
        subset = xs_at_hours(filtered_das, hr, **kwargs)
        if len(subset) == 0:
            print(f"WARNING: subset at {hr} hrs gives no data back - IGNORED")
            continue
        subset_c_d = get_contents_list(subset)

        plot_filter = dict(zip(plot_criteria, [subset_c_d.get(k) for k in plot_criteria]))
        for t in list(product(*plot_filter.values())):
            
            # filter
            filter_dict = dict(zip(plot_criteria, [[e] for e in t]))
            ret = filter_ds(subset, **filter_dict)
            
            # plot
            xs = []
            for da in ret: xs += list(da.data[~np.isnan(da.data)])
            xs.sort()
            # plot
            ax.scatter(*benard_estimator(xs), label = "_".join(t) + (f"_{hr}hrs" if len(hrs) > 1 else ""))
    # configure plot
    ax.set_yscale("function", functions = (lambda x: norm.ppf(x/100), lambda x: norm.cdf(x) * 100))
    ax.set_yticks([10, 30, 50, 70, 90])
    ax.set_xlabel("Current (A)" if not kwargs.get("relative", False) else "Relative change (dimensionless)")
    ax.set_ylabel("Probability (%)")
    ax.legend(title = "_".join(plot_criteria), loc = "lower right")
    # ax.grid()

@plot
def plot_char_stress_time(filtered_das, hrs, ax, plot_criteria = [], **kwargs):
    _, plot_tuples, label_map, colors = process_plot_criteria(filtered_das, plot_criteria)
    y_ax = kwargs.get("y_ax", ("CHARDOWN", 2.0, 0))
    relative = kwargs.get("relative", False)

    for i, t in enumerate(plot_tuples):
        filter_dict = dict(zip(plot_criteria, [[e] for e in t]))
        ret = filter_ds(filtered_das, **filter_dict)
        for da in ret:
            try:
                first = da[(da.meas_type == Subtest.CHARUP.value) & (da.stress_time == 0.0) & (da.set_voltage == y_ax[1])][y_ax[2]]
            except IndexError: 
                print("No 0 time reference found, sample(s) skipped")
                continue
            stress_times = np.unique(da[da.step_change].stress_time.data)

            rest = list()
            for st in stress_times:
                if st == 0: continue
                temp = da[(da.meas_type == Subtest[y_ax[0]].value) & (da.stress_time == st) & (da.set_voltage == y_ax[1])]
                if temp.values.size == 0: continue
                rest.append(temp[y_ax[2]])
            res = xr.concat([first] + rest, dim = "time")
            if relative: res.values = res.values / first.values
            if label_map[t] == None: label_map[t] = ax.plot(res.stress_time, res.data, c = colors[i % len(colors)])[0]
            else: ax.plot(res.stress_time, res.data, c = colors[i % len(colors)])

    ax.legend(list(label_map.values()), ["_".join([str(e) for e in t]) for t in label_map.keys()], title = "_".join(plot_criteria), loc = "best")
    ax.set_ylabel("Current (A)" if not relative else "Relative change (dimensionless)")
    ax.set_xlabel("Stress time (h)")
    # ax.grid()