import angr
import sys
project = angr.Project('simple')
initial_state = project.factory.entry_state()
simulation = project.factory.simgr(initial_state)

def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return 'Access Granted' in stdout_output.decode("utf-8") 

def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return 'Access Denied' in stdout_output.decode("utf-8") 
    
simulation.explore(find=is_successful, avoid=should_abort)

if simulation.found:
    solution_state = simulation.found[0]
    print("Found solution")
    print(solution_state.posix.dumps(sys.stdin.fileno()))
else:
    raise Exception('Could not find the password')