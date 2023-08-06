import pandas as pd
from pathlib import Path
import xarray as xr

class RenameFileParser():
    COLUMNS = ["purpose", "lot", "structure", "process", "wafer_num", "die_pos", "subdie", "orient", "status_flag"]
    ROWS = ["DUT_1_1", "DUT_1_2", "DUT_1_3", "DUT_1_4", "DUT_2_1", "DUT_2_2", "DUT_2_3", "DUT_2_4", "DUT_3_1", "DUT_3_2", "DUT_3_3", "DUT_3_4", "DUT_4_1", "DUT_4_2", "DUT_4_3", "DUT_4_4", "DUT_5_1", "DUT_5_2", "DUT_5_3", "DUT_5_4"]
    DEFAULT_DICT = pd.DataFrame(columns = COLUMNS, index = ROWS).fillna("").to_dict(orient = "index")

    def __init__(self, file : str, duts_dir = None, name_sep = "_"):
        # PATH INFO
        if duts_dir == None:
            self.path = Path(file)
        else:
            self.duts_dir = duts_dir
            self.duts_dir.mkdir(exist_ok= True, parents = True)
            self.path = Path(self.duts_dir, file)

        # PROCESS EXCEL CSV NIGHTMARE
        with open(self.path, "r") as f:
            header = f.readline()
        self.delim = "," if header.count(",") > header.count(";") else ";"
        self.name_sep = name_sep

        # GENERATE CSV
        self.data = pd.read_csv(self.path, index_col=[0, 1], delimiter=self.delim).fillna(method="ffill").applymap(lambda x: x.strip() if isinstance(x, str) else x)
        self.data.drop(self.data[self.data.empty_slot == "yes"].index, inplace=True)
        self.data.drop("empty_slot", axis = 1, inplace = True)
        if self.data.die_pos.dtypes == "O" or self.data.die_pos.dtypes == "str": self.data["die_pos"] = self.data.die_pos.str.extract(r"(?P<n>\d+)[A-Za-z]?").n
        self.data["die_pos"] = self.data.die_pos.astype(int).apply(lambda x: f"{x:03d}")
        self.data["subdie"] = self.data.subdie.astype(int).apply(lambda x: f"{x:03d}")

    @property
    def renamed_dies(self):
        return list(self.data.apply(lambda x: self.name_sep.join(list(x)), axis = 1))

    @property
    def name(self):
        return self.path.name.split(".")[0]

    @property
    def die_names(self):
        return list(self.data.index.get_level_values("new_name"))

    def get_details(self, droplevel = "old_name"):
        return self.data.droplevel(droplevel).to_dict(orient = "index")

    def get_xarray(self):
        return xr.DataArray(coords = {
            # dims
            "time": [],
            "dies": self.die_names,
            # meta data
            "stress_time": ("time", []),
            "meas_type": ("time", []),
            "step_change": ("time", []),
            "set_voltage": ("time", []),
            "meas_voltage": ("time", []),
            "set_temperature": ("time", []),
            "set_temperature": ("time", []),
            # die specifications
            "purpose": ("dies", self.data.purpose),
            "lot": ("dies", self.data.lot),
            "structure": ("dies", self.data.structure),
            "wafer": ("dies", self.data.wafer_num),
            "process": ("dies", self.data.process),
            "d_pos": ("dies", self.data.die_pos),
            "subdie": ("dies", self.data.subdie),
            "orientation": ("dies", self.data.orient),
            "status_flag": ("dies", self.data.status_flag),
            "stress_max": ("dies", [""] * len(self.data.purpose))
        }, dims = ["time", "dies"], attrs = {
            "setup": "",
            "lab_setup": ""
        })

if __name__ == "__main__":
    parsed = RenameFileParser(Path(r"C:\Users\vsever71\Documents\playground\legacy_converter_test\raw_data\20210728_5_2_WQ54\20210728_5_2_WQ54.csv"))
    # print(parsed.get_xarray())
    # print(RenameFileParser.DEFAULT_DICT)