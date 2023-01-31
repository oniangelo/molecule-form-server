import sys
sys.path.append('/home/gambacorta/Scrivania/Nico/website/molecule-form-server/')
from predizione import models_sequence 


#print(sys.argv[1])
out = models_sequence(sys.argv[1])
print(out[0])
