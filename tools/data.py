import pandas


class Data(object):

    gew_data = False
    panas_data = False
    email_name = "EMAIL"

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

        gew_data_num = data.iloc[:, slice_1:slice_2]
        gew_data_num = gew_data_num.drop(
            otherCols, axis=1).fillna(0).astype(int)

        gew_data_index = data[['ResponseId', 'Duration (in seconds)', self.email_name]].astype(
            {'ResponseId': 'string', 'Duration (in seconds)': 'int64', self.email_name: 'string'})

        gew_data_other = data[otherCols].fillna("").astype(str)

        return [gew_data_num, gew_data_index, gew_data_other]

    def return_panas_data(self, data, slice_1, slice_2):
        panas_data_num = data.iloc[:, slice_1:slice_2].fillna(
            1).apply(pandas.to_numeric)

        panas_data_index = data[['ResponseId', 'Duration (in seconds)', self.email_name]].astype(
            {'ResponseId': 'string', 'Duration (in seconds)': 'int64', self.email_name: 'string'})

        return [panas_data_num, panas_data_index]

    def get_gew_num_data(self, force=False):
        return self.get_gew_data(force)[0]

    def get_gew_assoc_data(self, force=False):
        return self.get_gew_data(force)[1].join(self.gew_data[0])

    def get_gew_other_data(self, force=False):
        return self.get_gew_data(force)[1].join(self.gew_data[2])

    def get_panas_num_data(self, force=False):
        return self.get_panas_data(force)[0]

    def get_panas_assoc_data(self, force=False):
        return self.get_panas_data(force)[1].join(self.get_panas_data()[0])


class FirstData(Data):

    def __init__(self, file):
        self.data = pandas.read_csv(file).drop(index=[0, 1]).reset_index()
        Data.__init__(self)

    def _get_gew_data(self):
        gew_data = self.data[pandas.isna(self.data["Q2.1_1"])]
        return self.return_gew_data(gew_data, 383, 778)

    def _get_panas_data(self):
        panas_data = self.data[pandas.notna(self.data["Q2.1_1"])]
        return self.return_panas_data(panas_data, 22, 382)


class SecondData(Data):

    def __init__(self, file_gew, file_panas):
        self.file_gew = file_gew
        self.file_panas = file_panas
        self.email_name = "RecipientEmail1"
        Data.__init__(self)

    def _get_gew_data(self):
        data = pandas.read_csv(self.file_gew).drop(index=[0, 1]).reset_index()
        return self.return_gew_data(data, 24, 419)

    def _get_panas_data(self):
        data = pandas.read_csv(self.file_panas).drop(
            index=[0, 1]).reset_index()
        return self.return_panas_data(data, 23, 383)
