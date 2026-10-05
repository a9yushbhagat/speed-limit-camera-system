import check

class Camera:
    '''
    Fields: cam_id (Str), position_km (Float)
    '''

    def __init__(self, c, p):
        '''
        Constructor: Creates a Camera object by calling
        Camera(cam_id, position_km).

        Effects: Mutates self

        __init__: Camera Str Float -> None
        '''
        self.cam_id = c
        self.position_km = p

    def __repr__(self):
        '''
        Returns a string representation of self.

        __repr__: Camera -> Str
        '''
        s = "Camera({0.cam_id} at {0.position_km}km)"
        return s.format(self)
    
    def __eq__(self, other):
        '''
        Returns True if self and other are Cameras with the same
        cam_id, and False otherwise.

        __eq__: Camera Any -> Bool
        '''
        return isinstance(other, Camera) and \
               self.cam_id == other.cam_id
    
    def distance_to(self, other):
        '''
        Returns the distance in km between self and other,
        always non-negative.

        distance_to: Camera Camera -> Float

        Examples:
           If c1 = Camera("C1", 5.0) and c2 = Camera("C2", 15.5),
           then c1.distance_to(c2) => 10.5
        '''
        d = abs(self.position_km - other.position_km)
        return d 
    

class Reading:
    '''
    Fields: plate (Str), cam (Camera), time_s (Float)
    '''

    def __init__(self, p, c, t):
        '''
        Constructor: Creates a Reading object by calling
        Reading(plate, cam, time_s).

        Effects: Mutates self

        __init__: Reading Str Camera Float -> None
        '''
        self.plate = p
        self.cam = c
        self.time_s = t

    def __repr__(self):
        '''
        Returns a string representation of self.

        __repr__: Reading -> Str
        '''
        s = "Reading({0.plate} at {0.cam.cam_id}, {0.time_s})"
        return s.format(self)
    
    def __eq__(self, other):
        '''
        Returns True if self and other are Readings with the same
        plate, cam, and time_s, and False otherwise.

        __eq__: Reading Any -> Bool
        '''
        return isinstance(other, Reading) and \
               self.plate == other.plate and \
               self.cam == other.cam and \
               self.time_s == other.time_s 
    
def average_speed(r1, r2):
    '''
    Returns the average speed in km/h of the car that produced
    readings r1 and r2.

    average_speed: Reading Reading -> Float
    Requires: r1.time_s != r2.time_s

    Examples:
       If r1 = Reading("ABC", Camera("C1", 0.0), 36000.0) and
       r2 = Reading("ABC", Camera("C2", 10.0), 36240.0),
       then average_speed(r1, r2) => 150.0
    '''
    total_time = r2.time_s - r1.time_s
    time_hr = total_time / 3600
    avg = (r2.cam.position_km - r1.cam.position_km) / time_hr
    return avg
    
def is_speeding(r1, r2, limit):
    '''
    Returns True if the car that produced r1 and r2 was travelling
    above limit km/h, and False otherwise.

    is_speeding: Reading Reading Float -> Bool
    Requires: r1.time_s != r2.time_s
              limit > 0

    Examples:
       If average_speed(r1, r2) => 150.0 and limit = 100,
       then is_speeding(r1, r2, 100) => True
    '''
    final_speed = average_speed(r1, r2)
    if final_speed > limit:
        return True
    else:
        return False
    

class Highway:
    '''
    Fields: readings (listof Reading)
    '''

    def __init__(self):
        '''
        Constructor: Creates a Highway object by calling Highway().

        Effects: Mutates self

        __init__: Highway -> None
        '''
        self.readings = []

    def __repr__(self):
        '''
        Returns a string representation of self.

        __repr__: Highway -> Str
        '''
        s = "Highway({0} readings)"
        return s.format(len(self.readings))

    def __eq__(self, other):
        '''
        Returns True if self and other are Highways with the same
        readings, and False otherwise.

        __eq__: Highway Any -> Bool
        '''
        return isinstance(other, Highway) and \
               self.readings == other.readings

    def add_reading(self, r):
        '''
        Returns None.

        Effects: Mutates self.readings by adding r

        add_reading: Highway Reading -> None

        Examples:
           If h = Highway() and r = Reading("ABC", Camera("C1", 0.0),
           36000.0), then h.add_reading(r) => None and
           h.readings == [r]
        '''
        self.readings += [r]

    def get_readings(self, plate):
        '''
        Returns a list of all Readings in self.readings whose plate
        matches plate, in the order they were added.

        get_readings: Highway Str -> (listof Reading)

        Examples:
           If h contains readings for "ABC123" and "XYZ999",
           then h.get_readings("ABC123") returns only the
           ABC123 readings
        '''
        if self.readings == []:
            return []
        acc = []
        for r in self.readings:
            if r.plate == plate:
                acc += [r]
        return acc
    
    def find_speeders(self, limit):
        '''
        Returns a list of plates (no duplicates) of cars that were
        travelling above limit km/h between any two consecutive
        camera readings.

        find_speeders: Highway Float -> (listof Str)
        Requires: limit > 0

        Examples:
           If h contains two readings for "ABC123" where the car
           travelled 150 km/h and limit = 100,
           then h.find_speeders(100) => ["ABC123"]
        '''
        acc = []
        for r in self.readings:
            if r in acc:
              None
            else:
              acc += self.get_readings(r.plate)
        d = {}
        for c in acc:
            if c.plate in d:
              d[c.plate] += [c]
            else:
              d[c.plate] = [c]
        speeding = []
        for s in d:
            if len(d[s]) >= 2:
              r1 = d[s][0]
              r2 = d[s][1]
              if is_speeding(r1, r2, limit):
                speeding += [s]
        return speeding

def write_tickets(h, limit, filename):
    '''
    Returns None.

    Effects: Writes one line per speeding plate to filename in the
             form plate,speed where speed is rounded to 2 decimal
             places

    write_tickets: Highway Float Str -> None
    Requires: limit > 0

    Examples:
       If h contains ABC123 travelling at 150.0 km/h and limit = 100,
       then write_tickets(h, 100, "tickets.txt") => None and writes
       ABC123,150.0
       to tickets.txt
    '''
    fout = open(filename, "w")
    lst = h.find_speeders(limit)
    for plate in lst:
        readings = h.get_readings(plate)
        speed = average_speed(readings[0], readings[1])
        fout.write(plate + "," + str(round(speed, 2)) + "\n")
    fout.close()


## Tests:
c1 = Camera("C1", 0.0)
c2 = Camera("C2", 10.0)

check.within("Q1T1: c1 to c2", c1.distance_to(c2), 10.0, 0.001)
check.within("Q1T2: order does not matter", c2.distance_to(c1), 10.0, 0.001)

r1 = Reading("ABC123", c1, 36000.0)
r2 = Reading("ABC123", c2, 36240.0)
r3 = Reading("XYZ999", c1, 36000.0)
r4 = Reading("XYZ999", c2, 36600.0)

check.within("Q2T1: average speed", average_speed(r1, r2), 150.0, 0.001)
check.expect("Q2T2: is speeding", is_speeding(r1, r2, 100), True)
check.expect("Q2T3: not speeding", is_speeding(r1, r2, 200), False)
check.expect("Q2T4: eq reading", r1 == Reading("ABC123", c1, 36000.0), True)

h = Highway()
check.expect("Q3T1: add reading", h.add_reading(r1), None)
h.add_reading(r2)
h.add_reading(r3)
h.add_reading(r4)
check.expect("Q3T2: get readings", h.get_readings("ABC123"), [r1, r2])
check.expect("Q3T3: find speeders", h.find_speeders(100), ["ABC123"])

check.set_file_exact("tickets.txt", "ABC123,150.0")
check.expect("Q4T1: write tickets", write_tickets(h, 100, "tickets.txt"), None)
