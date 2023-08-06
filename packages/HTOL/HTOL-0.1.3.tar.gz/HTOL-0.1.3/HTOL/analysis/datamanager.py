from HTOL.analysis.analysis import *
from cycler import cycler
from scipy.stats import norm
from pathlib import Path
import xarray as xr
import pandas as pd
from HTOL.support import *
from numpy import nan, polyfit, isnan
import numpy as np
from itertools import product
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Union
from importlib.resources import files

def update_criteria_string(da, plot_criteria, group_dict):
    ## GROUP DICT
    for p_c, p_d in group_dict.items():
        for new, olds in p_d.items():
            da[p_c].values = np.array([new if old in olds else old for old in da[p_c].values])

    ## CRIT_STRINGS
    crit_strings = ["_".join(x) for x in list(zip(*[da[p].values for p in plot_criteria]))] if len(plot_criteria) > 0 else [""] * len(da.dies.values)
    return da.assign_coords(crit_string = ("dies", crit_strings))

class HtolDataManager():
    NETCDF_FILE_GLOB = "*_*_*.nc"
    ATTRS_PARAMS = ["lab_setup", "setup"]
    DIMS_PARAMS = ["stress_max", "purpose", "lot", "structure", "wafer", "process", "d_pos", "subdie",  "orientation", "status_flag"]
    CONTENT_PARAMS = ATTRS_PARAMS + DIMS_PARAMS
    # FILTER_ARGUMENTS = ["stress_max", "purpose", "lot", "structure", "wafer", "process", "d_pos", "subdie", "orientation", "status_flag"]
    # OVERFLOW_OVERWRITE = nan

    def __init__(self, path : Union[Path, str], prop_cycler = None, *args, **kwargs):
        if isinstance(path, str): self.folder = Path(path).resolve()
        else: self.folder = path.resolve()

        mpl.style.use(kwargs.get("mpl_style", Path(files("HTOL.analysis")).resolve() / "htol_style.mplstyle"))
        self.data_array_list = self._generate_data_array_list()
        self.contents_dict = self._get_content_list()
        self.cycler = mpl.rcParams["axes.prop_cycle"] if prop_cycler == None else prop_cycler
        self.double_cycler = cycler('marker', ['+', '.', 'x', 'o', 's']) * self.cycler
        self.cycler_list = [cyc for cyc in self.cycler]

    def plot(func):
        def inner(self, *args, **kwargs):
            # configure ax
            fig_ax = kwargs.get("fig_ax", None)
            if fig_ax == None: fig, ax = plt.subplots(1, 1)
            else: fig, ax = fig_ax

            # initial data filtering
            subset_filter = kwargs.get("subset_filter", {})
            filtered = self.filter_data_array_list(self.data_array_list, **subset_filter)
            if len(filtered) == 0: raise AttributeError("filtering/timing is too strict - no data left")
            dec = int(kwargs.get("decimate", 1))
            if dec != 1: filtered = [da[::dec] for da in filtered]

            # generate plot criteria
            plot_criteria = kwargs.get("plot_criteria", [])
            group_dict = kwargs.get("group_dict", {})
            group_dict = {k: v for k, v in group_dict.items() if k in self.DIMS_PARAMS} # only take valid plot_criteria keys
            filtered = list(map(lambda da: update_criteria_string(da, plot_criteria, group_dict), filtered))

            # hours filter
            hours_min = kwargs.get("hours_min", None)
            hours_max = kwargs.get("hours_max", None)
            if hours_min != None: filtered = list(map(lambda elem: elem[elem.stress_time >= hours_min], filtered))
            if hours_max != None: filtered = list(map(lambda elem: elem[elem.stress_time <= hours_max], filtered))
            for elem in filtered: 
                if len(elem.values) == 0: filtered.remove(elem)

            kwargs["filtered"] = filtered
            kwargs["ax"] = ax
            func_return = func(self, *args, **kwargs)

            # return if necessary
            return fig, ax, func_return
        return inner

    @plot
    def plot_qq(self, sample_hours = 100, **kwargs):
        # process kwargs
        data_array_list = kwargs["filtered"]
        ax = kwargs["ax"]
        plot_criteria = kwargs.get("plot_criteria", [])
        relative = kwargs.get("relative", False)
        grid = kwargs.get("show_grid", True)

        # set cycler
        ax.set_prop_cycle(self.double_cycler)

        if not isinstance(sample_hours, list): sample_hours = [sample_hours]
        sample_hours = list(map(lambda x: int(x), sample_hours))
        right_max = 10 if relative else 2e-4
        for hr in sample_hours:
            subset = self._get_currents_at_hour(hr, data_array_list, **kwargs)
            if len(subset) == 0:
                print(f"WARNING: subset at {hr} hrs gives no data back - IGNORED")
                continue
            
            summary = dict()
            # GATHER DATA
            for da in subset:
                for r in da.dies.values:
                    t = da.sel(dies = r)
                    if np.isnan(float(t.values)): continue
                    if str(t.crit_string.values) in summary.keys(): summary[str(t.crit_string.values)].append(float(t.values))
                    else: summary[str(t.crit_string.values)] = [float(t.values)]
            # PLOT DATA
            for k, v in summary.items():
                v.sort()
                right_max = max(v) * 1.1 if max(v) >= right_max * 0.99 else right_max
                # ax.scatter(*benard_estimator(v), label = f"{k}_{hr}hrs")
                ax.plot(*benard_estimator(v), ls = "", label = f"{k}_{hr}hrs" if k != "" else f"{hr}hrs")

        ax.set_yscale("function", functions = (lambda x: norm.ppf(x/100), lambda x: norm.cdf(x) * 100))
        ax.set_yticks([10, 30, 50, 70, 90])
        ax.set_xlabel("Current (A)" if not kwargs.get("relative", False) else "Relative change (dimensionless)")
        ax.set_title("QQ plot")
        ax.set_xlim(left = 0, right = right_max)
        ax.set_ylabel("Probability (%)")
        if len(ax.lines) > 1: ax.legend(loc = "lower right")
        ax.grid(grid)

    @plot
    def plot_it(self, meas_type = ["STRESS"], **kwargs):
        data_array_list = kwargs["filtered"]
        ax = kwargs["ax"]
        plot_criteria = kwargs.get("plot_criteria", [])
        ## define local vars
        relative = kwargs.get("relative", False)
        ref_m_t = kwargs.get("reference_measurement_type", "CHARUP")
        grid = kwargs.get("show_grid", True)

        ## determine graph subtype
        if meas_type[0] == "STRESS":
            full_i_t = True
        elif meas_type[0] in ["CHARDOWN", "CHARUP"]:
            full_i_t = False
            m_t = Subtest[meas_type[0]].value # meas_type enum
            s_v = float(meas_type[1]) if len(meas_type) > 1 else 1.0 # set_voltage
            m_t_i = int(meas_type[2]) if len(meas_type) > 2 else 0 # measurement_type_index
        else:
            raise AttributeError("meas_type unclear for processing")
        # initiliaze cycler tracking
        i = 0
        label_map = pd.DataFrame(columns = ["cyc", "line"])

        # iterate through filtered data array
        for data_array in data_array_list:
            # analyze/plot line per line
            if full_i_t:
                temp = data_array.sel(time = data_array[data_array.meas_type == Subtest.STRESS.value].time.values)
                if relative: temp.values = temp.values / temp.values[0]
            else: 
                ### REFERENCE ANALYSIS
                try:
                    first = data_array[(data_array.meas_type == Subtest[ref_m_t].value) & (data_array.stress_time == 0.0) & (data_array.set_voltage == s_v)][m_t_i]
                except IndexError: 
                    print("No reference found at stress_time == 0.0 -> sample(s) skipped")
                    continue

                ### ADDITIONAL ANALYSIS
                stress_times = np.unique(data_array[data_array.step_change].stress_time.data)
                rest = list()
                for st in stress_times:
                    if st == 0: continue # seperate reference is determined and start
                    temp = data_array[(data_array.meas_type == m_t) & (data_array.stress_time == st) & (data_array.set_voltage == s_v)]
                    if temp.values.size == 0: continue
                    rest.append(temp[m_t_i])

                ### CONCAT AND POST-PROCESS
                temp = xr.concat([first] + rest, dim = "time")
                if relative: temp.values = temp.values / first.values

            # plot for right criteria
            for r in temp.dies.values:
                res = temp.sel(dies = r)
                crit_string = str(res.crit_string.values)
                if crit_string in label_map.index: ax.plot(res.stress_time, res.values, **label_map.at[crit_string, "cyc"])
                else:
                    cyc = self.cycler_list[i % len(self.cycler_list)]
                    line = ax.plot(res.stress_time, res.values, **cyc)[0]
                    label_map.loc[crit_string, ["cyc", "line"]] = [cyc, line]
                    i += 1

        ## LAYOUT PLOT
        label_map.sort_index(inplace = True)
        if len(label_map) > 1: ax.legend(list(label_map.line), list(label_map.index), title = "_".join(plot_criteria))
        ax.set_xlabel("Stress time (h)")
        ax.set_ylabel("Current (A)" if not relative else "Relative change (dimensionless)")
        ax.set_xlim(left = 0)
        ax.set_ylim(bottom = 0)
        cat = meas_type[0] if len(meas_type) == 1 else f"{meas_type[0]}_{meas_type[1]}V"
        ax.set_title(f"Dark current in function of stress time ({cat})")
        ax.grid(grid)

    @plot
    def plot_ii(self, x_ax = ("CHARDOWN", 1.0, 0), y_ax = ("STRESS", 2.0, 0), **kwargs):
        # process kwargs
        data_array_list = kwargs["filtered"]
        ax = kwargs["ax"]
        grid = kwargs.get("show_grid", True)

        x_list = self._process_ii_ax_list(x_ax)
        y_list = self._process_ii_ax_list(y_ax)
        ax.set_prop_cycle(self.double_cycler)

        summary = dict()
        for da in data_array_list:
            stress_times = list(da[(da.meas_type == Subtest.STRESS.value) & (da.step_change)].stress_time.data)
            if len(stress_times) == 0: continue
            
            for st in stress_times:
                x = da[(da.stress_time == st) & (da.meas_type == x_list[0]) & (da.set_voltage == x_list[1])]
                y = da[(da.stress_time == st) & (da.meas_type == y_list[0]) & (da.set_voltage == y_list[1])]

                if x.values.shape[0] == 0 or y.values.shape[0] == 0 or x.values.shape[1] != y.values.shape[1]:
                    print("x and y dimensions don't match, ambigious")
                    continue
                for r in da.dies.values:
                    x_temp = x.sel(dies = r)[x_list[2]]
                    y_temp = y.sel(dies = r)[y_list[2]]
                    string = str(x_temp.crit_string.values)
                    if string != str(y_temp.crit_string.values):
                        print("crit_string does not match?")
                        continue
                    if not string in summary.keys(): summary[string] = {"x": [], "y": []}
                    summary[string]["x"].append(float(x_temp.values))
                    summary[string]["y"].append(float(y_temp.values))
        
        fits = dict()
        try:
            for k, v in summary.items():
                ax.plot(v["x"], v["y"], ls = "", label = k)
                fits[k] = polyfit(v["x"], v["y"], kwargs.get("polyfit_grade", 3))
        except np.linalg.LinAlgError:
            print("Could not make the polyfit")
        ax.set_xlabel(f"Idark ({x_list[0]} @ {x_list[1]}V) (A)")
        ax.set_ylabel(f"Idark ({y_list[0]} @ {y_list[1]}V) (A)")
        ax.set_xlim(left = 0)
        ax.set_ylim(bottom = 0)
        if len(summary) > 1: ax.legend(loc = "best")
        ax.grid(grid)
        return fits

    @plot
    def plot_iv(self, meas = ("CHARDOWN", 0), **kwargs):
        # process kwargs
        data_array_list = kwargs["filtered"]
        ax = kwargs["ax"]
        grid = kwargs.get("show_grid", True)
        plot_criteria = kwargs.get("plot_criteria", [])

        summary = dict()
        for da in data_array_list:
            stress_times = list(da[(da.meas_type == Subtest.STRESS.value) & (da.step_change)].stress_time.data)
            if len(stress_times) == 0: continue

            for st in stress_times:
                temp = da[(da.stress_time == st) & (da.meas_type == Subtest[meas[0]].value)]
                if temp.values.shape[0] == 0: continue
                
                for r in temp.dies.values:
                    sub = temp.sel(dies = r)
                    d = {"x": [], "y": []}
                    for v in np.unique(sub.set_voltage.values):
                        d["x"].append(v)
                        d["y"].append(float(sub[sub.set_voltage == v][int(meas[1])]))
                    string = str(sub.crit_string.values)
                    if not string in summary.keys(): summary[string] = []
                    summary[string].append(d)

        label_map = pd.DataFrame(columns = ["cyc", "line"])
        i = 0
        for k, v in summary.items():
            l1 = v.pop(0)
            cyc = self.cycler_list[i % len(self.cycler_list)]
            line = ax.plot(l1["x"], l1["y"], **cyc)[0]
            label_map.loc[k, ["cyc", "line"]] = [cyc, line]
            i += 1
            for line in v:
                ax.plot(line["x"], line["y"], **label_map.at[k, "cyc"])

        label_map.sort_index(inplace = True)
        if len(label_map) > 1: ax.legend(list(label_map.line), list(label_map.index), title = "_".join(plot_criteria))
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (A)")
        ax.set_xlim(left = 0)
        ax.set_ylim(bottom = 0)
        ax.grid(grid)          

    def filter_data_array_list(self, data_array_list, **kwargs):
        ret = self._filter_attrs(data_array_list, **kwargs)
        ret = self._filter_die_dims(ret, **kwargs)
        return ret

    def _process_ii_ax_list(self, ax_list):
        if ax_list[0] in ["CHARDOWN", "CHARUP", "STRESS"]:
            m_t = Subtest[ax_list[0]].value # ax_list enum
            s_v = float(ax_list[1]) if len(ax_list) > 1 else 1.0 # set_voltage
            m_t_i = int(ax_list[2]) if len(ax_list) > 2 else 0 # measurement_type_index
        else:
            raise AttributeError("meas_type unclear for processing")
        return [m_t, s_v, m_t_i]

    def _filter_die_dims(self, data_array_list, **kwargs):
        ret = []
        filter_dict = {k: kwargs[k] for k in kwargs if k in self.DIMS_PARAMS}
        for da in data_array_list:
            dies_set = set(da.dies.data)
            for k, v in filter_dict.items():
                attr = getattr(da, k)
                dies_set &= set(attr[attr.isin(v)].dies.data)

            if len(dies_set) > 0: ret.append(da.sel(dies = list(dies_set)))
        return ret

    def _filter_attrs(self, data_array_list, **kwargs):
        lab_setup = kwargs.get("lab_setup", None)
        setup = kwargs.get("setup", None)
        ret = []
        for da in data_array_list:
            attrs = da.attrs.copy()
            if setup == None: attrs.pop("setup")
            elif not attrs["setup"] in setup: continue 
            if lab_setup == None: attrs.pop("lab_setup")
            elif not attrs["lab_setup"] in lab_setup: continue 
            ret.append(da)
        return ret

    def _generate_data_array_list(self):
        gen = Path(self.folder).glob(self.NETCDF_FILE_GLOB)
        das = [xr.open_dataarray(file) for file in gen]
        return das

    def _get_content_list(self):
        contents_dict = dict()
        for k in self.CONTENT_PARAMS:
            s = set()
            for da in self.data_array_list: 
                if k in self.ATTRS_PARAMS:
                    s.add(da.attrs[k])
                elif k in self.DIMS_PARAMS:
                    s |= set(da[k].values)
            contents_dict[k] = s
        return contents_dict

    def _match_relevant_set(self, cat, regex):
        ser = pd.Series(data = self.contents_dict[cat])
        return list(ser[ser.str.match(regex)])

    def _contains_relevant_set(self, cat, string):
        ser = pd.Series(data = self.contents_dict[cat])
        return list(ser[ser.str.contains(string)])

    def _get_currents_at_hour(self, hr, data_array_list, **kwargs):
        subset = []
        for da in data_array_list:
            temp = (da.stress_time - hr).to_series().abs()
            if temp.min() > hr * kwargs.get("relative_deviation_allowed", 0.01): continue
            t_ind = temp[temp == temp.min()].index[0]
            if kwargs.get("relative", False): da.values = da.values / da[(da.meas_type == Subtest.STRESS.value) & (da.stress_time == 0.0)].values
            subset.append(da.sel(time = t_ind))
        return subset


if __name__ == "__main__":
    pass

