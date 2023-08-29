import math
import random

from field.map import Map
from model.multicopter import Multi
from model.vtol import Vtol

class multiDR:

    def __init__(self,mapFilePath,drone_num) -> None:
        self.map = Map(mapFilePath)
        self.multi = Multi()
        self.vtol = Vtol()
        self.route_list = [] #機体数分のルートベクトル
        self.drone_num = drone_num
        
    def move():
        pass
    
    def exchange():
        pass
    
    def multi_TSP():
        pass
    
    def vtol_TSP():
        pass
    
    def serch_best_routing():
        #multi_TSP()とvtol_TSP()を比べていい結果のほうを取得
    
    def SA(self):
        #ここから初期解作成
        #ノード仕分けの母集団作成
        customer_list = []
        for i in range(self.map.CN):
            customer_list.append(i+1)
        #ランダム解生成
        #機体数分のベクトルをroute_listに追加
        #母集団からランダムでroute_listに仕分け
        
        #各ベクトルにおいて巡回セールスマン問題の厳密解を求める
        self.serch_best_routing()
        
        initial_temp = 100 #初期温度
        final_temp = 0 #最終温度
        current_temp = initial_temp #現在の温度
        
        while current_temp > final_temp :
            pass


def simulated_annealing(customers, num_vehicles, vehicle_capacity, energy_capacities, energy_efficiencies, initial_temperature, cooling_rate, iterations):
    num_customers = len(customers)
    depot = 0  # Depot is always at index 0
    best_solution = None
    best_cost = float('inf')
    current_solution = []
    for _ in range(num_vehicles):
        current_solution.append([depot])
    current_cost = num_vehicles  # Initialize with number of vehicles
    temperature = initial_temperature

    while temperature > 0.1:
        for _ in range(iterations):
            vehicle_idx = random.randint(0, num_vehicles - 1)
            vehicle_tour = current_solution[vehicle_idx]
            if len(vehicle_tour) < 3:
                continue
            node_idx1, node_idx2 = random.sample(range(1, len(vehicle_tour)), 2)
            vehicle_tour[node_idx1], vehicle_tour[node_idx2] = vehicle_tour[node_idx2], vehicle_tour[node_idx1]

            new_distance = calculate_total_distance(vehicle_tour, customers)
            energy_consumption = calculate_energy_consumption(new_distance, energy_efficiencies[vehicle_idx])
            
            if new_distance <= current_cost and energy_consumption <= energy_capacities[vehicle_idx] or random.random() < math.exp((current_cost - new_distance) / temperature):
                current_cost = new_distance
            else:
                vehicle_tour[node_idx1], vehicle_tour[node_idx2] = vehicle_tour[node_idx2], vehicle_tour[node_idx1]

            if current_cost < best_cost:
                best_solution = [tour.copy() for tour in current_solution]
                best_cost = current_cost

        temperature *= cooling_rate

    return best_solution

if __name__ == "__main__":
    # Sample input data (customer number, x, y, demand)
    customers = [
        (0, 0, 0, 0),     # Depot
        (1, 1, 2, 10),
        (2, 3, 5, 12),
        (3, 6, 8, 5),
        (4, 10, 12, 8),
    ]

    num_vehicles = 2
    vehicle_capacity = 30
    energy_capacities = [150, 100]  # Capacities for two types of vehicles
    energy_efficiencies = [0.8, 0.6]  # Efficiencies for two types of vehicles
    initial_temperature = 1000
    cooling_rate = 0.95
    iterations = 100

    # Find the optimal solution using Simulated Annealing
    optimal_solution = simulated_annealing(customers, num_vehicles, vehicle_capacity, energy_capacities, energy_efficiencies, initial_temperature, cooling_rate, iterations)

    for i, vehicle_tour in enumerate(optimal_solution):
        print(f"Vehicle {i + 1} Tour: {vehicle_tour}")
