import pandas
import numpy as np


def find_closest_date(timepoint, time_series, add_time_delta_column=True):
    # takes a pd.Timestamp() instance and a pd.Series with dates in it
    # calcs the delta between `timepoint` and each date in `time_series`
    # returns the closest date and optionally the number of days in its time delta
    """ timepoint=pandas.to_datetime(str(timepoint), format='%Y-%m-%d')
    print(timepoint)
    time_series=pandas.to_datetime(str(time_series), format='%Y-%m-%d') """
    print(time_series)
    deltas = np.abs(time_series - timepoint)
    print(deltas)
    idx_closest_date = np.argmin(deltas)
    print(idx_closest_date)
    res = {"closest_date": time_series.loc[idx_closest_date]}
    idx = ['closest_date']
    if add_time_delta_column:
        res["closest_delta"] = deltas[idx_closest_date]
        idx.append('closest_delta')
    return pandas.Series(res, index=idx)


def merge_data(ranks, matches):
    """ matches[['closest', 'days_bt_x_and_y']] = matches.date.apply(
        lambda x: find_closest_date(x, ranks.loc[ranks['date'] == max(ranks['date'])]['date'])) """

    ranks = ranks.loc[ranks['date'] == max(ranks['date'])].drop_duplicates()
    # merge winner id to get rank and points

    matches = matches.merge(ranks, how='left',
                            left_on=['winner_id'], right_on=['id'])

    matches = matches.drop(columns=['name', 'state', 'id', 'date_y'])
    matches = matches.rename(
        columns={'date_x':'date','rank': 'winner_rank', 'points': 'winner_points'})

    # merge loser id to get rank and points

    matches = matches.merge(ranks, how='left',
                            left_on=['loser_id'], right_on=['id'])

    matches = matches.drop(columns=['name', 'state', 'id', 'date_y'])
    matches = matches.rename(
        columns={'date_x':'date','rank': 'loser_rank', 'points': 'loser_points'})

    matches['winner_rank'] = matches['winner_rank'].fillna(0)
    matches['winner_points'] = matches['winner_points'].fillna(0)
    matches['loser_rank'] = matches['loser_rank'].fillna(0)
    matches['loser_points'] = matches['loser_points'].fillna(0)

    matches['winner_rank'] = matches['winner_rank'].astype(int)
    matches['winner_points'] = matches['winner_points'].astype(int)
    matches['loser_rank'] = matches['loser_rank'].astype(int)
    matches['loser_points'] = matches['loser_points'].astype(int)

    return matches


matches2018 = pandas.read_csv('data/2018.csv')
matches2019 = pandas.read_csv('data/2019.csv')
matches2020 = pandas.read_csv('data/2020.csv')

matches2018['date'] = matches2018['date'].apply(
    lambda x: pandas.to_datetime(str(x), format='%Y-%m-%d'))
matches2019['date'] = matches2019['date'].apply(
    lambda x: pandas.to_datetime(str(x), format='%Y-%m-%d'))
matches2020['date'] = matches2020['date'].apply(
    lambda x: pandas.to_datetime(str(x), format='%Y-%m-%d'))

ranks2018 = pandas.read_csv('data/2018ranks.csv')
ranks2019 = pandas.read_csv('data/2019ranks.csv')
ranks2020 = pandas.read_csv('data/2020ranks.csv')

ranks2018['date'] = ranks2018['date'].apply(
    lambda x: pandas.to_datetime(str(x), format='%Y-%m-%d'))
ranks2019['date'] = ranks2019['date'].apply(
    lambda x: pandas.to_datetime(str(x), format='%Y-%m-%d'))
ranks2020['date'] = ranks2020['date'].apply(
    lambda x: pandas.to_datetime(str(x), format='%Y-%m-%d'))


#ranks = pandas.concat([ranks2018, ranks2019, ranks2020], ignore_index=True)

final2018 = merge_data(ranks2018, matches2018)
final2019 = merge_data(ranks2019, matches2019)
final2020 = merge_data(ranks2020, matches2020)

final2018.to_csv('data/final2018.csv', index=False)
final2019.to_csv('data/final2019.csv', index=False)
final2020.to_csv('data/final2020.csv', index=False)
