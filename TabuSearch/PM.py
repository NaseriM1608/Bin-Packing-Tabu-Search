class PM:
    def __init__(self, Capacity):
        self.Capacity = Capacity
        self.Remaining_Capacity = Capacity
        self.VMs = []

    def remaining_capacity(self):
        return self.Remaining_Capacity

    def reduce_capacity(self, VM):
        self.Remaining_Capacity -= VM.Size

    def add_VM(self, VM):
        self.VMs.append(VM)
        self.reduce_capacity(VM)
        VM.PM = self

    def remove_vm(self, VM):
        self.VMs.remove(VM)
        self.Remaining_Capacity += VM.Size
        VM.PM = None
