import numpy as np
import pandas as pd
import scipy.spatial.distance as sp_dist
from sklearn.cluster import KMeans
from time import perf_counter


def insertion(coord, method='nearest'):
    assert method in ['nearest', 'farthest']
    dist_mat = cdist(coord, coord)
    large_num = dist_mat.max() + 0.1

    # assuming depot is the first city
    selecting_op = np.argmin if method == 'nearest' else np.argmax
    mask_val = large_num if method == 'nearest' else -1.0 * large_num

    tour = [0, selecting_op(dist_mat[0, 1:]) + 1, 0]

    while len(tour) <= n:
        sub_dist_mat = dist_mat[tour, :]
        sub_dist_mat[:, tour] = mask_val
        next_idx = np.unravel_index(selecting_op(sub_dist_mat),
                                    sub_dist_mat.shape)[-1]
        src, dst = tour[:-1], tour[1:]
        dist_incr = dist_mat[src, next_idx] + dist_mat[next_idx, dst] - dist_mat[src, dst]
        tour.insert(dist_incr.argmin() + 1, next_idx)

    tour_length = np.sum(dist_mat[tour[:-1], tour[1:]])
    return tour, tour_length


def nearest_neighbor(coord):
    dist_mat = cdist(coord, coord)
    large_num = dist_mat.max() + 0.1

    tour = [0, np.argmin(dist_mat[0, 1:]) + 1]
    while len(tour) <= n:
        cur_city_idx = tour[-1]
        sub_dist_mat = dist_mat[cur_city_idx, :]
        sub_dist_mat[tour] = large_num
        tour.append(np.unravel_index(np.argmin(sub_dist_mat), sub_dist_mat.shape)[-1])

    tour_length = np.sum(dist_mat[tour[:-1], tour[1:]])
    return tour, tour_length


def solve_tsp(sub_coord, tsp_heuristics):
    if tsp_heuristics is 'NN':
        tour, tour_length = nearest_neighbor(coord)

    if tsp_heuristics in ['NI', 'FI']:
        _method = 'nearest' if tsp_heuristics == 'NI' else 'farthest'
        tour, tour_length = insertion(coord, _method)

    return tour, tour_length


def solve_twophase(m: int,  # Number of salesmen
                   n: int = None,  # Number of cities including the depot
                   coords: np.ndarray = None,  # Depot and cities positions [ n x 2]
                   tsp_heuristics: str = 'NI',
                   seed: int = None):  # random seed for generating city positions

    if seed is not None:
        np.random.seed(seed)

    assert n is None or coords is None
    if n is not None:  # generate positions on fly.
        # the first city serves as the depot following the convention
        coords = np.random.uniform(size=(n, 2))
        depot_coord = coords[0:1, :]
        city_coord = coords[1:, :]
    if coords is not None:
        n = coords.shape[0]
        depot_coord = coords[0:1, :]
        city_coord = coords[1:, :]

    start_time = perf_counter()
    kmeans = KMeans(n_clusters=m, random_state=0).fit(city_coord)

    assigned_cities = {_m: np.arange(1, n)[kmeans.labels_ == _m] for _m in range(m)}
    tours = dict()
    tour_length = dict()
    for _m in range(m):
        if len(assigned_cities[_m]) == 0:  # Not assigned to any city
            tours[_m] = []
            tour_length[_m] = 0.0
        elif len(assigned_cities[_m]) == 1:  # Assigned to a single city
            city_i = int(assigned_cities[_m][0])
            tours[_m] = [city_i]
            # the depot returning cost
            tour_length[_m] = 2 * sp_dist.cdist(depot_coord, city_coord[city_i - 1:city_i, :], metric='euclidean')
        else:
            sub_coords = np.vstack([depot_coord, city_coord[assigned_cities[_m] - 1, :]])
            tour, tour_length = solve_tsp(sub_coords, tsp_heuristics)

            # sub_dists = sp_dist.cdist(sub_coords, sub_coords, metric='euclidean')
            #
            # # initialize the tour
            # cur_city_idx = 0  # depot start
            # tour = []
            # tour_len = 0.0
            #
            # unvisit_cities = assigned_cities[_m].tolist()  # except the depot
            # cities = [0] + unvisit_cities  # including depot as the initial city.
            # dist_df = pd.DataFrame(sub_dists, index=cities, columns=cities)
            #
            # while len(unvisit_cities) >= 1:
            #     cur_df = dist_df.loc[cur_city_idx][dist_df.loc[cur_city_idx] > 0.0]
            #     n_city_idx = cur_df.index[get_next_city_idx(cur_df, tsp_heuristics)]
            #
            #     tour_len += float(cur_df.loc[n_city_idx])
            #     tour.append(int(n_city_idx))
            #     dist_df = dist_df.drop(columns=cur_city_idx)
            #     unvisit_cities.remove(n_city_idx)
            #     cur_city_idx = n_city_idx

            tours[_m] = tour
            tour_length[_m] = tour_length

    end_time = perf_counter()

    info = dict()

    # meta info
    info['solution_method'] = '2phase-{}'.format(tsp_heuristics)
    info['n'] = int(n)
    info['m'] = int(m)
    info['coords'] = coords

    # solution and solver conditions
    info['solve'] = True
    info['obj_val'] = max(tour_length.values())
    info['run_time'] = end_time - start_time
    return_tour = {k: [0] + v + [0] for k, v in tours.items()}  # appending the depot to the end and first
    info['tours'] = return_tour

    # additional performance metrics
    info['amplitude'] = max(tour_length.values()) - min(tour_length.values())
    info['total_length'] = float(sum(tour_length.values()))
    info['tour_length'] = tour_length

    n_inactive = 0
    for tl in info['tour_length'].values():
        if tl <= 0.0:
            n_inactive += 1
    info['n_inactive'] = n_inactive
    info['utilization'] = (m - n_inactive) / m

    return info
