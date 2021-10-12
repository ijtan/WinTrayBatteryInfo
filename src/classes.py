class metric:
    def __init__(self, name, unit, function_name,value=0, hidden=False):
        self.name = name
        self.unit = unit
        self.value = value
        self.function_name = function_name
        self.hidden = hidden

    
    def __str__(self):
        if self.hidden:
            return ""
        else:
            return str(self.name + ": " + str(self.value) + self.unit)
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit and self.value() == other.value()
    
    def __ne__(self, other):
        return not self.__eq__(other)


class battery:
    def __init__(self,batt,metrics=[]):
        self.batt = batt
        self.metrics = metrics
    
    def update(self):
        for m in self.metrics:
            m.value = getattr(self.batt, m.function_name)
        return self.metrics

    def __str__(self):
        self.update()
        return "".join([str(m)+'\n' for m in self.metrics])
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.metrics == other.metrics
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def add_metric(self, metric):
        self.metrics.append(metric)
        # return self.metrics.index(metric)
    
    def remove_metric(self, metric):
        self.metrics.remove(metric)
    
    def get_metric(self, name):
        for m in self.metrics:
            if m.name == name:
                return m
        return None
    
    def get_metrics(self):
        return self.metrics