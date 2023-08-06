from HTOL.analysis.analysis import OVERFLOW_OVERWRITE
from HTOL.rename_file_parser import RenameFileParser
from os import name
import re
import logging
from HTOL.support import create_dt_flag, Subtest
from multiprocessing import Process
from pathlib import Path
from time import process_time
from numpy import float64, nan, unicode_
import pandas as pd
import xarray as xr

FULL_REGEX = re.compile(r"^(?P<date>\d+)_(?P<oven_nr>\d)_(?P<card_nr>\d)_(?P<name>.+?)_(?P<it>[A-Z])_(?P<temp>\d{2,3})C_(?P<volt>[0-9_]+)(?P<down>b)?V(?P<cool>coolto\d{2,3}C)?(?P<flag>[a-z])?$")
DIE_REGEX = re.compile(r"^(?P<str_b>[A-Za-z]+)(?P<str_nr>\d{2})_(?P<proc>P\d{4})_(?P<purp>[^_]+)_(?P<lot>V?P\d{5,6}[^_]*)_(?P<w_nr>D\d{2})_(?P<d_pos>\d{1,3})[A-Z]?_(?P<sub>\d{3})_(?P<orient>[a-z]+)_(?P<state_flag>S\d)$")
PURPOSE_REGEX = re.compile(r"^(?P<purp_type>[A-Za-z]+)(?P<purp_nr>\d+)$")
DUT_STRINGS = ["DUT_1_1", "DUT_1_2", "DUT_1_3", "DUT_1_4", "DUT_2_1", "DUT_2_2", "DUT_2_3", "DUT_2_4", "DUT_3_1", "DUT_3_2", "DUT_3_3", "DUT_3_4", "DUT_4_1", "DUT_4_2", "DUT_4_3", "DUT_4_4", "DUT_5_1", "DUT_5_2", "DUT_5_3", "DUT_5_4"]
DUT_MAPPING = dict(zip([f"{x:02d}.txt" for x in range(1,21)], DUT_STRINGS))    
OVERFLOW_OVERWRITE = nan

def analyze_file(setup_dir, output_dir, docs = None, overview = None):
    Path(output_dir).mkdir(parents = True, exist_ok = True)
    naming = Path(setup_dir, f"{setup_dir.name}.csv")

    # if csv file is not found
    print(f"Processing: {setup_dir.name}")
    if naming.exists(): pass
    elif isinstance(docs, pd.DataFrame) and setup_dir.name in docs.index:
        name_ser = docs.loc[setup_dir.name, :].dropna()
        naming = dict()
        for dut, name in name_ser.iteritems():
            m = DIE_REGEX.search(name)
            if m == None: 
                logging.error(f" {name}: Incorrect die header")
                name_ser.drop(labels = [name], inplace = True)
                continue
            else: md = m.groupdict()
            # check if lot is correct
            # if active_purp_wafer != f"{md['purp']}_{md['w_nr']}":
            #     active_purp_wafer = f"{md['purp']}_{md['w_nr']}"
            #     m_purp = PURPOSE_REGEX.search(md["purp"])
            #     if m_purp == None: logging.info(f" {md['purp']}: Purpose in wrong format - could not verify lot number")
            #     else:
            #         lot_overview = overview[(overview.Purpose == m_purp.group("purp_type")) & (overview.WQ == float(m_purp.group("purp_nr"))) & (overview.Wfr == md["w_nr"])]
            #         if len(lot_overview) == 0: logging.error(f" {active_purp_wafer}: no mapping in summary table")
            #         elif len(lot_overview) == 1:    
            #             lot_table = lot_overview.loc[lot_overview.index[0], "Lot"]
            #             if lot_table != md["lot"]: logging.error(f" {active_purp_wafer}: mapping not consistent (overview - {lot_table} vs word - {md['lot']})")
            #         else: logging.error(f" {active_purp_wafer}: ambigious mapping in summary table")
            naming[dut] = md
    else:
        logging.error(f"{setup_dir.name}: Could not declare all measurement specifications, not transferred")
        print(f"{setup_dir.name}: Could not declare all measurement specifications, not transferred")
        return None

    analyze_setup(setup_dir, naming, output_dir)

def analyze_files(data_dir, output_dir, docs = None, overview = None):
    logging.basicConfig(filename = f"logs/convertion_da_{create_dt_flag()}.log", level = logging.DEBUG)
    # Path(output_dir, "data_set").mkdir(parents = True, exist_ok = True)
    Path(output_dir).mkdir(parents = True, exist_ok = True)

    for setup in data_dir.glob("./*_*_*_*/"):
        # skip dirs
        if not setup.is_dir(): continue
        # process
        analyze_file(setup, output_dir, docs, overview)

def analyze_setup(setup, naming, output_dir):
    ## CREATE MAIN_DF
    main_df = pd.DataFrame()
    if isinstance(naming, dict):
        name_dict = naming
        pkl = False
    else:
        parser = RenameFileParser(naming)
        pkl = True
        name_dict = parser.get_details()

    ## CREATE TOP LEVEL VARS
    setup_string = "_".join(setup.name.split("_")[:3])
    lab_setup = "HTOL" if setup.name.split("_")[1].isnumeric() else setup.name.split("_")[1].capitalize()

    ## CREATE SUBSET OVERVIEW
    # subtest_overview = pd.DataFrame()
    subtest_list = []
    for subtest in setup.glob("./[0-9][0-9][0-9][0-9]*_*/"):
        # skip dirs
        if not subtest.is_dir(): continue
        # perform regex
        m = FULL_REGEX.search(subtest.name)
        if m == None:
            logging.error(f" ./{setup.name}/{subtest.name}: not a suitable folder name")
            continue
        d = m.groupdict()
        df = pd.DataFrame(data = d, index = [0])
        # add/overwrite
        df["folder"] = [subtest]
        df["volt"] = [parse_volt(m.group("volt"))]
        # append
        subtest_list.append(df)
    subtest_overview = pd.concat(subtest_list, ignore_index=True)
    # post process
    subtest_overview.replace({None: False, "b": True}, inplace = True)
    subtest_overview["meas_type"] = subtest_overview.apply(lambda x: get_meas_type(x), axis = 1)
    subtest_overview["prio"] = subtest_overview.meas_type.pipe(define_prio)

    #! NECESSARY?: FOR ITERATION A - UP AND DOWN IN DATASET
    # temp = subtest_overview[(subtest_overview.it == "A") & (subtest_overview.meas_type == "CHAR-UP")].copy()
    # if not temp.empty:
    #     temp["meas_type"] = "CHAR-DOWN"
    #     subtest_overview = subtest_overview.append(temp, ignore_index = True)

    subtest_overview.sort_values(by = ["it", "prio", "temp"], inplace = True)

    # subs = []
    for sub in subtest_overview.apply(process_line, args = (name_dict, ), axis = 1):
        if sub.empty: continue
        if not main_df.empty: 
            sub["time"] = sub.time + 1 + main_df.time.max() # add 1 seconds to be sure
        main_df = main_df.append(sub, ignore_index = True) # concat is annoying because of time series alteration
    #     subs.append(sub)
    # main_df = pd.concat(subs, ignore_index = True)
    main_df["meas_voltage"] = [nan] * len(main_df)
    main_df["meas_temperature"] = [nan] * len(main_df)
    main_df["stress_time"] = create_stress_time(main_df)
    main_df["step_ch"] = main_df.meas_type != main_df.meas_type.shift(1)
    main_df.sort_index(axis = 1, ascending = False, inplace = True)
    
    # if "STRESS" in list(subtest_overview.meas_type):
    #     stress_voltage_max = subtest_overview[subtest_overview.meas_type == "STRESS"].volt.max()
    #     stress_temp_max = subtest_overview[subtest_overview.meas_type == "STRESS"].temp.max()
    if 4 in list(subtest_overview.meas_type):
        stress_voltage_max = subtest_overview[subtest_overview.meas_type == Subtest.STRESS.value].volt.max()
        stress_temp_max = subtest_overview[subtest_overview.meas_type == Subtest.STRESS.value].temp.max()
    else:
        logging.info(" No stress level detected")
        return None
        # continue

    # meta = main_df.iloc[:, 0:6]
    # ensure data types
    # meta["set_temperature"] = meta.set_temperature.astype(float64) 
    # meta["meas_temperature"] = meta.meas_temperature.astype(float64)
    # meta["set_voltage"] = meta.set_voltage.astype(float64)
    # meta["meas_voltage"] = meta.meas_voltage.astype(float64)

    # main = ["set_voltage", "set_temperature", "meas_voltage", "meas_type", "meas_temperature"]
    # purp, lot, struct, wafer, proc, d_pos, sub, orient, state_flag  = ["meta"] * 5, ["meta"] * 5, ["meta"] * 5, ["meta"] * 5, ["meta"] * 5, ["meta"] * 5, ["meta"] * 5, ["meta"] * 5, ["meta"] * 5
    main, purpose, lot, structure, wafer, process, d_pos, subdie, orientation, status_flag = [], [], [], [], [], [], [], [], [], []
    for col in list(main_df.columns)[8:]:
        main.append(col)
        d = name_dict[col]

        d_pos.append(f"{d['die_pos']:>03}" if pkl else f"{d['d_pos']:>03}")
        subdie.append(f"{d['subdie']:>03}" if pkl else f"{d['sub']:>03}")
        orientation.append(d["orient"])
        status_flag.append(d["status_flag"] if pkl else d["state_flag"])
        
        purpose.append(d["purpose"] if pkl else d["purp"])
        lot.append(d["lot"])
        structure.append(d["structure"] if pkl else d["str_b"] + d["str_nr"])
        wafer.append(d["wafer_num"] if pkl else d["w_nr"])
        process.append(d["process"] if pkl else d["proc"])

    time = list(main_df.time)
    main_df.drop("time", axis = 1, inplace = True)
    main_df[main_df == 9.9e+37] = OVERFLOW_OVERWRITE

    ### DATAARRAY SOLUTION
    xr.DataArray(data = main_df[list(main_df.columns)[7:]], coords = {
        # dims
        "time": time,
        "dies": main,
        # meta data
        "stress_time": ("time", main_df.loc[:, "stress_time"]),
        "meas_type": ("time", main_df.loc[:, "meas_type"]),
        "step_change": ("time", main_df.loc[:, "step_ch"]),
        "set_voltage": ("time", main_df.loc[:, "set_voltage"]),
        "meas_voltage": ("time", main_df.loc[:, "meas_voltage"]),
        "set_temperature": ("time", main_df.loc[:, "set_temperature"]),
        "set_temperature": ("time", main_df.loc[:, "set_temperature"]),
        # die specifications
        "purpose": ("dies", purpose),
        "lot": ("dies", lot),
        "structure": ("dies", structure),
        "wafer": ("dies", wafer),
        "process": ("dies", process),
        "d_pos": ("dies", d_pos),
        "subdie": ("dies", subdie),
        "orientation": ("dies", orientation),
        "status_flag": ("dies", status_flag),
        "stress_max": ("dies", [f"{int(stress_temp_max)}C_{float(stress_voltage_max):.1f}V"]  * len(purpose))
        # "stress_temp_max": ("dies", [float(stress_temp_max)] * len(purpose)), # to faciliate filtering
        # "stress_temp_max": float(stress_temp_max), # to faciliate filtering
        # "stress_voltage_max": ("dies", [float(stress_voltage_max)] * len(purpose)), # to faciliate filtering
        # "stress_voltage_max": float(stress_voltage_max), # to faciliate filtering
    }, dims = ["time", "dies"], attrs = {
        "setup": setup_string,
        "lab_setup": lab_setup
    }).to_netcdf(Path(output_dir, f"{setup_string}.nc"))

def generate_path(p : Path, i : int = 1):
    p_temp = Path(p, f"SETUP{i:02d}")
    if not p_temp.exists(): return p_temp
    else:
        i += 1
        return generate_path(p, i)

def get_meas_type(ser):
    if ser.cool: return Subtest.TEMPDOWN.value
    if float(ser.temp) == 25.0: return Subtest.STARTUP.value
    elif isinstance(ser.volt, tuple) or float(ser.temp) == 85.0 or float(ser.temp) == 125.0:
        if ser.down: return Subtest.CHARDOWN.value
        else: return Subtest.CHARUP.value
    else:
        return Subtest.STRESS.value

def find_meas_type_order(df):
    target = pd.DataFrame(columns = ["meas_type"])
    target = df[df.meas_type.shift(1) != df.meas_type][["meas_type"]] # as dataframe
    target["start_ind"] = list(target.reset_index()["index"])
    target["end_ind"] = (target.start_ind.shift(-1, fill_value = len(df)) - 1).astype(int)
    return target

def create_stress_time(data):
    target = find_meas_type_order(data)
    if target[target.meas_type == Subtest.STRESS.value].empty: return list(data.time)
    wr_start = 0
    rem = 0
    stress_time = []
    for row in target[target.meas_type == Subtest.STRESS.value].iterrows():
        ser = data.loc[row[1].start_ind : row[1].end_ind, "time"]
        ser = ser - ser[row[1].start_ind]
        stress_time += [ser[row[1].start_ind] + rem] * (row[1].start_ind - wr_start)
        ser = ser + rem
        stress_time += list(ser)
        wr_start = row[1].end_ind + 1
        rem = ser[row[1].end_ind]
    if len(stress_time) < len(data): stress_time += [stress_time[-1]] * (len(data) - len(stress_time)) 
    return stress_time

def parse_volt(v):
    if "_" in v:
        if v.count("_") == 1:
            return float(v.replace("_", "."))
        else: raise AttributeError("cannot parse voltage")
    elif v.isnumeric() and len(v) > 2:
        if len(v) % 2 == 0:
            return tuple(float(v[i*2:2+i*2])/10 for i in range(int(len(v)/2)))
        else: raise AttributeError("cannot parse voltage")
    else:
        return float(v)

def define_prio(ser):
    d = {
        "STARTUP": 0,
        "CHAR-UP": 1,
        "TEMP-UP": 2,
        "STRESS": 3,
        "TEMP-DOWN": 4,
        "CHAR-DOWN": 5
    }
    return ser.replace(d)

def process_line(ser, name_dict):
    t = pd.DataFrame()
    d = pd.DataFrame()
    for file in ser.folder.glob("[0-9][0-9].txt"):
        descr = DUT_MAPPING[file.name]
        if not descr in name_dict.keys(): 
            continue
        temp = pd.read_csv(file, delimiter = "\t", names = ["time", "unit"], engine = "c")
        t[descr] = temp.time
        d[descr] = temp.unit
        d["meas_type"] = [ser.meas_type] * len(d)
        if isinstance(ser.volt, tuple):
            v = []
            for x in ser.volt:
                v += [x] * 2
            if len(v) != len(d):
                a = [v[-1]] * (len(d) - len(v))
                v += a
            d["set_voltage"] = v
        else: d["set_voltage"] = [float(ser.volt)] * len(d)
        d["set_temperature"] = [float(ser.temp)] * len(d)
        d["time"] = t.mean(axis = 1)/3600 # in hours
    # if not main_df.empty: d.time = d.time + main_df.time[main_df.index[-1]]
    # if not main_df.empty:
    #     main_df.time.max()
    #     d["time"] = d.time + main_df.time.max()
    return d

    