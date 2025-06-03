from PM import PM
from VM import VM
import random
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def cost_function(PMs):
    reward = 0
    for PM in PMs:
        if PM.Remaining_Capacity < 0:
            reward = -100
            break
        if PM.Remaining_Capacity == 0:
            reward += 50
        if PM.Remaining_Capacity == PM.Capacity:
            reward += 100
    return reward

PMs = [PM(random.randint(16, 24)) for _ in range(5)]
VMs = [VM(random.randint(6, 10)) for _ in range(5)]

PMs_Copy = copy.deepcopy(PMs)

for VM in VMs:
    random.shuffle(PMs)
    for PM in PMs:
        PM.add_VM(VM)
        break

initial_reward = cost_function(PMs)
list_of_rewards = []
list_of_rewards.append(initial_reward)

TABU_LIST_SIZE = 5
tabu_list = []

for i in range(100):
    PMs_Copy = copy.deepcopy(PMs)
    for pm in PMs_Copy:
        for vm in pm.VMs:
            vm.PM = pm

    VMs_Copy = []
    for pm in PMs_Copy:
        VMs_Copy.extend(pm.VMs)

    vm1 = random.choice(VMs_Copy)
    vm2 = random.choice(VMs_Copy)

    while vm1 == vm2 or vm1.PM == vm2.PM:
        vm1 = random.choice(VMs_Copy)

    pm1 = vm1.PM
    pm2 = vm2.PM
    pm1.remove_vm(vm1)
    pm1.add_VM(vm2)
    pm2.remove_vm(vm2)
    pm2.add_VM(vm1)
    (vm1.PM, vm2.PM) = (vm2.PM, vm1.PM)

    reward = cost_function(PMs_Copy)
    move = [vm1.id, vm2.id]
    move.sort()
    if move in tabu_list:
        if reward > list_of_rewards[-1]:
            PMs = copy.deepcopy(PMs_Copy)
            for pm in PMs:
                for vm in pm.VMs:
                    vm.PM = pm
            if len(tabu_list) == TABU_LIST_SIZE:
                tabu_list.pop(0)
            tabu_list.append(move)
        continue

    else:
        if reward > list_of_rewards[-1]:

            PMs = copy.deepcopy(PMs_Copy)
            for pm in PMs:
                for vm in pm.VMs:
                    vm.PM = pm
    list_of_rewards.append(reward)
    for i in range(1, len(list_of_rewards)):
        if list_of_rewards[i] < list_of_rewards[i - 1]:
            list_of_rewards[i] = list_of_rewards[i - 1]

plt.figure(figsize=(10, 4))
plt.plot(list_of_rewards, linestyle='-')
plt.title('Reward Progress Over Iterations')
plt.xlabel('Iteration')
plt.ylabel('Reward')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
colors = {}
y_ticks = []
y_labels = []

for i, pm in enumerate(PMs):
    x = 0
    for vm in pm.VMs:
        if vm.id not in colors:
            # Assign a unique random color for each VM
            colors[vm.id] = "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
        plt.barh(f"PM {i}", vm.Size, left=x, color=colors[vm.id], edgecolor='black')
        x += vm.Size

# Add legend
legend_patches = [mpatches.Patch(color=color, label=f"VM {vm_id}") for vm_id, color in colors.items()]
plt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', title="VMs")
plt.title("Final VM Allocation per PM")
plt.xlabel("Capacity Used")
plt.tight_layout()
plt.show()