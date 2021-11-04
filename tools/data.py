import pandas

# generic object from which the subsequent data objects will derive.
# holds most of the shared methods.


class Data(object):

    # if gew_data or panas_data are empty the object will fetch them from CSV.
    gew_data = False
    panas_data = False
    # default column names, may differ depending on result set.
    email_name = "EMAIL"
    id_name = 'ID'

    # data is fetched on initialization.
    def __init__(self):
        self.gew_data = self.get_gew_data()
        self.panas_data = self.get_panas_data()

    # returns data for the GEW, only fetches it if not present or force is set to `True`.
    def get_gew_data(self, force=False):
        if self.gew_data is False or force is True:
            return self._get_gew_data()
        else:
            return self.gew_data

    # same as above but for PANAS data.
    def get_panas_data(self, force=False):
        if self.panas_data is False or force is True:
            return self._get_panas_data()
        else:
            return self.panas_data

    # abstract function that needs to be implemented in child class.
    # Will fetch the GEW data according to specifications inherent to the result set (as defined in child class).
    def _get_gew_data(self):
        pass

    def _get_panas_data(self):
        pass

    # processes and returns the GEW data in three parts: the numerica data, the indices, and the "other" options.
    def return_gew_data(self, data, slice_1, slice_2):
        otherCols = ['OTHER1', 'OTHER2', 'OTHER3', 'OTHER4', 'OTHER5', 'OTHER6', 'OTHER7', 'OTHER8', 'OTHER9',
                     'OTHER10', 'OTHER11', 'OTHER12', 'OTHER13', 'OTHER14', 'OTHER15', 'OTHER16', 'OTHER17', 'OTHER18']

        gew_data_num = data.iloc[:, slice_1:slice_2].apply(
            lambda x: pandas.notna(x) if x.name in otherCols else x)
        gew_data_num = gew_data_num.fillna(0).astype(int)
        gew_data_index = data[['Duration (in seconds)', self.email_name]].astype(
            {'Duration (in seconds)': 'int64', self.email_name: 'string'})

        gew_data_other = data[otherCols].fillna("").astype(str)

        return [gew_data_num, gew_data_index, gew_data_other]

    # processes and returns the PANAS data in two parts: the numerica data, and the indices.
    def return_panas_data(self, data, slice_1, slice_2):
        panas_data_num = data.iloc[:, slice_1:slice_2].fillna(
            1).apply(pandas.to_numeric)
        panas_data_index = data[['Duration (in seconds)', self.email_name]].astype(
            {'Duration (in seconds)': 'int64', self.email_name: 'string'})

        return [panas_data_num, panas_data_index]

    # returns only the numeric data for the GEW.
    def get_gew_num_data(self, force=False):
        return self.get_gew_data(force)[0]

    # returns the numerica data associated with the indices.
    def get_gew_assoc_data(self, force=False):
        gdat = self.get_gew_data(force)
        gdat = gdat[1].join(gdat[0])
        return gdat

    # returns only the "other" options from the GEW data. Associated with indices.
    def get_gew_other_data(self, force=False):
        gdat = self.get_gew_data(force)
        return gdat[1].join(gdat[2])

    # returns only the numeric data for PANAS
    def get_panas_num_data(self, force=False):
        return self.get_panas_data(force)[0]

    # returns the numeric data associated with the indices.
    def get_panas_assoc_data(self, force=False):
        pdat = self.get_panas_data(force)
        pdat = pdat[1].join(pdat[0])
        return pdat

# Fetches the data from the first result set, which is gathered in a single CSV file


class FirstData(Data):

    def __init__(self, file):
        fdata = pandas.read_csv(file).drop(index=[0, 1]).reset_index()
        fdata = fdata.rename({"ResponseId": "ID"}, axis="columns")
        fdata.set_index(self.id_name, inplace=True)
        fdata.sort_index(inplace=True)
        self.data = fdata
        Data.__init__(self)

    def _get_gew_data(self):
        gew_data = self.data[pandas.isna(self.data["Q2.1_1"])]
        return self.return_gew_data(gew_data, 380, 776)

    def _get_panas_data(self):
        panas_data = self.data[pandas.notna(self.data["Q2.1_1"])]
        return self.return_panas_data(panas_data, 20, 380)

# Fetches the data from the second result set, which is split between two CSVs


class SecondData(Data):

    def __init__(self, file_gew, file_panas):
        self.file_gew = file_gew
        self.file_panas = file_panas
        self.email_name = "RecipientEmail1"
        self.id_name = "ID"
        Data.__init__(self)

    def _get_gew_data(self):
        data = pandas.read_csv(self.file_gew).drop(index=[0, 1]).reset_index()
        data.set_index(self.id_name, inplace=True)
        data.sort_index(inplace=True)
        return self.return_gew_data(data, 23, 419)

    def _get_panas_data(self):
        data = pandas.read_csv(self.file_panas).drop(
            index=[0, 1]).reset_index()
        data.set_index(self.id_name, inplace=True)
        data.sort_index(inplace=True)
        return self.return_panas_data(data, 23, 383)


# returns only the numerical data from both sets of results, seperated by method
def get_num_data_per_method(FirstData: pandas.DataFrame, SecondData: pandas.DataFrame) -> dict:
    # these variables will store the results using the Geneva Emotion wheel
    firstNumGEW = FirstData.get_gew_num_data()
    secondNumGEW = SecondData.get_gew_num_data()

    # Only preserves results from respondents who answered both surveys
    firstNumGEW = firstNumGEW[firstNumGEW.index.isin(
        secondNumGEW.index.values)]
    secondNumGEW = secondNumGEW[secondNumGEW.index.isin(
        firstNumGEW.index.values)]
    # same as above but for results using the PANAS
    firstNumPANAS = FirstData.get_panas_num_data()
    secondNumPANAS = SecondData.get_panas_num_data()

    firstNumPANAS = firstNumPANAS[firstNumPANAS.index.isin(
        secondNumPANAS.index.values)]
    secondNumPANAS = secondNumPANAS[secondNumPANAS.index.isin(
        firstNumPANAS.index.values)]

    return {'GEW': [firstNumGEW, secondNumGEW], 'PANAS': [firstNumPANAS, secondNumPANAS]}
