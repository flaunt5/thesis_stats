import pandas


class Data(object):

    gew_data = False
    panas_data = False
    email_name = "EMAIL"
    id_name = 'ID'

    def __init__(self):
        self.gew_data = self.get_gew_data()
        self.panas_data = self.get_panas_data()

    def get_gew_data(self, force=False):
        if self.gew_data is False or force is True:
            return self._get_gew_data()
        else:
            return self.gew_data

    def get_panas_data(self, force=False):
        if self.panas_data is False or force is True:
            return self._get_panas_data()
        else:
            return self.panas_data

    def _get_gew_data(self):
        pass

    def _get_panas_data(self):
        pass

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

    def return_panas_data(self, data, slice_1, slice_2):
        panas_data_num = data.iloc[:, slice_1:slice_2].fillna(
            1).apply(pandas.to_numeric)
        panas_data_index = data[['Duration (in seconds)', self.email_name]].astype(
            {'Duration (in seconds)': 'int64', self.email_name: 'string'})

        return [panas_data_num, panas_data_index]

    def get_gew_num_data(self, force=False):
        return self.get_gew_data(force)[0]

    def get_gew_assoc_data(self, force=False):
        gdat = self.get_gew_data(force)
        gdat = gdat[1].join(gdat[0])
        return gdat

    def get_gew_other_data(self, force=False):
        gdat = self.get_gew_data(force)
        return gdat[1].join(gdat[2])

    def get_panas_num_data(self, force=False):
        return self.get_panas_data(force)[0]

    def get_panas_assoc_data(self, force=False):
        pdat = self.get_panas_data(force)
        pdat = pdat[1].join(pdat[0])
        return pdat


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
