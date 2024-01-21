from flask import Flask, jsonify, request
from collections import deque

# Define the Person and Graph classes
class Person:
    def __init__(self, name):
        self.name = name
        self.friends = set()
        self.possessions = set()

    def add_friend(self, friend):
        self.friends.add(friend)

    def add_possession(self, item):
        self.possessions.add(item)

class Graph:
    def __init__(self):
        self.people = {}

    def add_person(self, name):
        if name not in self.people:
            self.people[name] = Person(name)

    def add_friendship(self, name1, name2):
        if name1 in self.people and name2 in self.people:
            self.people[name1].add_friend(name2)
            self.people[name2].add_friend(name1)
        else:
            raise Exception("Both people must be added to the graph before creating a friendship.")

    def add_possession(self, name, item):
        if name in self.people:
            self.people[name].add_possession(item)
        else:
            raise Exception("Person must be added to the graph before assigning possessions.")

# Initialize the graph
graph = Graph()

# Define the function to find the shortest path to a person with a desired item
def find_path_to_borrow(graph, start_name, item):
    visited = set()
    queue = deque([[start_name]])
    
    while queue:
        path = queue.popleft()
        person_name = path[-1]
        
        if person_name not in visited:
            visited.add(person_name)
            person = graph.people[person_name]
            
            if item in person.possessions:
                return path  # Return the path to the person who has the item
            
            for friend in person.friends:
                if friend not in visited:
                    new_path = list(path)
                    new_path.append(friend)
                    queue.append(new_path)
    
    return None  # If there is no path to someone with the item

# Flask app definition
app = Flask(__name__)

# API endpoint to get a list of friends
@app.route('/friends', methods=['GET'])
def get_friends():
    name = request.args.get('name')
    person = graph.people.get(name)
    if person:
        return jsonify({"friends": list(person.friends)})
    else:
        return jsonify({"error": "Person not found"}), 404

# API endpoint to check if two people know each other
@app.route('/knows', methods=['GET'])
def get_knows():
    name1 = request.args.get('person1')
    name2 = request.args.get('person2')
    person1 = graph.people.get(name1)
    if person1 and name2 in person1.friends:
        return jsonify({"knows": True})
    else:
        return jsonify({"knows": False})

# API endpoint to find the shortest path to borrow an item
@app.route('/borrow', methods=['GET'])
def get_borrow_path():
    name = request.args.get('name')
    item = request.args.get('item')
    path = find_path_to_borrow(graph, name, item)
    if path:
        return jsonify({"path": path})
    else:
        return jsonify({"error": "No path found to borrow the item"}), 404

# This would run your Flask app on localhost, port 5000
# app.run(debug=True)

# Main execution (for demonstration, add people, friendships, and possessions)
if __name__ == '__main__':
    # Add people to the graph
    graph.add_person('Kamil')
    graph.add_person('Magda')
    graph.add_person('Ewa')
    graph.add_person('Piotr')
    graph.add_person('Nikodem')
    graph.add_person('Mikolaj')
    graph.add_person('Liliana')
    graph.add_person('Daniel')
    # Add friendships
    graph.add_friendship('Kamil', 'Magda', 'Piotr', 'Daniel')
    graph.add_friendship('Magda', 'Kamil', 'Liliana')
    graph.add_friendship('Ewa', 'Magda', 'Liliana', 'Daniel')
    graph.add_friendship('Piotr', 'Kamil', 'Liliana')
    graph.add_friendship('Nikodem', 'Mikołaj', 'Daniel')
    graph.add_friendship('Mikolaj', 'Daniel')
    graph.add_friendship('Liliana', 'Magda', 'Ewa')
    graph.add_friendship('Daniel', 'Kamil', 'Ewa', 'Mikolaj')
    # Add possessions
    graph.add_possession('Magda', 'kamera')
    graph.add_possession('Piotr', 'kamera')
    graph.add_possession('Mikolaj', 'kamera')
    graph.add_possession('Liliana', 'kamera')
    graph.add_possession('Piotr', 'statyw')
    # app.run(debug=True)
