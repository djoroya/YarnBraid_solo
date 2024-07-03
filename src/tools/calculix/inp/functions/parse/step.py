from tools.calculix.inp.StepCard import StepCard

def parse_step(step_lines,new_cards):

    step_lines = [line for line in step_lines 
                  if line != '']
    
    # remove \n
    step_lines = [line.replace("\n","") for line in step_lines]
    
    # strip left and right
    step_lines = [line.strip() for line in step_lines]

    # remove **
    step_lines = [line for line in step_lines 
                  if not line.startswith('**')]
    # remove *END STEP
    step_lines = [line for line in step_lines 
                  if not line.startswith("*END STEP")]
    head = step_lines[0]
    head = head.split(",")

    type = step_lines[1]

    content = step_lines[2:]

    index = [i for i, line in enumerate(content) 
             if line.startswith('*')]

    cards = [content[index[i]:index[i+1]] 
             for i in range(len(index)-1)]

    return [StepCard(cards)]