import random


class TensorSim:
    """
    Simulates predictions for a given dataset at a given accuracy threshold
    """

    def __init__(self, df, data_cols, target_cols, sim_accuracy=None,
                 shuffle=False):

        if shuffle:
            self.df = df.sample(frac=1)
        else:
            self.df = df

        self.data_cols = data_cols
        self.target_cols = target_cols
        self.sim_accuracy = sim_accuracy
        self.shuffle = shuffle

        self.idx = 0

        print('TensorSim summary:')
        print('\tNumber of samples:', self.n_samples)
        print('\tData columns:', ', '.join(self.data_cols))
        print('\tTarget columns:', ', '.join(self.target_cols))
        print(f'\tSimulated accuracy: {100*self.sim_accuracy}%')

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.idx < self.n_samples:

            data = self.data.iloc[self.idx]
            prediction = self.targets.iloc[self.idx]

            self.idx += 1

            for col, pred in prediction.iteritems():

                if random.uniform(0, 1) > self.sim_accuracy:

                    incorrect_set = {value for value in self.target_set[col]
                                     if value != pred}

                    value_override = random.choice(tuple(incorrect_set))
                    prediction[col] = value_override

                    print(f'Generating incorrect! {pred} -> {value_override}')

                else:
                    print('Generating correct!')

            if self.idx == (self.n_samples - 1):
                print('Resetting index!')
                self.idx = 0

            return data, prediction

    @property
    def data(self):
        return self.df[self.data_cols]

    @property
    def targets(self):
        return self.df[self.target_cols]

    @property
    def n_samples(self):
        return self.df.shape[0]

    @property
    def n_features(self):
        return len(self.data)

    @property
    def n_targets(self):
        return len(self.targets)

    @property
    def target_set(self):
        return {col: self.targets[col].unique() for col in self.target_cols}
